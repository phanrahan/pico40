from pico import *

DELAY = -1 # 255 falls outside the range of signed

def delay():
    movi(r1, DELAY)
    loop1 = label()
    movi(r2, DELAY)
    loop2 = label()
    movi(r3, DELAY)
    loop3 = label()
    subi(r3, 1)
    jnz(loop3)
    subi(r2, 1)
    jnz(loop2)
    subi(r1, 1)
    jnz(loop1)


def prog():

    movi(r0, 0)

    loop = label()

    delay()

    xori(r0, 1)
    outi(r0, 0)

    jmp(loop)


mem = assemble(prog)

save(mem, 'a.mem')
