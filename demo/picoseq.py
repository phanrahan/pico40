import sys
from magma import *
from mantle import *
from parts.lattice.ice40.primitives.RAMB import ROMB

from pico.asm import *
from pico.cpu.seq import Sequencer
from pico.cpu.alu import Arith, Logic
from pico.cpu.ram import DualRAM

from boards.icestick import IceStick

icestick = IceStick()

icestick.Clock.on()
for i in range(8):
    icestick.J1[i].input().on()
for i in range(8):
    icestick.J3[i].output().on()

main = icestick.main()

ADDRN = 8
INSTN = 16
N = 8

def instructiondecode(insttype):
    # alu instructions
    logicinst = ROM2((1 << 0))(insttype)
    arithinst = ROM2((1 << 1))(insttype)
    aluinst =  ROM2((1 << 0) | (1 << 1))(insttype)

    # ld and st (immediate)
    ldloinst = ROM4(1 << 8)(inst[12:16])
    ldinst = ROM4(1 << 10)(inst[12:16])
    stinst = ROM4(1 << 11)(inst[12:16])

    # control flow instructions
    jumpinst = ROM4(1 << 12)(inst[12:16])
    #callinst = ROM4(1 << 13)(inst[12:16])

    return logicinst, arithinst, aluinst, \
           ldloinst, ldinst, stinst, \
           jumpinst

# jmp.py
#def prog():
#    mov(r0,r0)
#    jmp(0)

# alu.py
def prog():
    MAXINSTS = 1 << ADDRN
    for i in range(MAXINSTS/8):
        mov (r0, r0)
        and_(r0, r0)
        or_ (r0, r0)
        xor (r0, r0)
        add (r0, r0)
        sub (r0, r0)
        adc (r0, r0)
        sbc (r0, r0)

mem = assemble(prog, 1 << ADDRN)

# program memory
romb = ROMB(mem)
wire( 1, romb.RCLKE )
wire( 1, romb.RE    )
inst = romb.RDATA

# instruction decode
addr = inst[0:ADDRN]
imm = inst[0:N]
rb = inst[4:8]
ra = inst[8:12]
cc = inst[8:12]
op = inst[12:14]
insttype = inst[14:16]

logicinst, arithinst, aluinst, ldloinst, ldinst, stinst, jumpinst =\
    instructiondecode(insttype)
jump = jumpinst

# romb's output is registered
# phase=0
#   fetch()
# phase=1
#   execute()
phase = TFF()(1)

# sequencer
print 'Building sequencer'
seq = Sequencer(ADDRN)  
pc = seq(addr, jump, phase)
wire(pc, romb.RADDR)

debugmux = Mux(2,8)
debugmux( pc, inst[8:16], phase )
wire( debugmux, main.J3 )

compile(sys.argv[1], main)

