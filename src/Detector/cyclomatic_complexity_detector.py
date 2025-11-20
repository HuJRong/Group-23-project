from .CodeSmellHandlers.HandleCyclomaticComplexity.cyclomatic_complexity import (
    output_cyclomatic_complexity,
)


def detect_cyclomatic_complexity(directory: str) -> int:
    return output_cyclomatic_complexity(directory)