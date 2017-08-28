from magma import Circuit, Clock, Bit, Bits, In, Out, \
    bits, wire, cache_definition
from mantle import Register, Add, Mux

__all__ = ['DefineSequencer', 'Sequencer']

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

