# CodeSmellTool - Python Code Smell Detection Tool Brief Description

**CodeSmellTool** is an automated tool for analyzing Python source code and detecting potential "code smells". Combining static code analysis (based on AST and Pylint) with visualization capabilities, it generates detailed logs, statistical charts, and PDF review reports to help developers improve code quality.
## Key Features

The tool supports detecting the following types of code smells:

### Complexity & Size Related
- Long Method
- Long Parameter List
- Long Branches / High Cyclomatic Complexity
- Long Lambda
- Long List Comprehension


### Class Design Related
- Too Many Attributes
- Too Many Methods
- Low Class Cohesion
- Shotgun Surgery (Detects classes with excessive external dependencies)

### Code Quality & Maintainability
- Magic Numbers
- Duplicate Code
- Commented Code
- Unused Class Members
- Useless Try/Except

## Quick Start

### Usage
```bash
python CodeSmellTool.py <目标项目路径>
```
example:
```bash
python CodeSmellTool.py ./my_python_project
```
Note: Only code files are supported for analysis. Configuration files and other non-code assets should not be included.

### Configuration
Customize detection thresholds and ignore rules by modifying the config.yaml file in the project root directory. Example configuration:
```yaml
thresholds:
  long_method: 20           # Methods exceeding 20 lines are considered long
  long_parameter: 5         # Parameters exceeding 5 are considered excessive
  magic_number_threshold: 3 # Numbers appearing more than 3 times are considered magic numbers
  duplicate_code_similarity: 80 # Code with similarity >80% is considered duplicate

ignore:
  directories:
    - "venv"
    - "__pycache__"
  files:
    - "*/test_*.py"
```
### Output Results
After execution, the following files will be generated in the output folder:

PDF Report: *_review.pdf (Contains a summary of all detection results)

Log Files: Under output/logs/ (e.g., magic_number_logs.txt, recording detailed information about each code smell)

Visualization Charts: Under plots/ (Bar charts and pie charts showing code smell distribution)

### Project Structure
```
CodeSmellTool/
├── CodeSmellTool.py       # Entry point
├── src/                   # Core detection logic and implemention of detectors
├── tools/                 # Visualization generators and auxiliary tools
├── config.yaml            # User configuration file
├── requirements.txt       # Project dependencies
└── output/                # Auto-generated output directory
    ├── logs/              # Log files directory
    └── plots/             # Visualization charts directory
```
