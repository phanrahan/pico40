from pico40.asm import *
from pico40.setup import makepicoicestick

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop = label()
    add(r0,r1)
    st(r0, 0)
    jmp(loop)

main = makepicoicestick(prog, 8, 8)
