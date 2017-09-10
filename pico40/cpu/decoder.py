from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from ..mem import read as readmem
from .seq import Sequencer
from .alu import ALU
from .ram import DualRAM
from .cond import Cond

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
