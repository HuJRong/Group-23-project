
import fnmatch
import os
import shutil
import sys

from src import detector

def main():
    # print command line arguments
    for arg in sys.argv[1:]:
        print(arg)

def file_extractor(proj_path):
    matches = []
    target_root = os.path.join("code-dump", os.path.basename(os.path.normpath(proj_path)))
    os.makedirs(target_root, exist_ok=True)

    for entry in os.scandir(target_root):
        if entry.is_file():
            try:
                os.unlink(entry.path)
            except OSError as exc:
                print(exc)

    for root, _, filenames in os.walk(proj_path):
        for filename in fnmatch.filter(filenames, "*.py"):
            matches.append(os.path.join(root, filename))

    matches.sort()

    for idx, src in enumerate(matches):
        target_name = f"{idx:04d}_{os.path.basename(src)}"
        shutil.copy2(src, os.path.join(target_root, target_name))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("target directory not specified")
        sys.exit(1)
    file_extractor(sys.argv[1])
    detector.detect_main("./code-dump/" + os.path.basename(sys.argv[1]))
    print('*****     Output Generated     *****')

#if len(sys.argv) != 2:
#    print ("target directory not specified")
#cmd = "python3 tools/py_file_extractor ./sourcecode/"+sys.argv[1]
#result = run(shlex.split(cmd), stdout=PIPE)

#detect_main("./code-dump/"+sys.argv[1])



