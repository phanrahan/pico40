from magma import *
from mantle import *
from ..mem import read as readmem
from .seq import Sequencer
from .alu import ALU
from .decoder import InstructionDecoder

__all__ = ['Pico', 'DefinePico', 'INSTN']

INSTN = 16

def DefinePico(ADDRN, DATAN, debug=None):

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

    print('Building z condition code register')
    z = DFF(has_ce=True)

    print('Building c condition code register')
    c = DFF(has_ce=True)

    print('Building instruction decoder')
    arithinst, imminst, ioinst, jump, regwr, zwr, cwr, owr = \
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
    alu(raval, rbval, c.O, op, arithinst)

    print('Building Result Mux')
    resmux = Mux(2, N)
    resmux(alu.O, imm, imminst) # either alu or immediate 

    print('Building IO Mux')
    regmux = Mux(2, N)
    regmux(resmux, I, ioinst) # either result or IO

    regfile(ra, rb, ra, regmux, regwr)

    # compute z flag
    zval0 = Decode(0, N//2)(alu.O[0:N//2])
    zval1 = Decode(0, N//2)(alu.O[N//2:N])
    z(And(2)(zval0,zval1), CE=zwr)

    # compute c flag
    c(alu.COUT, CE=cwr)

    wire(imm, pico.port)
    wire(owr, pico.we)
    wire(pc, pico.addr)

    if debug in ['instlo', 'insthi', 'inst', 'raval', 'rbval', 'logic', 'arith', 'alu',
            'reg', 'flags']:
        debugmux = Mux(2,N)
        if   debug == 'instlo':
            debugout = inst[0:8]
        elif debug == 'insthi' or debug == 'inst':
            debugout = inst[8:16]
        elif debug == 'raval':
            debugout = raval
        elif debug == 'rbval':
            debugout = rbval
        elif debug == 'logic':
            debugout = logic.O
        elif debug == 'arith':
            debugout = arith.O
        elif debug == 'alu':
            debugout = alu.O
        elif debug == 'reg':
            debugout = regmux.O
        elif debug == 'flags':
            debugout = array([z.O,c.O,0,0,0,0,0,0])
        wire( debugmux( pc, debugout, phase ), pico.O )
    else:
        wire(raval, pico.O)

    EndCircuit()

    return pico

def Pico(ADDRN, DATAN, debug=None, **kwargs):
    return DefinePico(ADDRN, DATAN, debug=debug)(**kwargs)
