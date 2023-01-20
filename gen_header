#!/usr/bin/env python3
## syncs .h files with .c files and creates new .h files accordingly
## does not work with file names containing spaces

from os import popen, walk, getcwd, system, listdir
from os.path import split, splitext, join, exists
from sys import argv as av
av.pop(0)

include_flag = "/*INCLUDE*/\n"
prototype_flag = "/*PROTOTYPES*/\n"

header_comment = '''/*
** EPITECH PROJECT, 2022
** {}
** File description:
** {}
*/

/*INCLUDE*/

'''

header_guard = '''#ifndef {}
    #define {}

/*PROTOTYPES*/
'''

help_message = '''USAGE
    ./gen_header [OPTION] SRC DEST
DESCRIPTION
    src         folder where the program will look for .c files.
    dest        folder where the .h files will be generated.
    option      -m [FILE]   prototypes and includes will be put
                            on a single .h file with the given name.
                -t          add the title of the file in the header.
                -r          look for .c files recursively.
                -i          do NOT ignore main.c files and main functions
                -h          display this message.

files containing spaces in their name are unsupported and will be ignored.'''

def get_insert_line(lines, flag):
    insert_line = 0
    found_flag = False
    for l in enumerate(lines):
        if flag == l[1]:
            found_flag = True
            insert_line = l[0] + 1
        
        if found_flag and l[1] == "":
            insert_line = l[0]
            break

    return insert_line

def add_includes_to_header(src, header_path):
    with open(header_path, 'r') as f:
        lines = f.readlines()
    
    with open(src, "r") as f:
        includes = [l for l in f.readlines() if l.startswith("#include")]

    header_includes = [l for l in lines if l.startswith("#include")]

    insert_line = get_insert_line(lines, include_flag)

    for i in includes:
        if not i in header_includes:
            lines.insert(insert_line, i)
            insert_line += 1

    with open(header_path, "w") as f:
        f.writelines(lines)

def add_proto_to_header(src, header_path, options):

    split_path = split(src)
    no_include_path = join(split_path[0], "gen_header_" + split_path[1])

    with open(src, 'r') as f:
        c_file = [l for l in f.readlines() if not l.startswith("#include")]

    with open(no_include_path, 'w') as f:
        f.writelines(c_file)

    prototypes = popen(f'cproto "{no_include_path}" -I inlcude/').readlines()
    system(f"rm {no_include_path}")
    if not options["title"]:
        prototypes.pop(0)

    for p in enumerate(prototypes):
        if options["ignore"] and p[1].startswith("int main("):
            print(f"gen_header: ignored main function in {src}")
            prototypes.pop(p[0])

    with open(header_path, 'r') as f:
        lines = f.readlines()

    insert_line = get_insert_line(lines, prototype_flag)

    for p in prototypes:
        if not p in lines:
            lines.insert(insert_line, p)
            insert_line += 1

    with open(header_path, "w") as f:
        f.writelines(lines)

def add_all_to_header(src, header_path, options):
    if header_path == None:
        return

    add_includes_to_header(src, header_path)
    add_proto_to_header(src, header_path, options)

def create_header_file(file_name, dest, options):
    if options["ignore"] and file_name == 'main.c':
        print("gen_header: ignored main.c file")
        return None
    
    if ' ' in file_name:
        print(f"gen_header: ignored file name containing spaces ({file_name})")
        return None

    folder_name = split(getcwd())[-1]
    file_path = join(dest, splitext(file_name)[0] + ".h")

    header = header_comment.format(folder_name, f"{file_name}")
    guard_name = f"{file_name.upper()}_H_"
    guard = header_guard.format(guard_name, guard_name)
    system(f'echo "{header + guard}" > "{file_path}"')
    system(f'echo "#endif /* !{guard_name} */" >> "{file_path}"')
    return file_path

def gen_header(src, dest, options):
    if options["merge"][0]:
        header_path = create_header_file(options["merge"][1], dest, options)

    if not options["recursive"]:
        for file_name in listdir(src):
            path = join(src, file_name)
            if file_name.endswith(".c"):
                if options["merge"][0]:
                    add_all_to_header(path, header_path, options)
                else:
                    add_all_to_header(path, create_header_file(file_name, dest, options), options)
        return
    
    for root, subdir, files in walk(src):
        for f in files:
            if not f.endswith(".c"):
                continue
            path = join(root, f)
            if options["merge"][0]:
                add_all_to_header(path, header_path, options)
            else:
                file_name = splitext(split(path)[-1])[0]
                add_all_to_header(path, create_header_file(file_name, dest), options)

def get_options():
    options = {
        "help": False,
        "title": False,
        "recursive": False,
        "ignore": True,
        "merge": [False, None]
    }
    pop_index = []
    for arg in enumerate(av):
        if arg[1] == '-h':
            options["help"] = True
            pop_index.append(arg[0])
        if arg[1] == '-t':
            options["title"] = True
            pop_index.append(arg[0])
        if arg[1] == '-r':
            options["recursive"] = True
            pop_index.append(arg[0])
        if arg[1] == '-i':
            options["ignore"] = False
            pop_index.append(arg[0])
        if arg[1] == '-m':
            options["merge"][0] = True
            options["merge"][1] = av[arg[0] + 1]
            pop_index.append(arg[0])
            pop_index.append(arg[0] + 1)
    for index in sorted(pop_index, reverse=True):
        av.pop(index)
    return options

def main():
    try:
        options = get_options()
    except IndexError:
        print("gen_header: invalid arguments")
        return 84
    ac = len(av)
    if options["help"]:
        print(help_message)
        return 0

    if ac != 2:
        print("gen_header: invalid arguments")
        return 84

    if not exists(av[0]) or not exists(av[1]):
        print("gen_header: path does not exist")
        return 84

    gen_header(av[0], av[1], options)
    return 0

exit(main())
