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


class InstructionDecoder(Circuit):
    IO = ['inst',      In(Bits(16)),
          'phase',     In(Bit),
          'z',         In(Bit),

          'arith',     Out(Bit),
          'ioimm',     Out(Bit),
          'ld',        Out(Bit),
          'jump',      Out(Bit),
          'regwr',     Out(Bit),
          'zwr',       Out(Bit),
          #'cwr',       Out(Bit),
          'owr',       Out(Bit)]
    @classmethod
    def definition(io):
        inst = io.inst
        phase = io.phase
        z = io.z

        insttype = inst[14:16]
        #fullinsttype = inst[12:14]
        cc = inst[8:12]

        # alu instructions
        logicinst = ROM2((1 << 0))(insttype)
        arithinst = ROM2((1 << 1))(insttype)
        aluinst =   ROM2((1 << 0) | (1 << 1))(insttype)

        # ld and st (immediate)
        ldloimminst = ROM4(1 << 8)(inst[12:16])
        #ldhiimminst = ROM4(1 << 9)(inst[12:16])
        ldinst =    ROM4(1 << 10)(inst[12:16])
        stinst =    ROM4(1 << 11)(inst[12:16])
        # make this a ROM
        ld = Or(2)(ldinst, ldloimminst)

        # control flow instructions
        jumpinst = ROM4(1 << 12)(inst[12:16])
        #callinst = ROM4(1 << 13)(inst[12:16])
        #retinst = ROM4(1 << 14)(inst[12:16])

        always = Decode(15, 4)(cc)

        condz  = Decode(0, 4)(cc) #jz
        condnz = Decode(1, 4)(cc) #jnz
        jumpz = LUT3((I0&I2)|(I1&~I2))(condz, condnz, z)

        # jump is jump always of jump cond 
        cond = Or(2)(always, jumpz) 

        jump = And(2)(jumpinst, cond)

        regwr = LUT4((I0|I1|I2)&I3)(aluinst, ldloimminst, ldinst, phase)
        zwr =  And(2)(aluinst, phase)
        owr = And(2)(stinst, phase)

        #wire(logicinst, io.logicinst)
        wire(arithinst, io.arith)
        #wire(aluinst, io.aluinst)
        #wire(ldloinst, io.ldloinst)
        wire(ldloimminst, io.ioimm)
        wire(ld, io.ld)
        wire(jump, io.jump)
        wire(regwr, io.regwr)
        wire(zwr, io.zwr)
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

    # romb's output is registered
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

    print('Building condition code registers')
    z = DFF(has_ce=True)

    print('Building instruction decoder')
    arith, ioimm, ld, jump, \
    regwr, zwr, owr = \
        InstructionDecoder()(inst, phase, z)

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
    res = alu(raval, rbval, op, arith)

    regiomux = Mux(2, N)
    regiomux(I, imm, ioimm)  

    regimux = Mux(2, N)
    regimux(res, regiomux, ld) 

    regfile(ra, rb, ra, regimux, regwr)

    # z flag

    zval0 = Decode(0, N//2)(res[0:N//2])
    zval1 = Decode(0, N//2)(res[N//2:N])
    z(And(2)(zval0,zval1), CE=zwr)

    wire(imm, pico.port)
    wire(raval, pico.O)
    wire(owr, pico.we)
    wire(pc, pico.addr)

    EndCircuit()

    return pico

def Pico(ADDRN, DATAN, debug=False, **kwargs):
    return DefinePico(ADDRN, DATAN, debug=debug)(**kwargs)
