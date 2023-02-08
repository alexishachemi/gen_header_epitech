options = {
    "help": False,
    "ignore": False,
    "include": False,
    "merge": [False, ""],
    "recursive": False,
    "title": False
}
options_flags = [
        ['h', "help"],
        ['i', "ignore"],
        ['I', "include"],
        ['r', "recursive"],
        ['t', "title"],
    ]

def add_options(opt):
    for flag in options_flags:
        if flag[0] == opt:
            options[flag[1]] = True

def check_merge_option(arg, pop_index, av):
    if not 'm' in arg[1]:
        return 0
    if (arg[0] == len(av) - 1):
        return -1
    pop_index.append(arg[0] + 1)
    options["merge"][0] = True
    options["merge"][1] = av[arg[0] + 1]
    return 0

def check_valid_flags(flags):
    valid_flags = [f[0] for f in options_flags]
    valid_flags.append('m')
    for i in range(1, len(flags)):
        if not flags[i] in valid_flags:
            return -1
    return 0

def set_options(av):
    pop_index = []
    for arg in enumerate(av):
        if arg[1][0] != '-':
            continue
        if check_valid_flags(arg[1]) == -1:
            return -1
        if check_merge_option(arg, pop_index, av) == -1:
            return -1
        for i in range(1, len(arg[1])):
            add_options(arg[1][i])
        pop_index.append(arg[0])
    pop_index.sort(reverse=True)
    for i in pop_index:
        av.pop(i)
    return 0
