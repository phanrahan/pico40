from pico import *
from mem import save


def prog():

    movi(r0, 3)
    outi(r0, 0)
    subi(r0, 1)
    jnc(0)
    jmp(1)


assemble(prog)

save(mem, 'a.mem')
m')
