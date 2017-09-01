from pico import *


def prog():

    # ANODE - 0 bit turns the digit on
    movi(r0, 0)
    outi(r0, 2)

    # SEGMENT - 1 bit turns the digit off
    ini(r0, 0)
    outi(r0, 3)

    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
