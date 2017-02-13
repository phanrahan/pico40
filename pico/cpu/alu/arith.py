import sys
from magma import *
from mantle import *
from alu import Arith
from boards.icestick import IceStick

icestick = IceStick()

icestick.Clock.on()
for i in range(7):
    icestick.J1[i].input().on()
for i in range(3):
    icestick.J3[i].output().on()

main = icestick.main()

arith = Arith(2)

arith( main.J1[0:2], main.J1[2:4], main.J1[5], main.J1[6])
wire( main.J1[4], arith.CIN )
wire( arith.O, main.J3[0:2] )
wire( arith.COUT, main.J3[2] )

compile(sys.argv[1], main)

