from pico import *

def prog():
    ldlo(r0, 0x1)
    ldlo(r1, 0x2)
    add(r1,r0)
    st(r1, 0)
    jmp(0)

mem = assemble(prog)

save(mem, 'a.mem')
