from pico import *

def prog():
    ldlo(r0, 0x0)
    ldlo(r1, 0x1)
    mov(r1, r1)
    jnz(0)
    mov(r0, r0)
    jnz(0)
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
