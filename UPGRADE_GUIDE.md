# Pyscent 升级指南

## 概述

本次升级为 Pyscent 添加了以下功能：

1. **配置系统** - YAML配置文件支持
2. **新检测器** - 4个新的代码异味检测器
3. **可视化增强** - 支持多种图表类型
4. **单元测试** - 新增测试覆盖

## 新增功能

### 1. 配置系统

创建 `config.yaml` 文件来自定义检测行为：

```yaml
thresholds:
  magic_number_threshold: 3
  duplicate_code_similarity: 80

ignore:
  directories:
    - "venv"
    - "__pycache__"
  detectors:
    - "duplicate_code"  # 禁用某个检测器

visualization:
  chart_types:
    - "bar"
    - "pie"
```

### 2. 新检测器

#### 魔法数字检测器 (`magic_number_detector.py`)
- 检测代码中未命名的数字字面量
- 可配置出现次数阈值

#### 注释代码检测器 (`commented_code_detector.py`)
- 检测被注释掉的代码块
- 识别连续3行以上的注释代码

#### 未使用成员检测器 (`unused_member_detector.py`)
- 检测类中未使用的属性和方法
- 排除私有成员（以_开头）

#### 重复代码检测器 (`duplicate_code_detector.py`)
- 检测函数级别的重复代码
- 使用AST相似度比较

### 3. 可视化增强

现在支持多种图表类型：
- **条形图** (bar) - 默认，显示文件级别的统计
- **饼图** (pie) - 显示分布比例
- **散点图** (scatter) - 显示数据分布
- **热力图** (heatmap) - 显示密度分布

在 `config.yaml` 中配置：

```yaml
visualization:
  chart_types:
    - "bar"
    - "pie"
```

## 使用方法

### 基本使用

```bash
python CodeSmellTool.py <项目路径>
```

### 使用配置文件

程序会自动查找项目根目录下的 `config.yaml`，也可以修改代码传入配置路径。

### 运行测试

```bash
python -m pytest tests/test_new_detectors.py
```

## 文件结构

```
Pyscent-master/
├── config.yaml                    # 配置文件（新增）
├── src/
│   ├── config_loader.py           # 配置加载模块（新增）
│   └── Detector/
│       ├── magic_number_detector.py      # 魔法数字检测器（新增）
│       ├── commented_code_detector.py    # 注释代码检测器（新增）
│       ├── unused_member_detector.py      # 未使用成员检测器（新增）
│       └── duplicate_code_detector.py   # 重复代码检测器（新增）
├── tools/
│   └── viz_generator.py           # 可视化生成器（升级）
└── tests/
    └── test_new_detectors.py      # 新检测器测试（新增）
```

## 配置说明

### 阈值配置

- `magic_number_threshold`: 魔法数字出现次数阈值（默认：3）
- `duplicate_code_similarity`: 重复代码相似度阈值（默认：80%）

### 忽略规则

- `directories`: 忽略的目录列表
- `files`: 忽略的文件模式
- `detectors`: 禁用的检测器列表

### 可视化配置

- `chart_types`: 要生成的图表类型列表
- `figure_size`: 图表尺寸（宽x高，单位：英寸）

## 注意事项

1. 新检测器可能需要额外时间，特别是重复代码检测
2. 配置文件使用YAML格式，注意缩进
3. 如果配置文件不存在，将使用默认配置
4. 图表生成可能需要更多内存，特别是热力图

## 未来改进

- [ ] 并行处理优化
- [ ] 更多图表类型
- [ ] HTML报告格式
- [ ] 增量分析支持

