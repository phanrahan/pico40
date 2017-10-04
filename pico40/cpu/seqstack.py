from magma import Circuit, Clock, Bit, Bits, In, Out, \
    bits, wire, cache_definition
from mantle import Register, Add, Mux

__all__ = ['DefineSequencer', 'Sequencer']

#
# type: [DI[n], A[4], WE, INCR] -> O[n]
#
# function computes
#
# combinational
#    returns ram16[A] + INCR
#
# sequential
#    if WE: ram16[A] = DI
#
def RAM(n):

    # RAM16 + CIN
    def ram16(x, y, s, e):
        ram = RAM16(0, o=False)
        return CARRY(ram, 'CIN', 'COUT', 0, site=s, elem=e)

    #
    # Need to feed increment through COUT of the lower slice
    #
    # wire A into cy0
    # lut selects cy0
    #
    lut = LUT('A&~A', o=False, site=site, elem='Y')
    lut = CARRY(lut, None, 'COUT', 'A', o=False, site=site, elem='Y')

    c = Wire()
    lut(c)

    ram = forkjoin(col(ram16, n, site.delta(0, 1)), 'jff')
    ram.I = [ram.I + [c]]  # [DI, A, WE] + [INCR]

    wire(lut.COUT, ram.CIN)

    return ram

#
# Build an sequencer with an n-bit program counter
#
# returns [INCR, JUMP, ADDR[n], PUSH, POP] -> O[n]
#
#  combinational
#    newsp = SP+PUSH-POP
#    newpc = ADDR if JUMP else RAM[newsp]+INCR
#
#  sequential
#    RAM[newsp] = newpc
#    SP = newsp
#
#  O = newpc
#


def Sequencer(n):

    addr = Bus(n)
    incr = Wire()
    jump = Wire()
    push = Wire()
    pop = Wire()
    we = Wire()

    #
    # o=True makes the combinational output be the output of the counter
    # (rather than the register).
    #
    print 'building sp'
    newsp = UpDownCounter(4, o=True)(push, pop, ce=we)

    print 'building pc'
    PC = RAM(n)

    print 'building mux'
    newpc = Mux(2, n)([PC, addr], jump)

    print 'wiring pc'
    PC(newpc, newsp, we, incr)

    return Module([incr, jump, addr, push, pop], newpc, ce=we)

@cache_definition
def DefineSequencer(n):
    T = Bits(n)
    class _Sequencer(Circuit):
        name = 'Sequencer{}'.format(n)
        IO = ["addr", In(T), "jump", In(Bit), "we", In(Bit), "O", Out(T), "CLK", In(Clock)]

        @classmethod
        def definition(io):
            pc = Register(n, has_ce=True)
            add = Add(n)
            mux = Mux(2, n)

            add( pc, bits(1,n=n) )
            pc(mux)

            wire(add.O,   mux.I0)
            wire(io.addr, mux.I1)
            wire(io.jump, mux.S)

            wire(io.CLK, pc.CLK)
            wire(io.we, pc.CE)
            wire(pc.O, io.O)

    return _Sequencer

def Sequencer(n, **kwargs):
    return DefineSequencer(n)(**kwargs)


