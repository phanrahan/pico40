from pico import *

def prog():
    ldlo(r0, 0x4)
    ldlo(r1, 0x1)
    sub(r0,r1)
    jz(0)
    sub(r0,r1)
    jz(0)
    sub(r0,r1)
    jz(0)
    sub(r0,r1)
    jz(0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
