from pico40.asm import *
from pico40.setup import makepicoicestick

def prog():
    mov(r0, r0)
    jmp(0)

main = makepicoicestick(prog, 8, 8, debug='inst')

