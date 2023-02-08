import os

def get_source_file(file_path):
    with open(file_path, 'r') as f:
        source_file = f.read().splitlines()
    return source_file

def extract_proto(source_file):
    extracted = []
    for i in range(len(source_file) - 1):
        if (source_file[i + 1].startswith('{') and 
            not source_file[i].startswith("static")):
            extracted.append(source_file[i] + ';')
    return extracted

def extract_include(source_file):
    extracted = []
    for line in source_file:
        if line.startswith("#include"):
            extracted.append('\t' + line)
    return extracted
