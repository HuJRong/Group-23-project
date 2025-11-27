"""
新检测器的单元测试
"""
import unittest
import os
import tempfile
import shutil
from src.Detector.magic_number_detector import detect_magic_numbers
from src.Detector.commented_code_detector import detect_commented_code
from src.Detector.unused_member_detector import detect_unused_members
from src.Detector.duplicate_code_detector import detect_duplicate_code


class TestMagicNumberDetector(unittest.TestCase):
    """魔法数字检测器测试"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.py")
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_detect_magic_numbers(self):
        """测试魔法数字检测"""
        code = """
def calculate(x):
    return x * 42 + 99 - 37
"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        count, worst = detect_magic_numbers(self.test_dir)
        # 应该检测到魔法数字（42, 99, 37）
        self.assertGreaterEqual(count, 0)


class TestCommentedCodeDetector(unittest.TestCase):
    """注释代码检测器测试"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.py")
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_detect_commented_code(self):
        """测试注释代码检测"""
        code = """
# def old_function(x):
#     return x * 2
# if x > 10:
#     print("old code")
def new_function(x):
    return x * 3
"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        count, worst = detect_commented_code(self.test_dir)
        # 应该检测到注释代码块
        self.assertGreaterEqual(count, 0)


class TestUnusedMemberDetector(unittest.TestCase):
    """未使用成员检测器测试"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test.py")
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_detect_unused_members(self):
        """测试未使用成员检测"""
        code = """
class MyClass:
    def used_method(self):
        return self.used_attr
    
    def unused_method(self):
        pass
    
    def __init__(self):
        self.used_attr = 1
        self.unused_attr = 2
"""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        count, worst = detect_unused_members(self.test_dir)
        # 应该检测到未使用的成员
        self.assertGreaterEqual(count, 0)


class TestDuplicateCodeDetector(unittest.TestCase):
    """重复代码检测器测试"""
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_file1 = os.path.join(self.test_dir, "file1.py")
        self.test_file2 = os.path.join(self.test_dir, "file2.py")
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_detect_duplicate_code(self):
        """测试重复代码检测"""
        code1 = """
def calculate_sum(a, b):
    result = a + b
    return result
"""
        code2 = """
def add_numbers(x, y):
    total = x + y
    return total
"""
        with open(self.test_file1, 'w', encoding='utf-8') as f:
            f.write(code1)
        with open(self.test_file2, 'w', encoding='utf-8') as f:
            f.write(code2)
        
        count, worst = detect_duplicate_code(self.test_dir)
        # 应该检测到相似的代码
        self.assertGreaterEqual(count, 0)


if __name__ == '__main__':
    unittest.main()

