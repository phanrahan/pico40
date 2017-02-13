import sys
from magma import *
from pico.asm import *
from setup import makepico

def prog():
    ldlo(r0, 0b01010101)
    ldlo(r1, 0b10101010)
    xor(r1, r0)
    st(r1, 0)
    jmp(0)

main = makepico(prog)

compile(sys.argv[1], main)
