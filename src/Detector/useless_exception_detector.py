import os
from .CodeSmellHandlers.HandleExceptionSmell.useless_exception import detect_useless_exception_per_file

def detect_useless_exception(directory):
    output_list = []
    for filename in os.listdir(directory):
        if filename.endswith(".py"):
            file_path = os.path.join(directory, filename)
            long_stmts = detect_useless_exception_per_file(file_path)
            output_list.append((filename,long_stmts))
    dir_name = os.path.basename(os.path.normpath(directory))
    log_count = generate_log(dir_name, output_list)
    
    return ([line for line in output_list if line[1]], log_count)


def generate_log(dir_name, output_list):
    log_count = 0
    log_dir = os.path.join("output", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "useless_exception_logs.txt")
    
    # Check if there's any content to write
    has_content = False
    for file in output_list:
        if file[1]:  # if smelly_lineno_list is not empty
            has_content = True
            break
    
    if has_content:
        log = open(log_path, "w", encoding="utf8")
        for file in output_list:
            filename = file[0]
            smelly_lineno_list = file[1]
            if smelly_lineno_list:
                for lineno in smelly_lineno_list:
                    log.write('FILENAME: {}, LINE: {} ({})\n'.format(filename, str(lineno[0]), lineno[1]))
                    log_count += 1
        log.close()
    return log_count


# test run

# out = detect_useless_exception('../../code-dump/scikit-learn-master')