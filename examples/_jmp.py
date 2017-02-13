import sys
from magma import *
from pico.asm import *
from setup import makepico

def prog():
    mov(r0,r0)
    jmp(0)

main = makepico(prog)

compile(sys.argv[1], main)
