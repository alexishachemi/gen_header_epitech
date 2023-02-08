import os
from options import options
from file_handling import *
from datetime import date

header_comment = "/*\n** EPITECH PROJECT, {}\n** {}\n** File description:\n** {}\n*/"
header_guard = "\n#ifndef {}\n\t#define {}\n/*INCLUDE*/\n/*PROTOTYPES*/\n\n"
include_flag = "/*INCLUDE*/"
prototype_flag = "/*PROTOTYPES*/"

def create_empty_header(file_name):
    folder_name = os.path.split(os.getcwd())[1]
    guard_name = file_name.upper() + '_'
    formatted_comment = header_comment.format(date.today().year, folder_name, file_name)
    formatted_guard = header_guard.format(guard_name, guard_name)
    header = formatted_comment.splitlines() + formatted_guard.splitlines()
    header.append(f"#endif /* !{guard_name} */")
    return header

def insert_lines(header, flag, lines):
    offset = 1
    for l in enumerate(header):
        if l[1] == flag:
            for line in lines:
                header.insert(l[0] + offset, line)
                offset += 1

def remove_flags(header):
    for i in range(len(header) - 1, 0, -1):
        if header[i] == include_flag:
            header.pop(i)
        elif header[i] == prototype_flag:
            header[i] = ''

def write_header(path, file_name, header):
    file_path = os.path.join(path, file_name + ".h")
    with open(file_path, 'w') as f:
        for line in header:
            f.write(line + '\n')

def get_header_info(file_path):
    source_file = get_source_file(file_path)
    includes = []
    if options["include"]:
        includes = extract_include(source_file)
    proto = extract_proto(source_file)
    if options["title"]:
        proto.insert(0, f"/* {file_path} */")
    return [includes, proto]
