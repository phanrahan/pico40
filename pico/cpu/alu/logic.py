import sys
from magma import *
from mantle import *
from alu import Logic
from boards.icestick import IceStick

icestick = IceStick()

icestick.Clock.on()
for i in range(6):
    icestick.J1[i].input().on()
for i in range(2):
    icestick.J3[i].output().on()

main = icestick.main()

logic = Logic(2)

logic( main.J1[0:2], main.J1[2:4], main.J1[4], main.J1[5])
wire( logic.O, main.J3 )

compile(sys.argv[1], main)

