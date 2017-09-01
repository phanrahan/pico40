from pico40.asm import *
from pico40.setup import makepicoicestick

def prog():
    ldlo(r0, 0x55)
    st(r0, 0)
    jmp(0)

main = makepicoicestick(prog, 8, 8)

