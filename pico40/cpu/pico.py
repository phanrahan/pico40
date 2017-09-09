from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from ..mem import read as readmem
from .seq import Sequencer
from .alu import ALU
from .ram import DualRAM

__all__ = ['Pico', 'DefinePico', 'INSTN']

INSTN = 16

class Cond(Circuit):
    IO = ["inst", In(Bits(4)), 
          "cond", In(Bits(4)),
          "z",    In(Bit),
          "c",    In(Bit),
          "jump", Out(Bit)]
    @classmethod
    def definition(io):
        inst = io.inst
        cond = io.cond
        z = io.z
        c = io.c

        # control flow instructions
        jumpinst = ROM4(1 << 12)(inst)
        #callinst = ROM4(1 << 13)(inst)
        #retinst = ROM4(1 << 14)(inst)

        always = Decode(15, 4)(cond)

        condz  = Decode(0, 4)(cond) #jz
        condnz = Decode(1, 4)(cond) #jnz
        jumpz = LUT3((I0&I2)|(I1&~I2))(condz, condnz, z)

        condc  = Decode(2, 4)(cond) #jc
        condnc = Decode(3, 4)(cond) #jnc
        jumpc = LUT3((I0&I2)|(I1&~I2))(condc, condnc, c)

        # jump is jump always of jump cond 
        cond = Or(3)(always, jumpz, jumpc) 

        jump = And(2)(jumpinst, cond)

        wire(jump, io.jump)


class InstructionDecoder(Circuit):
    IO = ['inst',      In(Bits(16)),
          'phase',     In(Bit),
          'z',         In(Bit),
          'c',         In(Bit),

          'arith',     Out(Bit),
          'ioimm',     Out(Bit),
          'ld',        Out(Bit),
          'jump',      Out(Bit),

          'regwr',     Out(Bit),
          'zwr',       Out(Bit),
          'cwr',       Out(Bit),
          'owr',       Out(Bit)]

    @classmethod
    def definition(io):
        inst = io.inst
        phase = io.phase
        z = io.z
        c = io.c

        cond = inst[8:12]
        insttype = inst[12:16]
        insttypeop = inst[14:16]

        # alu instructions
        #logicinst = ROM2((1 << 0))(insttypeop)
        arithinst = ROM2((1 << 1))(insttypeop)
        aluinst =   ROM2((1 << 0) | (1 << 1))(insttypeop)

        # ld and st (immediate)
        ldloimminst = ROM4(1 << 8)(insttype)
        #ldhiimminst = ROM4(1 << 9)(insttype)
        ldinst =    ROM4(1 << 10)(insttype)
        stinst =    ROM4(1 << 11)(insttype)
        # make this a ROM
        ld = Or(2)(ldinst, ldloimminst)

        jump = Cond()(insttype, cond, z, c)

        regwr = LUT4((I0|I1|I2)&I3)(aluinst, ldloimminst, ldinst, phase)
        owr = And(2)(stinst, phase)

        zwr =  And(2)(aluinst, phase)
        cwr =  And(2)(arithinst, phase)

        wire(arithinst, io.arith)
        wire(ldloimminst, io.ioimm)
        wire(ld, io.ld)
        wire(jump, io.jump)

        wire(regwr, io.regwr)
        wire(zwr, io.zwr)
        wire(cwr, io.cwr)
        wire(owr, io.owr)

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
