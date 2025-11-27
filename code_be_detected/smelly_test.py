# --- Pyscent "Smelly" Test File (ASCII Only) ---
# This file intentionally contains code smells Pyscent should detect.

# Used for "Shotgun Surgery" detection
def external_helper_function_1():
    pass


def external_helper_function_2():
    pass


def external_helper_function_3():
    pass


def external_helper_function_4():
    pass


def external_helper_function_5():
    pass


def external_helper_function_6():
    pass


class SmellyClass:
    """
    A class intentionally written poorly to trigger Pyscent alerts.
    """

    # Smell 1: Too Many Attributes (Pylint R0902)
    def __init__(self):
        self.attr1 = 1
        self.attr2 = 2
        self.attr3 = 3
        self.attr4 = 4
        self.attr5 = 5
        self.attr6 = 6
        self.attr7 = 7
        self.attr8 = 8  # Pylint default threshold is 7

        # Smell 2: Shotgun Surgery (Pyscent custom check)
        # Pyscent checks for > 5 external calls
        external_helper_function_1()
        external_helper_function_2()
        external_helper_function_3()
        external_helper_function_4()
        external_helper_function_5()
        external_helper_function_6()

    # Smell 3: Too Many Methods (Pylint R0904)
    def method1(self): pass

    def method2(self): pass

    def method3(self): pass

    def method4(self): pass

    def method5(self): pass

    def method6(self): pass

    def method7(self): pass

    def method8(self): pass

    def method9(self): pass

    def method10(self): pass

    def method11(self): pass

    def method12(self): pass

    def method13(self): pass

    def method14(self): pass

    def method15(self): pass

    def method16(self): pass

    def method17(self): pass

    def method18(self): pass

    def method19(self): pass

    def method20(self): pass

    def method21(self): pass  # Pylint default threshold is 20


# Smell 4: Long Parameter List (Pylint R0913)
def very_long_parameter_function(a, b, c, d, e, f, g, h):  # Pylint default is 5
    print(a, b, c, d, e, f, g, h)


# Smell 5: Long Method and Too Many Branches (Pylint R0915, R0912)
def very_long_and_complex_function(val):
    if val == 1:
        print(1)
    elif val == 2:
        print(2)
    elif val == 3:
        print(3)
    elif val == 4:
        print(4)
    elif val == 5:
        print(5)
    elif val == 6:
        print(6)
    elif val == 7:
        print(7)
    elif val == 8:
        print(8)
    elif val == 9:
        print(9)
    elif val == 10:
        print(10)
    elif val == 11:
        print(11)
    elif val == 12:
        print(12)
    elif val == 13:  # Pylint default branch threshold is 12
        print(13)
    return None


def useless_exceptions_demo():
    # Smell 6: Useless Try/Except (General Exception)
    try:
        x = 1 / 0
    except Exception:
        print("Caught a general exception!")

    # Smell 6: Useless Try/Except (Empty 'pass')
    try:
        y = 1 / 0
    except ZeroDivisionError:
        pass


def long_statements_demo():
    # Smell 7: Long Lambda (Pyscent threshold is 60)
    long_lambda_function = lambda a, b, c, d, e, f, g: a + b + c + d + e + f + g + 12345678901234567890

    # Smell 8: Long List Comprehension (Pyscent threshold is 72)
    long_list_comp = [i * i for i in range(100) if i % 2 == 0 and i % 3 == 0 and i % 5 == 0 and i % 7 == 0]

    print(long_lambda_function(1, 2, 3, 4, 5, 6, 7))
    print(long_list_comp)

# test_case_4_long_method.py

def very_long_function(data):
    total = 0
    try:
        for i in range(len(data)):
            if data[i] % 2 == 0:
                total += data[i] * 2 + 3  # Magic Number
            else:
                total += data[i] * 3 + 5
        # 模拟大量业务逻辑（50+ 行）
        total += sum([x for x in range(10)])
        total += sum([x for x in range(20)])
        total += sum([x for x in range(30)])
        total += sum([x for x in range(40)])
        total += sum([x for x in range(50)])
        total += sum([x for x in range(60)])
        total += sum([x for x in range(70)])
        total += sum([x for x in range(80)])
        total += sum([x for x in range(90)])
        total += sum([x for x in range(100)])
        for i in range(20):
            total += i ** 2 + i * 3
        for i in range(20):
            total -= i
        for i in range(20):
            total += i * 2
        for i in range(20):
            total -= i ** 2
        # 继续累加以增加函数长度
        total += sum([i for i in range(200) if i % 5 == 0])
        total += sum([i for i in range(150) if i % 7 == 0])
        total += sum([i for i in range(300) if i % 3 == 0])
        total += sum([i for i in range(400) if i % 9 == 0])
        total += sum([i for i in range(250) if i % 4 == 0])
        total += sum([i for i in range(350) if i % 6 == 0])
        total += sum([i for i in range(500) if i % 8 == 0])
        total += sum([i for i in range(600) if i % 10 == 0])
        total += sum([i for i in range(700) if i % 11 == 0])
        total += sum([i for i in range(800) if i % 13 == 0])
        total += sum([i for i in range(900) if i % 17 == 0])
        total += sum([i for i in range(1000) if i % 19 == 0])
        # 约 60+ 行逻辑
    except:
        pass  # Useless Try/Except
    return total
