"""
未使用成员检测器
检测类中未使用的属性和方法
"""
import ast
import os
from typing import List, Tuple, Dict, Set
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


def detect_unused_members(directory: str) -> Tuple[int, Dict]:
    """
    检测目录中所有Python文件的未使用成员
    
    Args:
        directory: 要检测的目录路径
        
    Returns:
        (未使用成员总数, 最严重的文件信息)
    """
    unused_members = []
    worst_file = {}
    max_unused = 0
    
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            config = get_config()
            if config.should_ignore_file(os.path.join(directory, filename)):
                continue
                
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, encoding='UTF8') as f:
                    data = f.read()
                    tree = ast.parse(data)
                    file_unused = _detect_unused_members_in_file(tree)
                    
                    if file_unused:
                        unused_count = len(file_unused)
                        unused_members.append((filename, file_unused))
                        if unused_count > max_unused:
                            max_unused = unused_count
                            worst_file = {
                                "filename": filename,
                                "unused_count": unused_count,
                                "members": file_unused[:5]  # 只保存前5个
                            }
            except Exception as e:
                continue
    
    # 生成日志
    _generate_log(unused_members)
    
    total_unused = sum(len(members) for _, members in unused_members)
    return total_unused, worst_file


def _detect_unused_members_in_file(tree: ast.AST) -> List[Dict]:
    """
    在单个文件中检测未使用的类成员
    
    Args:
        tree: AST树
        
    Returns:
        [{"type": "attribute"/"method", "name": "...", "lineno": ...}, ...]
    """
    unused = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_members = _get_class_members(node)
            used_members = _get_used_members(node)
            
            for member_name, member_info in class_members.items():
                # 排除特殊方法和私有方法（可能被外部调用）
                if member_name.startswith('_'):
                    continue
                
                if member_name not in used_members:
                    unused.append({
                        "type": member_info["type"],
                        "name": member_name,
                        "lineno": member_info["lineno"]
                    })
    
    return unused


def _get_class_members(class_node: ast.ClassDef) -> Dict[str, Dict]:
    """获取类中定义的所有成员"""
    members = {}
    
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            members[item.name] = {
                "type": "method",
                "lineno": item.lineno
            }
        elif isinstance(item, ast.Assign):
            for target in item.targets:
                if isinstance(target, ast.Name):
                    members[target.id] = {
                        "type": "attribute",
                        "lineno": item.lineno
                    }
    
    return members


def _get_used_members(class_node: ast.ClassDef) -> Set[str]:
    """获取类中被使用的成员名称"""
    used = set()
    
    # 遍历类中所有节点，查找成员访问
    for node in ast.walk(class_node):
        if isinstance(node, ast.Attribute):
            # self.xxx 或 obj.xxx
            if isinstance(node.value, ast.Name) and node.value.id == 'self':
                used.add(node.attr)
            elif isinstance(node.value, ast.Name):
                # 可能是类实例访问
                used.add(node.attr)
        elif isinstance(node, ast.Call):
            # 方法调用
            if isinstance(node.func, ast.Attribute):
                used.add(node.func.attr)
    
    return used


def _generate_log(unused_members: List[Tuple[str, List[Dict]]]):
    """生成未使用成员日志"""
    config = get_config()
    log_dir = config.get_logs_dir()
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "unused_member_logs.txt")
    
    if unused_members:
        with open(log_path, "w", encoding="utf8") as log:
            for filename, members in unused_members:
                for member in members:
                    log.write(f"filename: {filename}, type: {member['type']}, name: {member['name']}, lineno: {member['lineno']}\n")

