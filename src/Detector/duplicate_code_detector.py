"""
重复代码检测器
检测代码中的重复代码块
使用简单的AST节点比较方法
"""
import ast
import os
from typing import List, Tuple, Dict
from collections import defaultdict
try:
    from src.config_loader import get_config
except ImportError:
    def get_config():
        class SimpleConfig:
            def get_threshold(self, name, default):
                defaults = {"duplicate_code_similarity": 80}
                return defaults.get(name, default)
            def should_ignore_file(self, path):
                return False
            def get_logs_dir(self):
                return "output/logs"
        return SimpleConfig()


def detect_duplicate_code(directory: str) -> Tuple[int, Dict]:
    """
    检测目录中所有Python文件的重复代码
    
    Args:
        directory: 要检测的目录路径
        
    Returns:
        (重复代码块数量, 最严重的重复代码信息)
    """
    config = get_config()
    similarity_threshold = config.get_threshold("duplicate_code_similarity", 80)
    
    duplicates = []
    worst_duplicate = {}
    max_similarity = 0
    
    # 收集所有函数
    all_functions = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            if config.should_ignore_file(os.path.join(directory, filename)):
                continue
                
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, encoding='UTF8') as f:
                    data = f.read()
                    tree = ast.parse(data)
                    functions = _extract_functions(tree, filename)
                    all_functions.extend(functions)
            except Exception as e:
                continue
    
    # 比较函数找出重复
    for i, func1 in enumerate(all_functions):
        for func2 in all_functions[i+1:]:
            similarity = _calculate_similarity(func1["ast"], func2["ast"])
            
            if similarity >= similarity_threshold:
                duplicates.append({
                    "file1": func1["filename"],
                    "file2": func2["filename"],
                    "name1": func1["name"],
                    "name2": func2["name"],
                    "lineno1": func1["lineno"],
                    "lineno2": func2["lineno"],
                    "similarity": similarity
                })
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    worst_duplicate = duplicates[-1]
    
    # 生成日志
    _generate_log(duplicates)
    
    return len(duplicates), worst_duplicate


def _extract_functions(tree: ast.AST, filename: str) -> List[Dict]:
    """从AST树中提取所有函数定义"""
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "ast": node,
                "filename": filename,
                "lineno": node.lineno
            })
    
    return functions


def _calculate_similarity(node1: ast.AST, node2: ast.AST) -> float:
    """
    计算两个AST节点的相似度
    使用简化的方法：比较节点类型和结构
    
    Returns:
        相似度百分比 (0-100)
    """
    # 如果节点类型不同，相似度为0
    if type(node1) != type(node2):
        return 0.0
    
    # 获取两个节点的结构特征
    features1 = _extract_features(node1)
    features2 = _extract_features(node2)
    
    # 计算Jaccard相似度
    intersection = len(features1 & features2)
    union = len(features1 | features2)
    
    if union == 0:
        return 100.0 if type(node1) == type(node2) else 0.0
    
    similarity = (intersection / union) * 100
    return similarity


def _extract_features(node: ast.AST) -> set:
    """提取AST节点的特征集合"""
    features = set()
    
    for child in ast.iter_child_nodes(node):
        # 添加节点类型
        features.add(type(child).__name__)
        
        # 对于特定节点，添加更多特征
        if isinstance(child, ast.Name):
            features.add(f"name:{child.id}")
        elif isinstance(child, ast.Constant):
            features.add(f"constant:{type(child.value).__name__}")
        elif isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name):
                features.add(f"call:{child.func.id}")
    
    return features


def _generate_log(duplicates: List[Dict]):
    """生成重复代码日志"""
    config = get_config()
    log_dir = config.get_logs_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "duplicate_code_logs.txt")
    
    if duplicates:
        with open(log_path, "w", encoding="utf8") as log:
            for dup in duplicates:
                log.write(f"file1: {dup['file1']}, function1: {dup['name1']}, lineno1: {dup['lineno1']}, "
                         f"file2: {dup['file2']}, function2: {dup['name2']}, lineno2: {dup['lineno2']}, "
                         f"similarity: {dup['similarity']:.1f}%\n")

