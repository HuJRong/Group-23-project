"""
注释代码检测器
检测被注释掉的代码块
"""
import ast
import os
import re
from typing import List, Tuple, Dict
try:
    from src.config_loader import get_config
except ImportError:
    def get_config():
        class SimpleConfig:
            def should_ignore_file(self, path):
                return False
            def get_logs_dir(self):
                return "output/logs"
        return SimpleConfig()


def detect_commented_code(directory: str) -> Tuple[int, Dict]:
    """
    检测目录中所有Python文件的注释代码
    
    Args:
        directory: 要检测的目录路径
        
    Returns:
        (注释代码块数量, 最严重的注释代码信息)
    """
    commented_blocks = []
    worst_block = {}
    max_lines = 0
    
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            config = get_config()
            if config.should_ignore_file(os.path.join(directory, filename)):
                continue
                
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, encoding='UTF8') as f:
                    lines = f.readlines()
                    file_blocks = _detect_commented_code_in_file(lines)
                    
                    for start_line, end_line, block_lines in file_blocks:
                        commented_blocks.append((filename, start_line, end_line, block_lines))
                        if block_lines > max_lines:
                            max_lines = block_lines
                            worst_block = {
                                "filename": filename,
                                "start_line": start_line,
                                "end_line": end_line,
                                "lines": block_lines
                            }
            except Exception as e:
                continue
    
    # 生成日志
    _generate_log(commented_blocks)
    
    return len(commented_blocks), worst_block


def _detect_commented_code_in_file(lines: List[str]) -> List[Tuple[int, int, int]]:
    """
    在单个文件中检测注释代码
    
    检测规则：
    1. 连续3行以上的注释
    2. 注释中包含Python关键字或操作符
    3. 注释看起来像代码（包含赋值、函数调用等）
    
    Args:
        lines: 文件行列表
        
    Returns:
        [(起始行号, 结束行号, 行数), ...]
    """
    blocks = []
    current_block_start = None
    current_block_lines = []
    
    # Python关键字和操作符模式
    CODE_PATTERNS = [
        r'\b(def|class|if|elif|else|for|while|try|except|return|import|from)\b',
        r'[=+\-*/%<>!&|]',  # 操作符
        r'\(.*\)',  # 函数调用
        r'\[.*\]',  # 列表/字典访问
    ]
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # 检查是否是注释行
        if stripped.startswith('#') and len(stripped) > 1:
            comment_content = stripped[1:].strip()
            
            # 检查注释内容是否像代码
            is_code_like = any(re.search(pattern, comment_content) for pattern in CODE_PATTERNS)
            
            if is_code_like:
                if current_block_start is None:
                    current_block_start = i
                    current_block_lines = [i]
                else:
                    current_block_lines.append(i)
            else:
                # 如果当前有代码块且超过3行，保存它
                if current_block_start is not None and len(current_block_lines) >= 3:
                    blocks.append((current_block_start, current_block_lines[-1], len(current_block_lines)))
                current_block_start = None
                current_block_lines = []
        else:
            # 非注释行，结束当前块
            if current_block_start is not None and len(current_block_lines) >= 3:
                blocks.append((current_block_start, current_block_lines[-1], len(current_block_lines)))
            current_block_start = None
            current_block_lines = []
    
    # 处理文件末尾的块
    if current_block_start is not None and len(current_block_lines) >= 3:
        blocks.append((current_block_start, current_block_lines[-1], len(current_block_lines)))
    
    return blocks


def _generate_log(commented_blocks: List[Tuple[str, int, int, int]]):
    """生成注释代码日志"""
    config = get_config()
    log_dir = config.get_logs_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "commented_code_logs.txt")
    
    if commented_blocks:
        with open(log_path, "w", encoding="utf8") as log:
            for filename, start_line, end_line, lines in commented_blocks:
                log.write(f"filename: {filename}, start_line: {start_line}, end_line: {end_line}, lines: {lines}\n")

