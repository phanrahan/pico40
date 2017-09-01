from pico import *


def prog():
    jmp(2)
    jmp(0)
    call(4)
    jmp(0)
    ret()


mem = assemble(prog)

save(mem, 'a.mem')
