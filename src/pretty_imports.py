import re
import os
import sys

from stdlib_list import in_stdlib

def get_code(path):
    code = []

    try:
        with open(path, 'r') as f:
            code = f.read()
    except FileNotFoundError as e:
        sys.exit("ERROR: Input file provided does not exist\n")

    return code 

def get_imports(code):
    pattern = re.compile(r'^(from|import) ([a-zA-Z0-9*_. ]+$)', re.MULTILINE)

    if not pattern.search(code):
        sys.exit("ERROR: No imports found\n")

    imports = pattern.finditer(code)

    return imports, pattern

def get_local_files():
    local_files = os.listdir(os.getcwd())
    local_files = [file.split('.', 1)[0] for file in local_files]
    return local_files

def classify_imports(imports):
    classified_imports = {
        'third_party': [],
        'built_in': [],
        'local': []
    }

    for imp in imports:
        module_name =  re.split('[ .]', imp.group(0))[1]

        if in_stdlib(module_name):
            classified_imports['built_in'].append(imp.group(0))
        elif module_name in get_local_files():
            classified_imports['local'].append(imp.group(0))
        else:
            classified_imports['third_party'].append(imp.group(0))

    return classified_imports

def add_esc_chars(classified_imports):
    for key, value in classified_imports.items():
        classified_imports[key] = [elm + '\n' for elm in value]
        classified_imports[key][-1] += '\n'

def alphabetize(classified_imports):
    for key, value in classified_imports.items():
        classified_imports[key] = sorted(value)

def format_imports(classified_imports):
    combined_imports = sum(list(classified_imports.values()), [])
    return ''.join(combined_imports)

def write_imports(imports, path, code, pattern):
    cleaned_code = re.sub(pattern, '', code).lstrip()

    with open(path, 'w') as f:
        f.write(imports + cleaned_code)

def pretty_imports(path):
    if '.py' not in path:
        sys.exit("ERROR: Input file provided is not a python file\n")

    code = get_code(path) 
    imports, pattern = get_imports(code)
    classified_imports = classify_imports(imports)

    alphabetize(classified_imports)
    add_esc_chars(classified_imports)

    formatted_imports = format_imports(classified_imports)

    write_imports(formatted_imports, path, code, pattern)

if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
    except IndexError:
        sys.exit("ERROR: input file not provided\n")

    pretty_imports(sys.argv[1])
    
    print("Formatting...")
    print("formatting completed\n")
