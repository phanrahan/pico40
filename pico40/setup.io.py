from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from loam.boards.icestick import IceStick
from pico40 import assemble, Pico, Input, Output

__all__ = ['makepico', 'makepicoicestick']

def makepico(prog, inputs, outputs, ADDRN, DATAN):

    mem = assemble(prog, 1 << ADDRN)

    romb = ROMB(mem) # this should have a width=16
    #print(repr(romb))
    #print('ADDRN',len(romb.RADDR))
    #print('INSTN',len(romb.RDATA))
    assert len(romb.RDATA) == 16
    wire( 1, romb.RE)

    pico = Pico(ADDRN, DATAN)
    #print('ADDRN',len(pico.addr))
    #print('INSTN',len(pico.data))

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

def makepicoicestick(prog, ADDRN, DATAN):

    icestick = IceStick()
    icestick.Clock.on()
    for i in range(8):
        icestick.J1[i].input().on()
    for i in range(8):
        icestick.J3[i].output().on()

    main = icestick.main()

    pico, romb = makepico(prog, [main.J1], [main.J3], ADDRN, DATAN)

    return main
