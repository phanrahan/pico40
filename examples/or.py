from pico40.asm import *
from setup import makepicoicestick

def prog():
    ldlo(r0, 0b01010101)
    ldlo(r1, 0b00001111)
    or_(r1, r0)
    st(r1, 0)
    jmp(0)

main = makepicoicestick(prog, 8, 8)

