from pico import *


def prog():
    logn = 4

    mov(r0, r0)
    for i in range(logn):
        n = (1 << i)
        jmp(2 * n)
        for j in range(1, n):
            nop()
    jmp(1)


mem = assemble(prog)

save(mem, 'a.mem')
