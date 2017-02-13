from magma import *
from mantle import Register, Add, Mux

__all__ = ['Sequencer']

def Sequencer(n):

    pc = Register(n, ce=True)

    add = Add(n)

    add( pc, constarray(1,n) )

    mux = Mux(2, n)

    wire(add.O, mux.I0)

    pc(mux)

    return AnonymousCircuit("addr", mux.I1, 
                            "jump", mux.S,
                            "we",   pc.CE,
                            "O",   pc.O)
               


if __name__ == '__main__':

    import sys
    from mem import read
    from parts.lattice.ice40.primitives.RAMB import ROMB
    from mantle import TFF
    from boards.icestick import IceStick

    icestick = IceStick()

    icestick.Clock.on()
    #for i in range(8):
    #    icestick.J1[i].input().on()
    for i in range(8):
        icestick.J3[i].output().on()

    main = icestick.main()

    ADDRN = 8
    INSTN = 16
    DATAN = 8

    mem = read('a.mem')
    mem += (256-len(mem))*[0]
    print len(mem)
    
    # program memory
    romb = ROMB(mem)
    print romb.interface
    wire( 1, romb.RE    )
    wire( 1, romb.RCLKE )
    inst = romb.RDATA
    
    # instruction decode
    addr = inst[0:ADDRN]
    imm = inst[0:DATAN]
    rb = inst[4:8]
    ra = inst[8:12]
    cc = inst[8:12]
    op = inst[12:16]
    insttype = inst[14:16]
    jump = inst[15]

    tff = TFF()
    tff(1)

    seq = Sequencer(8)

    pc = seq(addr, jump, tff)
    wire( pc, romb.RADDR )

    wire(pc, main.J3)

    compile(sys.argv[1], main)

