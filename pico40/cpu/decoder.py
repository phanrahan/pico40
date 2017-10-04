from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from ..mem import read as readmem
from .seq import Sequencer
from .alu import ALU
from .cond import Cond

def ROM2(x):
    return uncurry(LUT2(x))

def ROM4(x):
    return uncurry(LUT4(x))


class InstructionDecoder(Circuit):
    IO = ['inst',      In(Bits(16)),
          'phase',     In(Bit),
          'z',         In(Bit),
          'c',         In(Bit),

          'arithinst', Out(Bit),
          'imminst',   Out(Bit),
          'ioinst',    Out(Bit),
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

        regwr = LUT3((I0|I1)&I2)(aluinst, ld, phase)

        zwr =  And(2)(aluinst, phase)
        cwr =  And(2)(arithinst, phase)

        owr = And(2)(stinst, phase)

        wire(arithinst, io.arithinst)
        wire(ldloimminst, io.imminst)
        wire(ldinst, io.ioinst)

        wire(jump, io.jump)

        wire(regwr, io.regwr)
        wire(zwr, io.zwr)
        wire(cwr, io.cwr)
        wire(owr, io.owr)
