# test_case_1_smells.py

class ComplexClass:
    def __init__(self):
        # Too Many Attributes
        self.a1 = 1
        self.a2 = 2
        self.a3 = 3
        self.a4 = 4
        self.a5 = 5
        self.a6 = 6
        self.a7 = 7
        self.a8 = 8  # 超过阈值 → Too Many Attributes
        self.result = 0

    def calc(self, x, y, z, m, n, p, q, r):  # Long Parameter List
        try:
            # Magic Numbers
            self.result = (x + y + z) * 3 + 42  
        except:
            pass  # Useless Try/Except
        return self.result

    def display(self):
        print(f"Result is {self.result}")
