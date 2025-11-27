# test_case_3_smells.py

class MultiProblemClass:
    def __init__(self):
        self.x = 10     # unused
        self.y = 20     # unused
        self.z = 30     # unused

    # Too Many Methods
    def m1(self): pass
    def m2(self): pass
    def m3(self): pass
    def m4(self): pass
    def m5(self): pass
    def m6(self): pass
    def m7(self): pass
    def m8(self): pass
    def m9(self): pass
    def m10(self): pass
    def m11(self): pass
    def m12(self): pass
    def m13(self): pass
    def m14(self): pass
    def m15(self): pass
    def m16(self): pass
    def m17(self): pass
    def m18(self): pass
    def m19(self): pass
    def m20(self): pass
    def m21(self): pass  # 超过阈值

    def compute(self):
        # Magic Numbers + Long List Comprehension
        result = [i * 3 + 7 for i in range(100) if i % 3 == 0 and i < 90]
        return sum(result)
