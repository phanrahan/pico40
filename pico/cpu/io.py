from magma import *
from mantle import *

__all__ = ['Input', 'Output']

def Input(N, inputs):

    A = In(Array(N, Bit))()
    n = len(inputs)
    if   n == 1:
        O = inputs[0]
    elif n == 2:
        mux = Mux(2, N)
        mux(inputs[0], inputs[1], A[0])
        O = mux.O
    elif n == 4:
        mux = Mux(4, N)
        mux(inputs[0], inputs[1], inputs[2], inputs[3], A[0:2])
        O = mux.O
    elif n == 8:
        mux = Mux(8, N)
        mux(inputs[0], inputs[1], inputs[2], inputs[3],
            inputs[4], inputs[5], inputs[6], inputs[7], A[0:3])
        O = mux.O

    return AnonymousCircuit("A", A, "O", O)


#
# Generate a register with the same number of bits as the output
#
def OutputOne(input, output, we):
    reg = Register(8, ce=True)
    reg(input, ce=we)
    wire(reg, output)

def Output(N, outputs):

    I = In(Array(N, Bit))()
    A = In(Array(N, Bit))()
    we = In(Bit)()

    if len(outputs) == 1:
        OutputOne(I, outputs[0], we)
    else:
        for output in outputs:
            en = Decode(i, N)(A)
            en = And2()(en, we)
            OutputOne(I, output, en)

    return AnonymousCircuit("A", A, "I", I, "WE", we )

