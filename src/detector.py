import ast
import os
from fpdf import FPDF
import sys
from .Detector.class_coupling_detector import detect_class_cohesion
from .Detector.cyclomatic_complexity_detector import detect_cyclomatic_complexity
from .Detector.long_lambda_detector import detect_long_lambda
from .Detector.long_list_comp_detector import detect_long_list_comp
from .Detector.pylint_output_detector import detect_pylint_output
from .Detector.shotgun_surgery_detector import detect_shotgun_surgery
from .Detector.useless_exception_detector import detect_useless_exception
from .Detector.magic_number_detector import detect_magic_numbers
from .Detector.commented_code_detector import detect_commented_code
from .Detector.unused_member_detector import detect_unused_members
from .Detector.duplicate_code_detector import detect_duplicate_code
from .config_loader import get_config
from tools.viz_generator import add_viz

def detect_main(directory, config_path=None):
    """
    主检测函数
    
    Args:
        directory: 要检测的目录路径
        config_path: 配置文件路径（可选）
    """
    # 加载配置
    if config_path:
        config = get_config(config_path)
    else:
        config = get_config()
    
    # Get stats for files in directory
    stats_dict = get_stats(directory)

    # Setup PDF
    pdf = FPDF(format='letter')
    pdf.add_page()
    
    # Enable Unicode support for Chinese characters
    pdf.set_auto_page_break(auto=True, margin=15)

    dirname = os.path.basename(os.path.normpath(directory))

    # Print Title
    pdf.set_font("times", style='b', size=24)
    header_text = 'Code Smell Summary: {}'.format(dirname)
    write_pdf_line(pdf, header_text, 20)

    pdf.set_font("times", size=12)
    # Print Pylint Output
    header_text = "[ Long Methods ]"
    write_pdf_line(pdf, header_text, 10)
    long_method, long_params, long_branches, many_attrbs, many_methods = \
        detect_pylint_output(directory)
    pylint_text = "   - Number of Long Methods / Total number of Methods: {} / {}".format(str(long_method[0]),
                                                                                          str(stats_dict["methods"]))
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "   - Longest Method:"
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * File Name: {}".format(long_method[1]['filename'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Line Number: {}".format(long_method[1]['lineno'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Number of Statements: {}".format(long_method[1]['metric'])
    write_pdf_line(pdf, pylint_text, 10)

    header_text = "[ Long Parameter ]"
    write_pdf_line(pdf, header_text, 10)
    pdf.set_font("times", size=12)
    pylint_text = "   - Number of Methods with Long Parameter / Total number of Methods: {} / {}".format(
        str(long_params[0]), str(stats_dict["methods"]))
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "   - Method with Longest Parameter:"
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * File Name: {}".format(long_params[1]['filename'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Line Number: {}".format(long_params[1]['lineno'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Number of Parameters: {}".format(long_params[1]['metric'])
    write_pdf_line(pdf, pylint_text, 10)

    header_text = "[ Long Branches ]"
    write_pdf_line(pdf, header_text, 10)
    pdf.set_font("times", size=12)
    pylint_text = "   - Number of Long Branches: {}".format(str(long_branches[0]))
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "   - Longest Branch:"
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * File Name: {}".format(long_branches[1]['filename'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Line Number: {}".format(long_branches[1]['lineno'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Number of Branches: {}".format(long_branches[1]['metric'])
    write_pdf_line(pdf, pylint_text, 10)

    header_text = "[ Too Many Attributes in Class ]"
    write_pdf_line(pdf, header_text, 10)
    pdf.set_font("times", size=12)
    pylint_text = "   - Number of Classes with Many Attributes: {}/{}".format(str(many_attrbs[0]),
                                                                              str(stats_dict["classes"]))
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "   - Class with most Attributes:"
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * File Name: {}".format(many_attrbs[1]['filename'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Line Number: {}".format(many_attrbs[1]['lineno'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Number of Attributes in Class: {}".format(many_attrbs[1]['metric'])
    write_pdf_line(pdf, pylint_text, 10)

    header_text = "[ Too Many Methods in Class ]"
    write_pdf_line(pdf, header_text, 10)
    pdf.set_font("times", size=12)
    pylint_text = "   - Number of Classes with Many Methods: {}/{}".format(str(many_methods[0]),
                                                                           str(stats_dict["classes"]))
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "   - Class with most methods:"
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * File Name: {}".format(many_methods[1]['filename'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Line Number: {}".format(many_methods[1]['lineno'])
    write_pdf_line(pdf, pylint_text, 10)
    pylint_text = "              * Number of Methods in Class: {}".format(many_methods[1]['metric'])
    write_pdf_line(pdf, pylint_text, 10)

    # Print useless try...except

    header_text = "[ Useless Try/Except Clauses ]"
    write_pdf_line(pdf, header_text, 10)
    useless_try = detect_useless_exception(directory)
    body_text = "   - Number of Useless Try-Except / Total Try-Except: {}/{}".format(str(useless_try[1]),
                                                                                     str(stats_dict["try"]))
    write_pdf_line(pdf, body_text, 10)

    # Print Shotgun Surgery
    header_text = "[ Shotgun Surgery ]"
    num_shotgun, most_external = detect_shotgun_surgery(directory)
    write_pdf_line(pdf, header_text, 10)
    body_text = "   - Smelly Class / Total Class: {}/{}".format(num_shotgun, str(stats_dict["classes"]))
    write_pdf_line(pdf, body_text, 10)
    body_text = "   - Class with Most External Functions:"
    write_pdf_line(pdf, body_text, 10)
    text = "              * File Name: {}".format(most_external[0])
    write_pdf_line(pdf, text, 10)
    text = "              * Class Name: {}".format(most_external[1])
    write_pdf_line(pdf, text, 10)
    text = "              * Number of External Function Calls: {}".format(most_external[2])
    write_pdf_line(pdf, text, 10)

    # Print Cohesion Output
    header_text = "[ Class Cohesion ]"
    write_pdf_line(pdf, header_text, 10)
    cohesion_output = detect_class_cohesion(directory, 30)
    cohesion_text = "   - Classes with Low Cohesion/Total number of Classe: {}/{}".format(str(cohesion_output),
                                                                                          str(stats_dict["classes"]))
    write_pdf_line(pdf, cohesion_text, 10)

    # Print Code Complexity
    header_text = "[ Code Complexity ]"
    write_pdf_line(pdf, header_text, 10)
    cc_output = detect_cyclomatic_complexity(directory)
    cc_text = "   - Blocks with Cyclomatic Complexity Rank Lower than 'C' / Total Number of Code Blocks: {}/{}".format(
        str(cc_output), str(stats_dict["codeblocks"]))
    write_pdf_line(pdf, cc_text, 10)

    # Print Long Lambda
    header_text = "[ Long Lambda ]"
    write_pdf_line(pdf, header_text, 10)
    long_lambda_output = detect_long_lambda(directory, 60)
    long_lambda_text = "   - Number of Long Lambda Functions / Number of Lambda Functions: {}/{}".format(
        str(long_lambda_output[0]), str(stats_dict["lambdas"]))
    write_pdf_line(pdf, long_lambda_text, 10)

    if long_lambda_output[1] != {}:
        text = "   - Longest Lambda:"
        write_pdf_line(pdf, text, 10)
        text = "              * Filename: {}".format(str(long_lambda_output[1]['filename']))
        write_pdf_line(pdf, text, 10)
        text = "              * Line Number: {}".format(str(long_lambda_output[1]['lineno']))
        write_pdf_line(pdf, text, 10)
        text = "              * Lambda Length: {}".format(str(long_lambda_output[1]['line length']))
        write_pdf_line(pdf, text, 10)

    # Print Long List Comprehension
    header_text = "[ Long List Comprehension ]"
    write_pdf_line(pdf, header_text, 10)
    long_list_comp_output = detect_long_list_comp(directory, 72)
    long_list_comp_text = "   - Number of Long List Comprehension / Number of List Comprehensions: {}/{}".format(
        str(long_list_comp_output[0]), str(stats_dict["listcomps"]))
    write_pdf_line(pdf, long_list_comp_text, 10)

    if long_list_comp_output[1] != {}:
        text = "   - Longest List Comprehension:"
        write_pdf_line(pdf, text, 10)
        text = "              * Filename: {}".format(str(long_list_comp_output[1]['filename']))
        write_pdf_line(pdf, text, 10)
        text = "              * Line Number: {}".format(str(long_list_comp_output[1]['lineno']))
        write_pdf_line(pdf, text, 10)
        text = "              * List Comprehension Length: {}".format(str(long_list_comp_output[1]['line length']))
        write_pdf_line(pdf, text, 10)

    # New Detectors
    config = get_config()
    
    # Magic Number Detection
    if not config.should_ignore_detector("magic_number"):
        header_text = "[ Magic Numbers ]"
        write_pdf_line(pdf, header_text, 10)
        magic_output = detect_magic_numbers(directory)
        magic_text = "   - Number of Magic Numbers Found: {}".format(str(magic_output[0]))
        write_pdf_line(pdf, magic_text, 10)
        if magic_output[1] and magic_output[1].get('number') is not None:
            text = "   - Most Frequent Magic Number:"
            write_pdf_line(pdf, text, 10)
            text = "              * Filename: {}".format(str(magic_output[1]['filename']))
            write_pdf_line(pdf, text, 10)
            text = "              * Number: {}".format(str(magic_output[1]['number']))
            write_pdf_line(pdf, text, 10)
            text = "              * Occurrences: {}".format(str(magic_output[1]['count']))
            write_pdf_line(pdf, text, 10)
            text = "              * Line Number: {}".format(str(magic_output[1]['lineno']))
            write_pdf_line(pdf, text, 10)

    # Commented Code Detection
    if not config.should_ignore_detector("commented_code"):
        header_text = "[ Commented Code ]"
        write_pdf_line(pdf, header_text, 10)
        commented_output = detect_commented_code(directory)
        commented_text = "   - Number of Commented Code Blocks: {}".format(str(commented_output[0]))
        write_pdf_line(pdf, commented_text, 10)
        if commented_output[1] and commented_output[1].get('filename'):
            text = "   - Largest Commented Block:"
            write_pdf_line(pdf, text, 10)
            text = "              * Filename: {}".format(str(commented_output[1]['filename']))
            write_pdf_line(pdf, text, 10)
            text = "              * Lines: {} (from line {} to {})".format(
                str(commented_output[1]['lines']),
                str(commented_output[1]['start_line']),
                str(commented_output[1]['end_line']))
            write_pdf_line(pdf, text, 10)

    # Unused Member Detection
    if not config.should_ignore_detector("unused_member"):
        header_text = "[ Unused Class Members ]"
        write_pdf_line(pdf, header_text, 10)
        unused_output = detect_unused_members(directory)
        unused_text = "   - Number of Unused Members: {}".format(str(unused_output[0]))
        write_pdf_line(pdf, unused_text, 10)
        if unused_output[1] and unused_output[1].get('filename'):
            text = "   - File with Most Unused Members:"
            write_pdf_line(pdf, text, 10)
            text = "              * Filename: {}".format(str(unused_output[1]['filename']))
            write_pdf_line(pdf, text, 10)
            text = "              * Unused Count: {}".format(str(unused_output[1]['unused_count']))
            write_pdf_line(pdf, text, 10)

    # Duplicate Code Detection
    if not config.should_ignore_detector("duplicate_code"):
        header_text = "[ Duplicate Code ]"
        write_pdf_line(pdf, header_text, 10)
        duplicate_output = detect_duplicate_code(directory)
        duplicate_text = "   - Number of Duplicate Code Pairs: {}".format(str(duplicate_output[0]))
        write_pdf_line(pdf, duplicate_text, 10)
        if duplicate_output[1] and duplicate_output[1].get('file1'):
            text = "   - Most Similar Duplicate:"
            write_pdf_line(pdf, text, 10)
            text = "              * File 1: {} (function: {}, line: {})".format(
                str(duplicate_output[1]['file1']),
                str(duplicate_output[1]['name1']),
                str(duplicate_output[1]['lineno1']))
            write_pdf_line(pdf, text, 10)
            text = "              * File 2: {} (function: {}, line: {})".format(
                str(duplicate_output[1]['file2']),
                str(duplicate_output[1]['name2']),
                str(duplicate_output[1]['lineno2']))
            write_pdf_line(pdf, text, 10)
            text = "              * Similarity: {:.1f}%".format(duplicate_output[1]['similarity'])
            write_pdf_line(pdf, text, 10)

    line = "================================================================================="
    write_pdf_line(pdf, line, 20)

    add_viz()

    plot_dir = config.get_plots_dir()
    # Create plots directory if it doesn't exist
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir, exist_ok=True)
    
    # Add plots to PDF if they exist
    if os.path.exists(plot_dir) and os.listdir(plot_dir):
        for filename in sorted(os.listdir(plot_dir)):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.pdf')) and '_bar.png' in filename:
                pdf.image(os.path.join(plot_dir, filename), w = pdf.w/3.0, h = pdf.h/5.0)
                pdf.ln(0.15)
    
    # Create output directory if it doesn't exist
    output_dir = config.get_output_dir()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # Output stream to PDF
    pdf.output(os.path.join(output_dir, "{}_review.pdf".format(dirname)))


def write_pdf_line(pdf, text, text_height):
    pdf.write(text_height,text)
    pdf.ln()


def get_stats(directory):
    total_num_method = 0
    total_num_class = 0
    total_num_lambda = 0
    total_num_try_catch = 0
    total_num_list_comp = 0
    total_num_code_blocks = 0
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            file_path = os.path.join(directory, filename)
            with open(file_path, encoding='UTF8') as f:
                data = f.read()
                tree = ast.parse(data)
                for node in ast.walk(tree):
                    if isinstance(node,ast.FunctionDef):
                        total_num_method+=1
                    if isinstance(node,ast.ClassDef):
                        total_num_class+=1
                    if isinstance(node,ast.Lambda):
                        total_num_lambda+=1
                    if isinstance(node,ast.Try):
                        total_num_try_catch += 1
                    if isinstance(node,ast.ListComp):
                        total_num_list_comp+=1
    total_num_code_blocks = total_num_method + total_num_class
    return {"methods":total_num_method,"classes":total_num_class,"lambdas":total_num_lambda,\
            "try":total_num_try_catch,"listcomps":total_num_list_comp,\
            "codeblocks":total_num_code_blocks}

#detect_main("../code-dump/flask-master")