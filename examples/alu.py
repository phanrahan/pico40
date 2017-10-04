from pico40.asm import *
from pico40.setup import makepicoicestick

def prog():
    for i in range(256//8):
        mov (r0, r0)
        and_(r0, r0)
        or_ (r0, r0)
        xor (r0, r0)
        add (r0, r0)
        sub (r0, r0)
        adc (r0, r0)
        sbc (r0, r0)

main = makepicoicestick(prog, 8, 8, debug='inst')

