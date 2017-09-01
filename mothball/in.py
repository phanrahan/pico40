from pico import *


def prog():
    ini(r0, 0)
    outi(r0, 0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
