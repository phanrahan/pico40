from magma import *
from mantle import *

__all__  = ['DefineLogic', 'Logic']
__all__ += ['DefineArith', 'Arith']
__all__ += ['DefineALU', 'ALU']

@cache_definition
def DefineLogic(n):

    T = Bits(n)
    class _Logic(Circuit):
        name = 'Logic{}'.format(n)
        IO = ["A",  In(T),
              "B",  In(T),
              "S0", In(Bit),
              "S1", In(Bit),
              "O",  Out(T)]
        @classmethod
        def definition(io):
            def logic(y):

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

                return LUT4(logicfunc)

            logic = braid(col(logic, n), joinargs=['I0', 'I1'], forkargs=['I2', 'I3'])
            wire(io.A, logic.I0)
            wire(io.B, logic.I1)
            wire(io.S0, logic.I2)
            wire(io.S1, logic.I3)
            wire(logic.O, io.O)

    return _Logic

def Logic(n, **kwargs):
    return DefineLogic(n)(**kwargs)


#
#  [A[n], B[n], SUB, CARRY, CIN] -> C[n], COUT
#
@cache_definition
def DefineArith(n):

    T = Bits(n)
    class _Arith(Circuit):
        name = 'Arith{}'.format(n)
        IO = ["A",     In(T),
              "B",     In(T),
              "SUB",   In(Bit),
              "CARRY", In(Bit),
              "CIN",   In(Bit),
              "O",     Out(T),
              "COUT",  Out(Bit)]
        @classmethod
        def definition(io):
            inv = Invert(n)
            mux = Mux(2,n)
            add = Add(n, True, True)

            # 
            # compute carry in to the adder
            #
            #        CAR SUB CIN CIN'
            #  ADD     0   0   0   0
            #  ADD     0   0   1   0
            #  SUB     0   1   0   1
            #  SUB     0   1   1   1
            #  ADDC    1   0   0   0
            #  ADDC    1   0   1   1
            #  SUBC    1   1   0   1
            #  SUBC    1   1   1   0
            #
            truth = [0, 0, 1, 1, 0, 1, 1, 0]
            cin = LUT3(truth)(io.CIN, io.SUB, io.CARRY)

            wire( io.B, inv.I )

            wire( io.B,   mux.I0 )
            wire( inv.O,  mux.I1 )
            wire( io.SUB, mux.S )

            wire( io.A,  add.I0 )
            wire( mux.O, add.I1 )
            wire( cin  , add.CIN )
            wire( add.O, io.O )
            wire( add.COUT, io.COUT )

    return _Arith

def Arith(n, **kwargs):
    return DefineArith(n)(**kwargs)


@cache_definition
def DefineALU(n):
    T = Bits(n)
    class _ALU(Circuit):
        name = 'ALU{}'.format(n)
        IO = ["A", In(T), 
              "B", In(T),
              "CIN", In(Bit),
              "op", In(Bits(2)),
              "insttype", In(Bit),
              "O", Out(T), 
              "COUT", Out(Bit)]

        @classmethod
        def definition(io):
            #print('Building logic unit')
            logicunit = Logic(n)

            #print('Building arith unit')
            arithunit = Arith(n)

            #print('Building alu mux')
            mux = Mux(2, n)

            #print('Wiring logic unit')
            logicunit(io.A, io.B, io.op[0], io.op[1])

            #print('Wiring arith unit')
            arithunit(io.A, io.B, io.op[0], io.op[1], io.CIN) # CIN=0

            #print('Wiring alumux')
            res = mux(logicunit.O, arithunit.O, io.insttype)
            wire( res, io.O )
            wire( arithunit.COUT, io.COUT)

    return _ALU

def ALU(n, **kwargs):
    return DefineALU(n)(**kwargs)

