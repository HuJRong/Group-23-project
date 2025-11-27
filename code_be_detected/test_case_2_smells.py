# test_case_2_smells.py

def long_branch_test(x):
    if x == 1: return "A"
    elif x == 2: return "B"
    elif x == 3: return "C"
    elif x == 4: return "D"
    elif x == 5: return "E"
    elif x == 6: return "F"
    elif x == 7: return "G"
    elif x == 8: return "H"
    elif x == 9: return "I"
    elif x == 10: return "J"
    elif x == 11: return "K"
    elif x == 12: return "L"
    else: return "Z"  # Long Branch

# Duplicate Code
def helper_func_1(a, b):
    return a + b * 2 + 3

def helper_func_2(a, b):
    return a + b * 2 + 3  # 完全重复

# Commented Code
# old_result = long_branch_test(3)
# print(old_result)

# Long Lambda
long_lambda = lambda x: sum([i for i in range(100) if i % 2 == 0 and i > 10])
