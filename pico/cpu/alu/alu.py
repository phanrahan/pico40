from magma import *
from mantle import *

__all__ = ['Logic', 'Arith']

def logicfunc(A, B, S0, S1):
    if S1 == 0:
        if S0 == 0:
            return B
        else:
            return A&B
    else:
        if S0 == 0:
            return A|B
        else:
            return A^B

def Logic(n):

    def logic(y):
        return LUT4(logicfunc)

    return braid(col(logic, n), joinargs=['I0', 'I1'], forkargs=['I2', 'I3'])


#
#  [A[n], B[n], SUB, CARRY, CIN] -> C[n], COUT
#
def Arith(n):

    A = In(Array(n, Bit))()
    B = In(Array(n, Bit))()
    SUB = In(Bit)()
    CARRY = In(Bit)()
    CIN = In(Bit)()

    inv = Invert(n)
    wire( B, inv )

    mux = Mux(2,n)
    wire(   B, mux.I0 )
    wire( inv, mux.I1 )
    wire( SUB, mux.S )

    add = AddC(n)
    wire(  A, add.I0 )
    wire(mux, add.I1)

    #        CAR SUB CIN CIN'
    #  ADD     0   0   0   0
    #  ADD     0   0   1   0
    #  SUB     0   1   0   1
    #  SUB     0   1   1   1
    #  ADDC    1   0   0   0
    #  ADDC    1   0   1   1
    #  SUBC    1   1   0   1
    #  SUBC    1   1   1   0
    truth = [0, 0, 1, 1, 0, 1, 1, 0]
    cin = LUT3(truth)(CIN, SUB, CARRY)
    wire(cin, add.CIN)

    return AnonymousCircuit("A",     A,
                            "B",     B,
                            "SUB",   SUB,
                            "CARRY", CARRY,
                            "CIN",   CIN,
                            "O",     add.O,
                            "COUT",  add.COUT)

