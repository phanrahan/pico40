from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from ..mem import read as readmem
from .seq import Sequencer
from .alu import ALU
from .ram import DualRAM

__all__ = ['Pico', 'DefinePico', 'INSTN']

INSTN = 16

#ADDRN = 8
#MAXINSTS = 1 << ADDRN
#
#DATAN = 8
#N = DATAN


def instructiondecode(inst):
    insttype = inst[14:16]

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

def DefinePico(ADDRN, DATAN, debug=False):

    N = DATAN
    assert N == 8

    pico = DefineCircuit('pico', 
            "data", In(Bits(INSTN)),
            "addr", Out(Bits(DATAN)),
            "port", Out(Bits(DATAN)),
            "we",   Out(Bit),
            "I",    In(Bits(DATAN)),
            "O",    Out(Bits(DATAN)),
            "CLK",  In(Clock) )

    inst = pico.data

    # instruction decode
    addr = inst[0:ADDRN]
    imm = inst[0:N]
    rb = inst[4:8]
    ra = inst[8:12]
    cc = inst[8:12]
    op = inst[12:14]

    print('Building instruction decoder')
    logicinst, arithinst, aluinst, ldloinst, ldinst, stinst, jumpinst =\
        instructiondecode(inst)

    # romb's output is registered
    # phase=0
    #   fetch()
    # phase=1
    #   execute()
    phase = TFF()(1)

    z = DFF(has_ce=True)
    condz = Decode(0, 4)(cc)  #jz
    condnz = Decode(1, 4)(cc) #jnz
    jumpz = LUT3((I0&I2)|(I1&~I2))(condz, condnz, z)

    always = Decode(15, 4)(cc)

    # jump is jump always of jump cond 
    cond = Or(2)(always, jumpz) 
    jump = And(2)(jumpinst, cond)

    # register write
    regwr = LUT4((I0|I1|I2)&I3)(aluinst, ldloinst, ldinst, phase)

    # sequencer
    print('Building sequencer')
    seq = Sequencer(ADDRN)  
    pc = seq(addr, jump, phase)
    wire(pc, pico.addr)

    regiomux = Mux(2, N)
    regiomux(imm, pico.I, ldinst)

    print('Building register file')
    regimux = Mux(2, N)
    regfile = DualRAM(4, N)
    raval, rbval = regfile(ra, rb, ra, regimux, regwr)

    print('Building ALU')
    alu = ALU(N)
    res = alu(raval, rbval, op, arithinst)

    ld = Or(2)(ldinst, ldloinst)
    regimux(res, regiomux, ld) 

    # z flag
    zval = Decode(0, N)
    zwr =  And(2)(aluinst, phase)
    z(zval(res), CE=zwr)

    owr = And(2)(stinst, phase)
    wire(owr, pico.we)

    wire(raval, pico.O)
    wire(imm, pico.port)

    EndCircuit()

    return pico

def Pico(ADDRN, DATAN, debug=False, **kwargs):
    return DefinePico(ADDRN, DATAN, debug=debug)(**kwargs)
