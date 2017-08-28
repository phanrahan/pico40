from pico40.asm import *
from setup import makepicoicestick

def prog():
    ld(r0, 0)
    st(r0, 0)
    jmp(0)

main = makepicoicestick(prog, 8, 8)

