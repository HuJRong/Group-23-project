import os
import sys
from subprocess import PIPE, run
from typing import List


def output_long_methods(directory: str) -> str:
    """
    Return stdout of the pylint refactoring (R) command.

    Parameters:
        directory (string): path of the directory of source code files

    Return:
        stdout (str): stdout of the pylint command

    """

    file_list = get_file_list(directory)
    if not file_list:
        return ""

    cmd: List[str] = [sys.executable, "-m", "pylint", "--disable=E,W,C,F,I", *file_list]
    result = run(cmd, stdout=PIPE, stderr=PIPE, cwd=directory, text=True)
    return result.stdout


def get_file_list(directory: str) -> List[str]:
    file_list = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".py"):
            file_list.append(filename)
    return file_list