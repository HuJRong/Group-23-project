"""
Visualization generator
Supports multiple chart types: bar charts, pie charts, scatter plots, and heat maps
"""
import os
import re
from collections import Counter, defaultdict
from matplotlib.pyplot import *
from matplotlib import pyplot as plt
import numpy as np
try:
    from src.config_loader import get_config
except ImportError:
    def get_config():
        class SimpleConfig:
            def get_plots_dir(self):
                return "plots"
            def get_logs_dir(self):
                return "output/logs"
            def __init__(self):
                self.config = {
                    "visualization": {"chart_types": ["bar"]}
                }
        return SimpleConfig()

output_list = []


def generate_viz(data, label, filename, chart_type="bar"):
    """
    Generate visualization charts
    
    Args:
        data: Log file content
        label: Y-axis label
        filename: Log filename
        chart_type: Chart type ("bar", "pie", "scatter", "heatmap")
    """
    config = get_config()
    chart_types = config.config.get("visualization", {}).get("chart_types", ["bar"])
    
    # Parse data
    parsed_data = _parse_log_data(data, filename)
    if not parsed_data:
        return
    
    # Generate charts based on configuration
    if "bar" in chart_types:
        _generate_bar_chart(parsed_data, label, filename)
    if "pie" in chart_types and len(parsed_data) <= 10:
        _generate_pie_chart(parsed_data, label, filename)
    if "scatter" in chart_types:
        _generate_scatter_chart(parsed_data, label, filename)
    if "heatmap" in chart_types:
        _generate_heatmap(parsed_data, label, filename)


def _parse_log_data(data, filename):
    """Parse log data and return unified format"""
    lines = data.splitlines()
    lines = [line.strip() for line in lines if line.strip()]
    if len(lines) < 1:
        return []
    
    parsed = []
    
    for line in lines:
        try:
            # Parse different formats of logs
            if "filename:" in line:
                # Standard format: "filename: xxx lineno: yyy metric: zzz"
                # Or: "filename: xxx, smelly_lines: yyy, metric: zzz"
                filename_part = line.split("filename:")[1]
                if "," in filename_part:
                    file_name = filename_part.split(",")[0].strip()
                else:
                    file_name = filename_part.split()[0].strip()
                
                # Extract metric value
                metric_value = 1  # Default value
                if "metric:" in line:
                    metric_part = line.split("metric:")[1].strip()
                    try:
                        metric_value = int(metric_part.split()[0])
                    except:
                        pass
                elif "count:" in line:
                    count_part = line.split("count:")[1].strip()
                    try:
                        metric_value = int(count_part.split()[0])
                    except:
                        pass
                elif "similarity:" in line:
                    sim_part = line.split("similarity:")[1].strip()
                    try:
                        metric_value = float(sim_part.split()[0].rstrip('%'))
                    except:
                        pass
                
                parsed.append({
                    "filename": file_name,
                    "value": metric_value
                })
        except Exception as e:
            continue
    
    return parsed


def _generate_bar_chart(data, label, filename):
    """生成条形图"""
    if not data:
        return
    
    # Aggregate data by filename
    file_counts = Counter()
    for item in data:
        file_counts[item["filename"]] += item["value"]
    
    # Limit display to top 20 files
    top_items = file_counts.most_common(20)
    x_val = [item[0] for item in top_items]
    y_val = [item[1] for item in top_items]
    
    figure(figsize=(12, 6))
    bar(x_val, y_val, color="#85b1dd")
    xticks(rotation=0)
    xlabel("File Names")
    title(filename[:-4])  # Remove .txt extension
    ylabel(label)
    tight_layout()
    
    plot_dir = _get_plots_dir()
    savefig(os.path.join(plot_dir, f"{filename[:-4]}_bar.png"), bbox_inches="tight", dpi=150)
    close()


def _generate_pie_chart(data, label, filename):
    """Generate pie chart"""
    if not data or len(data) > 10:
        return
    
    # Aggregate data by filename
    file_counts = Counter()
    for item in data:
        file_counts[item["filename"]] += item["value"]
    
    # Limit display to top 10 files
    top_items = file_counts.most_common(10)
    labels = [item[0] for item in top_items]
    sizes = [item[1] for item in top_items]
    
    figure(figsize=(10, 8))
    pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    title(f"{filename[:-4]} - Distribution")
    axis('equal')
    
    plot_dir = _get_plots_dir()
    savefig(os.path.join(plot_dir, f"{filename[:-4]}_pie.png"), bbox_inches="tight", dpi=150)
    close()


def _generate_scatter_chart(data, label, filename):
    """Generate scatter chart (to show distribution)"""
    if not data:
        return
    
    # Aggregate data by filename
    file_values = defaultdict(list)
    for item in data:
        file_values[item["filename"]].append(item["value"])
    
    # Calculate statistics for each file
    files = []
    means = []
    maxs = []
    
    for file, values in list(file_values.items())[:20]:  # Limit to top 20 files
        files.append(file)
        means.append(np.mean(values))
        maxs.append(np.max(values))
    
    figure(figsize=(10, 6))
    scatter(range(len(files)), means, s=100, alpha=0.6, c=maxs, cmap='viridis')
    colorbar(label='Max Value')
    xticks(range(len(files)), files, rotation=0)
    xlabel("File Names")
    ylabel(f"{label} (mean)")
    title(f"{filename[:-4]} - Distribution")
    tight_layout()
    
    plot_dir = _get_plots_dir()
    savefig(os.path.join(plot_dir, f"{filename[:-4]}_scatter.png"), bbox_inches="tight", dpi=150)
    close()


def _generate_heatmap(data, label, filename):
    """Generate heatmap (by file and time/type)"""
    if not data:
        return
    
    # Aggregate data by filename
    file_counts = Counter()
    for item in data:
        file_counts[item["filename"]] += item["value"]
    
    # Limit display to top 15 files
    top_files = [f[0] for f in file_counts.most_common(15)]
    
    # Create matrix data (simplified here, can be more complex)
    matrix_data = []
    for file in top_files:
        count = file_counts[file]
        matrix_data.append([count])
    
    if not matrix_data:
        return
    
    figure(figsize=(8, max(6, len(top_files) * 0.5)))
    im = imshow(matrix_data, aspect='auto', cmap='YlOrRd', interpolation='nearest')
    colorbar(label=label)
    yticks(range(len(top_files)), top_files)
    xticks([0], ['Count'])
    title(f"{filename[:-4]} - Heatmap")
    tight_layout()
    
    plot_dir = _get_plots_dir()
    savefig(os.path.join(plot_dir, f"{filename[:-4]}_heatmap.png"), bbox_inches="tight", dpi=150)
    close()


def _get_plots_dir():
    """Get plots directory"""
    config = get_config()
    plot_dir = config.get_plots_dir()
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir, exist_ok=True)
    return plot_dir


def add_viz():
    """Generate visualizations for all log files"""
    config = get_config()
    logs_dir = config.get_logs_dir()
    
    if not os.path.exists(logs_dir):
        return
    
    chart_types = config.config.get("visualization", {}).get("chart_types", ["bar"])
    
    for filename in os.listdir(logs_dir):
        if filename.endswith("logs.txt") and "exception" not in filename:
            file_path = os.path.join(logs_dir, filename)
            try:
                with open(file_path, encoding='UTF8') as f:
                    data = f.read()
                    
                    # Determine the label based on the file name
                    if "many" in filename:
                        label = "count"
                    elif "long" in filename:
                        label = "number of characters"
                    elif "magic" in filename:
                        label = "occurrence count"
                    elif "duplicate" in filename:
                        label = "similarity %"
                    elif "commented" in filename:
                        label = "lines of code"
                    elif "unused" in filename:
                        label = "count"
                    else:
                        label = "metric"
                    
                    # Generate charts (use the first chart type in config as primary type)
                    generate_viz(data, label, filename, chart_types[0] if chart_types else "bar")
            except (OSError, IOError) as e:
                continue
