from pico import *

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    ldlo(r2,16)
    loop1 = label()
    sub(r2, r0)
    jnz(loop1)
    st(r0,0)
    ldlo(r2,16)
    loop1 = label()
    sub(r2, r1)
    jnz(loop1)
    st(r1,0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
