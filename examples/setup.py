from magma import *
from mantle import *
from parts.lattice.ice40.primitives.RAMB import ROMB
from pico.asm import assemble
from pico.cpu import Pico, Input, Output, ADDRN, DATAN
from boards.icestick import IceStick

__all__ = ['makepico', 'makepicoicestick']

def makepico(prog, inputs, outputs):
    mem = assemble(prog, 1 << ADDRN)

    romb = ROMB(mem)
    wire( 1, romb.RCLKE )
    wire( 1, romb.RE    )

    pico = Pico()

    wire(pico.addr, romb.RADDR)
    wire(romb.RDATA, pico.data)

    input = Input(DATAN, inputs)
    wire(pico.port, input.A)
    wire(input.O, pico.I)

    output = Output(DATAN, outputs)

    wire(pico.port, output.A)
    wire(pico.we, output.WE)
    wire(pico.O, output.I)

    return pico, romb

def makepicoicestick(prog):

    icestick = IceStick()
    icestick.Clock.on()
    for i in range(8):
        icestick.J1[i].input().on()
    for i in range(8):
        icestick.J3[i].output().on()

    main = icestick.main()

    pico, romb = makepico(prog, [main.J1], [main.J3])

    return main
