from pico40.asm import *
from setup import makepicoicestick

def prog():
    ldlo(r0, 0x55)
    ldlo(r1, 0x0f)
    and_(r1, r0)
    st(r1, 0)
    jmp(0)

main = makepicoicestick(prog, 8, 8)


