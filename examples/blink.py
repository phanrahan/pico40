from pico40.asm import *
from setup import makepicoicestick

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop0 = label()
    sub(r0,r1)
    jnz(loop0)
    st(r0, 0)
    loop1 = label()
    sub(r0,r1)
    jnz(loop1)
    st(r1, 0)
    jmp(loop0)

main = makepicoicestick(prog, 8, 8)
