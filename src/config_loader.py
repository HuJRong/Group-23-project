"""
配置加载模块
支持从YAML配置文件加载配置，并提供默认配置
"""
import os
import yaml
from typing import Dict, Any, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class ConfigLoader:
    """配置加载器"""
    
    DEFAULT_CONFIG = {
        "thresholds": {
            "long_method": 50,
            "long_parameter": 5,
            "long_branches": 10,
            "too_many_attributes": 10,
            "too_many_methods": 20,
            "long_lambda": 60,
            "long_list_comp": 72,
            "low_cohesion": 30,
            "cyclomatic_complexity_rank": "C",
            "duplicate_code_similarity": 80,
            "magic_number_threshold": 3,
        },
        "ignore": {
            "directories": ["venv", "__pycache__", ".git", "node_modules", "*.egg-info"],
            "files": ["*/test_*.py", "*/__init__.py", "*/migrations/*.py"],
            "detectors": [],
        },
        "output": {
            "directory": "output",
            "plots_directory": "plots",
            "logs_directory": "output/logs",
            "generate_pdf": True,
            "generate_html": False,
            "generate_json": False,
        },
        "visualization": {
            "chart_types": ["bar", "pie"],
            "theme": "default",
            "figure_size": {"width": 10, "height": 6},
        },
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置加载器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, config_path: str):
        """从YAML文件加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self._merge_config(self.config, user_config)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {config_path}: {e}")
            print("使用默认配置")
    
    def _merge_config(self, base: Dict, override: Dict):
        """递归合并配置字典"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get_threshold(self, detector_name: str, default: Any = None) -> Any:
        """获取检测器阈值"""
        return self.config.get("thresholds", {}).get(detector_name, default)
    
    def should_ignore_file(self, file_path: str) -> bool:
        """检查文件是否应该被忽略"""
        import fnmatch
        
        # 检查目录忽略规则
        for pattern in self.config.get("ignore", {}).get("directories", []):
            if fnmatch.fnmatch(file_path, f"*{pattern}*"):
                return True
        
        # 检查文件忽略规则
        for pattern in self.config.get("ignore", {}).get("files", []):
            if fnmatch.fnmatch(file_path, pattern):
                return True
        
        return False
    
    def should_ignore_detector(self, detector_name: str) -> bool:
        """检查检测器是否应该被忽略"""
        ignored = self.config.get("ignore", {}).get("detectors", [])
        return detector_name in ignored
    
    def get_output_dir(self) -> str:
        """获取输出目录"""
        return self.config.get("output", {}).get("directory", "output")
    
    def get_plots_dir(self) -> str:
        """获取图表目录"""
        return self.config.get("output", {}).get("plots_directory", "plots")
    
    def get_logs_dir(self) -> str:
        """获取日志目录"""
        return self.config.get("output", {}).get("logs_directory", "output/logs")


# 全局配置实例
_global_config: Optional[ConfigLoader] = None


def get_config(config_path: Optional[str] = None) -> ConfigLoader:
    """获取全局配置实例"""
    global _global_config
    if _global_config is None:
        _global_config = ConfigLoader(config_path)
    return _global_config


def reset_config():
    """重置全局配置（主要用于测试）"""
    global _global_config
    _global_config = None

