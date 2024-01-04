from stdlib_list import in_stdlib

import os
import re
import sys
import logging

def remove_items(_list, item):
    return list(filter(lambda a: a != item, _list))

def get_local_files():
    local_files = os.listdir(os.getcwd())
    local_files = [file.split(".", 1)[0] for file in local_files]
    return local_files

def combine_lists(lists):
    combined_list = []

    for i in range(0, len(lists)):
        if i > 0:
            combined_list += (["\n"] + lists[i])
        else:
            combined_list += lists[i]

    return combined_list

def get_lines(python_file):
    lines = python_file.readlines()
    lines = [line.strip() for line in lines]
    lines = remove_items(lines, '')

    return lines

def read_python_file(file_path, raw=False):
    if ".py" not in file_path:
        print("Usage: pretty_imports.py <input.py>")
        logging.error("input file is not a python file or not found")
        exit(1)

    try:
        with open(file_path, "r") as python_file:        
                lines = get_lines(python_file)
                return lines
    except FileNotFoundError:
        print("Usage: pretty_imports.py <input.py>")
        logging.error("input file not found or not a python file")
        exit(1)
    
def add_lines(lines, file_path):
    with open(file_path, "w") as python_file:
        python_file.writelines(lines)

def str_contains(lelist, lestr):
    if [e in lelist for e in lelist if e in lestr]:
        return True
    return False

def get_lines_until(stop, file_path):
    lines = []
    del_lines = []

    with open(file_path, "r") as python_file:
        lines = python_file.readlines()

        for num, line in enumerate(lines):
            if line.strip() == stop:
                del_lines = lines[num+1:]

    if del_lines[0] == "\n":
        del_lines.pop(0)

    return del_lines
                            
class Organizer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = read_python_file(self.file_path)
        
        self.raw_imports = []
        self.imports = {
            "third_party": [],
            "builtin": [],
            "local": []
        }

    def get_imports(self):
        filter_keys = ["#", "'", '"']

        for line in self.lines:
            if "from " in line or "import " in line:
                if not str_contains(filter_keys, line):
                    self.raw_imports.append(line)

    def classify_imports(self):
        local_files = get_local_files()
    
        for module in self.raw_imports.copy():
            module_name = re.split("[ .]", module)[1]

            if module_name in local_files:
                self.imports["local"].append(module)
            elif in_stdlib(module_name):
                self.imports["builtin"].append(module)
            else:
                self.imports["third_party"].append(module)

    def alphabetize(self):
        for key, value in self.imports.items():
            self.imports[key] = sorted(value)

    def add_esc_chars(self, esc_char):
        for key, value in self.imports.items():
            self.imports[key] = [elm + esc_char for elm in value]
    
    def replace_imports(self):
        del_lines = get_lines_until(self.raw_imports[-1], self.file_path)
        imports = combine_lists(list(self.imports.values()))
        add_lines(imports + del_lines, self.file_path)
        
    def organize(self):
        self.get_imports()
        self.classify_imports()
        self.alphabetize()
        self.add_esc_chars("\n")
        self.replace_imports()
                
def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.ERROR)

    if len(sys.argv) < 2:
        print("Usage: pretty_imports.py <input.py>")
        logging.error("no input file provided") 
        return 0

    file_path = sys.argv[1]
    
    organizer = Organizer(file_path)
    organizer.organize()

if __name__ == "__main__":
    main()
