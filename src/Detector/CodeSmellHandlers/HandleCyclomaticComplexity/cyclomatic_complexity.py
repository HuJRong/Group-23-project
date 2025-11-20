import os
from typing import Iterable

from radon.complexity import cc_visit


def output_cyclomatic_complexity(directory: str, min_rank: str = "C") -> int:
    """
    Count code blocks with cyclomatic complexity worse than the given rank.

    Returns
    -------
    int
        Number of blocks whose rank is alphabetically greater than ``min_rank``.
    """

    total = 0
    for filename in _iter_python_files(directory):
        path = os.path.join(directory, filename)
        try:
            with open(path, encoding="utf8") as file_obj:
                source = file_obj.read()
        except OSError:
            continue

        try:
            blocks = cc_visit(source)
        except (SyntaxError, UnicodeDecodeError):
            continue

        for block in blocks:
            if block.letter > min_rank:
                total += 1

    return total


def _iter_python_files(directory: str) -> Iterable[str]:
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".py"):
            yield filename
