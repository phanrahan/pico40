from magma import *
from mantle import *

__all__  = ['DefineRAM', 'RAM']
__all__ += ['DefineROM', 'ROM']

def REGs(n, width):
    return [Register(width, has_ce=True) for i in range(n)]

def MUXs(n, width):
    return [Mux(2,width) for i in range(n)]

def readport(logn, width, regs, raddr):
    n = 1 << logn

    muxs = MUXs(n-1, width)
    for i in range(n//2):
        muxs[i](regs[2*i], regs[2*i+1], raddr[0])

    k = 0
    l = 1 << (logn-1)
    for i in range(logn-1):
        for j in range(l//2):
            muxs[k+l+j](muxs[k+2*j], muxs[k+2*j+1], raddr[i+1])
        k += l
        l //= 2

    return muxs[n-2]

def writeport(logn, width, regs, WADDR, I, WE):
    n = 1 << logn

    decoder = Decoder(logn)
    enable = And(2,1<<logn)
    enable(decoder(WADDR), repeat(WE, n))

    for i in range(n):
        regs[i](I, CE=enable.O[i])

@cache_definition
def DefineRAM(logn, width):
    n = 1 << logn
    TADDR = Bits(logn)
    TDATA = Bits(width)

    class _RAM(Circuit):
        name = 'RAM{}x{}'.format(n,width)
        IO = ['RADDR', In(TADDR),
              'RDATA', Out(TDATA),
              'WADDR', In(TADDR),
              'WDATA', In(TDATA),
              'CLK', In(Clock),
              'WE', In(Bit)]

        @classmethod
        def definition(io):
            regs = REGs(n, width)
            writeport(logn, width, regs, io.WADDR, io.WDATA, io.WE)
            rdata = readport(logn, width, regs, io.RADDR)
            wire(rdata, io.RDATA)

    return _RAM

def RAM(height, width):
    return DefineRAM(height, width)()


@cache_definition
def DefineDualRAM(logn, width):
    n = 1 << logn
    TADDR = Bits(logn)
    TDATA = Bits(width)

    class _DualRAM(Circuit):
        name = 'DualRAM{}x{}'.format(n,width)
        IO = ['RADDR0', In(TADDR),
              'RDATA0', Out(TDATA),
              'RADDR1', In(TADDR),
              'RDATA1', Out(TDATA),
              'WADDR', In(TADDR),
              'WDATA', In(TDATA),
              'CLK', In(Clock),
              'WE', In(Bit)]

        @classmethod
        def definition(io):
            regs = REGs(n, width)
            writeport(logn, width, regs, io.WADDR, io.WDATA, io.WE)
            rdata0 = readport(logn, width, regs, io.RADDR0)
            wire(rdata0, io.RDATA0)
            rdata1 = readport(logn, width, regs, io.RADDR1)
            wire(rdata1, io.RDATA1)

    return _DualRAM

def DualRAM(height, width):
    return DefineDualRAM(height, width)()

