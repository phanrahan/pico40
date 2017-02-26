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

# blink.py
def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop0 = label()
    sub(r0,r1)
    jnz(loop0)
    st(r0, 0)
    loop1 = label()
    sub(r0,r1)
    jnz(loop1)
    st(r1, 0)
    jmp(loop0)

mem = assemble(prog, 1<<ADDRN)

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

# romb's output is registered
# phase=0
#   fetch()
# phase=1
#   execute()
phase = TFF()(1)

# z condition code
print 'Building z'
z = DFF(ce=True)
condz = Decode(0, 4)(cc)  #jz
condnz = Decode(1, 4)(cc) #jnz
jumpz = LUT3((I0&I2)|(I1&~I2))(condz, condnz, z)

# c condition code
print 'Building c'
c = DFF(ce=True)
condc = Decode(2, 4)(cc)
condnc = Decode(3, 4)(cc)
jumpc = LUT3((I0&I2)|(I1&~I2))(condc, condnc, c)

always = Decode(15, 4)(cc)

# jump is jump always of jumpz or jumpc
cond = Or3()(always, jumpz, jumpc) 
jump = And2()(jumpinst, cond)

# register write
regwr = LUT4((I0|I1|I2)&I3)(aluinst, ldloinst, ldinst, phase)


# sequencer
print 'Building sequencer'
seq = Sequencer(ADDRN)  
pc = seq(addr, jump, phase)
wire(pc, romb.RADDR)

print 'Building input'
input = main.J1

print 'Building input mux'
regiomux = Mux(2, N)
regiomux(imm, input, ldinst)

print 'Building register input mux'
regimux = Mux(2, N)

print 'Building registers'
raval, rbval = DualRAM(4, ra, rb, ra, regimux, regwr)

# alu
print 'Building logic unit'
logicunit = Logic(N)
print 'Building arith unit'
arithunit = Arith(N)
print 'Building alu mux'
alumux = Mux(2, N)

print 'Wiring logic unit'
logicres = logicunit(raval, rbval, op[0], op[1])
print 'Wiring arith unit'
arithres = arithunit(raval, rbval, op[0], op[1])
wire(c, arithunit.CIN)
print 'Wiring alumux'
res = alumux(logicres, arithres, arithinst)

print 'Wiring register input mux'
ld = Or2()(ldinst, ldloinst)
regimux(res, regiomux, ld) 

# z flag
print 'Wiring z'
zval = Decode(0, N)
zwr =  And2()(aluinst, phase)
z(zval(res), CE=zwr)

# c flag
print 'Wiring c'
cwr =  And2()(arithinst, phase)
c(arithunit.COUT, CE=cwr)

print 'Wiring output'
output = Register(N, ce=True)
owr = And2()(stinst, phase)
output(raval, CE=owr)

wire(output, main.J3)

compile(sys.argv[1], main)

