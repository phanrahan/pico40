from pico import *

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop1 = label()
    sub(r2, r0)
    jnz(loop1)
    loop2 = label()
    sub(r3, r0)
    jnz(loop2)
    loop3 = label()
    sub(r3, r0)
    jnz(loop3)
    st(r0,0)
    loop1 = label()
    sub(r2, r0)
    jnz(loop1)
    loop2 = label()
    sub(r3, r0)
    jnz(loop2)
    loop3 = label()
    sub(r3, r0)
    jnz(loop3)
    st(r1,0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
