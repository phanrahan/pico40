from magma import *
from mantle import *
from mantle.lattice.ice40 import ROMB
from loam.boards.icestick import IceStick
from pico40 import assemble, Pico

__all__ = ['makepico', 'makepicoicestick']

def makepico(prog, input, output, ADDRN, DATAN, debug):

    mem = assemble(prog, 1 << ADDRN)

    romb = ROMB(len(mem), 16, mem) # this should have a width=16
    #print(repr(romb))
    #print('ADDRN',len(romb.RADDR))
    #print('INSTN',len(romb.RDATA))
    assert len(romb.RDATA) == 16
    wire( 1, romb.RE)

    pico = Pico(ADDRN, DATAN, debug)
    #print('ADDRN',len(pico.addr))
    #print('INSTN',len(pico.data))

    wire(pico.addr, romb.RADDR)
    wire(romb.RDATA, pico.data)

    #input = Input(DATAN, inputs)
    #wire(pico.port, input.A)
    #wire(input.O, pico.I)
    wire(input, pico.I)

    if debug is None:
        #output = Output(DATAN, outputs)
        #wire(pico.port, output.A)
        reg = Register(DATAN, has_ce=True)
        reg(pico.O, ce=pico.we)
        wire(reg.O, output)
    else:
        wire(pico.O, output)

    return pico, romb

def makepicoicestick(prog, ADDRN, DATAN, debug=None):

    icestick = IceStick()
    icestick.Clock.on()
    for i in range(8):
        icestick.J1[i].input().on()
    for i in range(8):
        icestick.J3[i].output().on()

    main = icestick.main()

    pico, romb = makepico(prog, main.J1, main.J3, ADDRN, DATAN, debug)

    return main
