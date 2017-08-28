__all__ = ['assemble', 'emit', 'org', 'equ', 'label', 'word']

MAXINSTS = 0
mem = []
pc = 0

pass_ = 0
labels = {}


def assemble(prog, maxinsts):
    global pc, pass_
    global MAXINSTS
    global mem

    MAXINSTS = maxinsts
    mem = MAXINSTS * [0]

    pass_ = 0
    pc = 0
    prog()

    pass_ = 1
    pc = 0
    prog()

    return mem


def emit(x):
    global mem, pc
    if pc >= 0 and pc < MAXINSTS:
        mem[pc] = x
    pc += 1


def org(value):
    global pc
    pc = value


def equ(name, value):
    global labels
    labels[name] = value


def label(name=None):
    global labels
    if name:
        if pass_ == 0:
            labels[name] = pc
        if pass_ == 1:
            return labels[name]
        return 0
    return pc


def word(value):
    emit(value)

