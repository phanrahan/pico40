from pico import *


def prog():
    ini(r0, 1)   # from joystick
    outi(r0, 0)  # to leds
    jmp(0)


mem = assemble(prog)

save(mem, 'a.mem')
