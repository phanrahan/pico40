from pico40.asm import *
from pico40.setup import makepicoicestick

def prog():
    ldlo(r0, 2)
    ldlo(r1, 2)
    add(r1,r0)
    st(r1, 0)
    jmp(0)

main = makepicoicestick(prog, 8, 8)
