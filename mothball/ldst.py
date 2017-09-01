from pico import *

def prog():
    ld(r0, 0)
    st(r0, 0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
