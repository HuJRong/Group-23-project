import os
import subprocess
from typing import List


def output_class_cohesion(directory: str) -> str:
    file_list = get_file_list(directory)
    if not file_list:
        return ""

    cmd: List[str] = ["cohesion", "--files", *file_list]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=directory,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return ""

    generate_log(result.stdout.splitlines())
    return result.stdout


def generate_log(output):
    pass
    # print (output[1])
    # log = open("../../logs/class_cohesion_logs", "w")
    # for file in output_list:
    #     filename = file[0]
    #     stmt_lineno_list = file[1]
    #     for stmt_lineno in stmt_lineno_list:
    #         log.write("filename: " + filename + " lineno: " + str(stmt_lineno[1]) + " metric: " + str(
    #             len(stmt_lineno[0])) + "\n")
def get_file_list(directory: str) -> List[str]:
    return [
        filename
        for filename in sorted(os.listdir(directory))
        if filename.endswith(".py")
    ]