from pico import *

DELAY = 255


def delay(d):
    movi(r1, d)
    loop1 = label()
    movi(r2, d)
    loop2 = label()
    movi(r3, d)
    loop3 = label()
    subi(r3, 1)
    jnz(loop3)
    subi(r2, 1)
    jnz(loop2)
    subi(r1, 1)
    jnz(loop1)

    ret()


def prog():
    d = 5

    movi(r0, 0)
    call(5)
    xori(r0, 1)
    outi(r0, 0)
    jmp(0)

    assert d == label()
    delay(DELAY)


mem = assemble(prog)

save(mem, 'a.mem')
