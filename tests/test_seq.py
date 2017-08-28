from magma import wire, EndCircuit
from loam.boards.icestick import IceStick, TFF
from mantle.lattice.ice40 import ROMB
from pico40.asm import *
from pico40.cpu.seq import Sequencer

ADDRN = 8
DATAN = 8

def prog():
    for i in range(7):
        nop()
    jmp(0)

mem = assemble( prog, 1<<ADDRN )

icestick = IceStick()
icestick.Clock.on()
for i in range(DATAN):
    icestick.J3[i].output().on()

main = icestick.main()

# program memory
romb = ROMB(mem)
wire( 1, romb.RE )

inst = romb.RDATA
addr = inst[0:ADDRN]
jump = inst[15]

# 2 phases: read inst, execute inst
tff = TFF()
tff(1)

seq = Sequencer(DATAN)

pc = seq(addr, jump, tff)
wire( pc, romb.RADDR )

wire(pc, main.J3)

EndCircuit()

