#!/usr/bin/env python3
## syncs .h files with .c files and creates new .h files accordingly
## does not work with file names containing spaces

import os
from sys import argv as av
from file_handling import *
from header import *
from options import set_options, options

av.pop(0)
help_message = '''USAGE
    ./gen_header [OPTION] SRC DEST
DESCRIPTION
    src         folder where the program will look for .c files.
    dest        folder where the .h files will be generated.
    option      
                -h          display this message.
                -i          do NOT ignore main.c files and main functions
                -I          add includes to the .h file
                -m [FILE]   prototypes and includes will be put
                            on a single .h file with the given name.
                -r          look for .c files recursively.
                -t          add the title of the file in the header.

files containing spaces in their name are unsupported and will be ignored.'''

def add_file_header(file_path, dest, header):
    file_name = os.path.split(file_path)[1].removesuffix(".c")
    header_info = get_header_info(file_path)

    if (header == None):
        file_header = create_empty_header(file_name)
        insert_lines(file_header, include_flag, header_info[0])
        insert_lines(file_header, prototype_flag, header_info[1])
        remove_flags(file_header)
        write_header(dest, file_name, file_header)
    else:
        insert_lines(header, include_flag, header_info[0])
        insert_lines(header, prototype_flag, header_info[1])

def gen_headers_rec(src, dest):
    header = None
    if options["merge"][0]:
        header = create_empty_header(options["merge"][1])
    for dir_path, dir_names, file_names in os.walk(src):
        for f in file_names:
            if (options["ignore"] and f == "main.c") or not f.endswith(".c"):
                continue
            add_file_header(os.path.join(dir_path, f), dest, header)
    if options["merge"][0]:
        remove_flags(header)
        write_header(dest, options["merge"][1], header)

def gen_headers(src, dest):
    header = None
    if options["merge"][0]:
        header = create_empty_header(options["merge"][1])
    for f in os.listdir(src):
        if (options["ignore"] and f == "main.c") or not f.endswith(".c"):
            continue
        add_file_header(os.path.join(src, f), dest, header)
    if options["merge"][0]:
        remove_flags(header)
        write_header(dest, options["merge"][1], header)

def main():
    if set_options(av) == -1:
        exit(84)
    ac = len(av)
    if options["help"] or ac == 0:
        print(help_message)
        exit(0)
    if ac != 2 or not os.path.exists(av[0]) or not os.path.exists(av[1]):
        exit(84)
    if not os.path.isdir(av[0]):
        if av[0].endswith(".c"):
            add_file_header(av[0], av[1], None)
        else:
            exit(84)
    elif options["recursive"]:
        gen_headers_rec(av[0], av[1])
    else:
        gen_headers(av[0], av[1])
    exit(0)

if __name__ == "__main__":
    main()
