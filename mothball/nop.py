from pico import *

def prog():
    for i in range(256):
        mov(r0, r0)

mem = assemble(prog)
print len(mem)

save(mem, 'a.mem')
