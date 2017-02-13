import sys
from pico.asm import *
from setup import makepicoicestick
from magma import compile

def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop = label()
    add(r0,r1)
    st(r0, 0)
    jmp(loop)

main = makepicoicestick(prog)

compile(sys.argv[1], main)
