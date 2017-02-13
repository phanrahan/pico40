import sys
from magma import *
from pico.asm import *
from pico.cpu import MAXINSTS
from setup import makepico

def prog():
    for i in range(MAXINSTS/8):
        mov (r0, r0)
        and_(r0, r0)
        or_ (r0, r0)
        xor (r0, r0)
        add (r0, r0)
        sub (r0, r0)
        adc (r0, r0)
        sbc (r0, r0)

main = makepico(prog)

compile(sys.argv[1], main)
