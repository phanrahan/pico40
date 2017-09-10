from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from ..mem import read as readmem
from .seq import Sequencer
from .alu import ALU
from .ram import DualRAM
from .decoder import InstructionDecoder

__all__ = ['Pico', 'DefinePico', 'INSTN']

INSTN = 16

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
    I = pico.I

    # romb's output is registered, which requires two phases
    # phase=0
    #   fetch()
    # phase=1
    #   execute()
    phase = TFF()(1)

    # instruction decode
    addr = inst[0:ADDRN]
    imm = inst[0:N]
    rb = inst[4:8]
    ra = inst[8:12]
    op = inst[12:14]

    print('Building condition z condition code register')
    z = DFF(has_ce=True)

    print('Building condition c condition code register')
    c = DFF(has_ce=True)

    print('Building instruction decoder')
    arith, ioimm, ld, jump, regwr, zwr, cwr, owr = \
        InstructionDecoder()(inst, phase, z, c)

    # sequencer
    print('Building sequencer')
    seq = Sequencer(ADDRN)  
    pc = seq(addr, jump, phase)

    print('Building register file')
    regfile = DualRAM(4, N)
    raval = regfile.RDATA0
    rbval = regfile.RDATA1

    print('Building ALU')
    alu = ALU(N)
    alu(raval, rbval, 0, op, arith)

    print('Building IO Mux')
    regiomux = Mux(2, N)
    regiomux(I, imm, ioimm)  

    regimux = Mux(2, N)
    regimux(alu.O, regiomux, ld) 

    regfile(ra, rb, ra, regimux, regwr)

    # compute z flag
    zval0 = Decode(0, N//2)(alu.O[0:N//2])
    zval1 = Decode(0, N//2)(alu.O[N//2:N])
    z(And(2)(zval0,zval1), CE=zwr)

    # compute c flag
    c(alu.COUT, CE=cwr)

    wire(imm, pico.port)
    wire(raval, pico.O)
    wire(owr, pico.we)
    wire(pc, pico.addr)

    EndCircuit()

    return pico

def Pico(ADDRN, DATAN, debug=False, **kwargs):
    return DefinePico(ADDRN, DATAN, debug=debug)(**kwargs)
