"""
魔法数字检测器
检测代码中出现的魔法数字（未命名的数字字面量）
"""
import ast
import os
from collections import Counter
from typing import List, Tuple, Dict

# 尝试导入配置，如果失败则使用默认值
try:
    from src.config_loader import get_config
except ImportError:
    def get_config():
        class SimpleConfig:
            def get_threshold(self, name, default):
                defaults = {"magic_number_threshold": 3}
                return defaults.get(name, default)
            def should_ignore_file(self, path):
                return False
            def get_logs_dir(self):
                return "output/logs"
        return SimpleConfig()


def detect_magic_numbers(directory: str) -> Tuple[int, Dict]:
    """
    检测目录中所有Python文件的魔法数字
    
    Args:
        directory: 要检测的目录路径
        
    Returns:
        (魔法数字总数, 最严重的魔法数字信息)
    """
    config = get_config()
    threshold = config.get_threshold("magic_number_threshold", 3)
    
    magic_numbers = []
    worst_magic = {}
    max_count = 0
    
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            if config.should_ignore_file(os.path.join(directory, filename)):
                continue
                
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, encoding='UTF8') as f:
                    data = f.read()
                    tree = ast.parse(data)
                    file_magic = _detect_magic_numbers_in_file(tree, threshold)
                    
                    for number, count, lineno in file_magic:
                        magic_numbers.append((filename, number, count, lineno))
                        if count > max_count:
                            max_count = count
                            worst_magic = {
                                "filename": filename,
                                "number": number,
                                "count": count,
                                "lineno": lineno
                            }
            except Exception as e:
                continue
    
    # 生成日志
    _generate_log(magic_numbers)
    
    return len(magic_numbers), worst_magic


def _detect_magic_numbers_in_file(tree: ast.AST, threshold: int) -> List[Tuple[float, int, int]]:
    """
    在单个文件中检测魔法数字
    
    Args:
        tree: AST树
        threshold: 出现次数阈值
        
    Returns:
        [(数字值, 出现次数, 行号), ...]
    """
    number_counter = Counter()
    number_locations = {}  # {number: first_lineno}
    
    # 排除常见的常量数字
    EXCLUDED_NUMBERS = {0, 1, -1, 2, -2, 10, 100, 1000, 60, 24, 7, 3.14}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            number = node.value
            # 排除常见常量
            if number not in EXCLUDED_NUMBERS:
                number_counter[number] += 1
                if number not in number_locations:
                    number_locations[number] = node.lineno
    
    # 返回出现次数超过阈值的数字
    result = []
    for number, count in number_counter.items():
        if count >= threshold:
            result.append((number, count, number_locations[number]))
    
    return result


def _generate_log(magic_numbers: List[Tuple[str, float, int, int]]):
    """生成魔法数字日志"""
    config = get_config()
    log_dir = config.get_logs_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "magic_number_logs.txt")
    
    if magic_numbers:
        with open(log_path, "w", encoding="utf8") as log:
            for filename, number, count, lineno in magic_numbers:
                log.write(f"filename: {filename}, number: {number}, count: {count}, lineno: {lineno}\n")

