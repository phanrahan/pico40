from magma import wire, EndCircuit
from loam.boards.icestick import IceStick
from pico40.cpu.alu import Arith

icestick = IceStick()
for i in range(7):
    icestick.J1[i].input().on()
for i in range(3):
    icestick.J3[i].output().on()

main = icestick.main()

arith = Arith(2)

arith( main.J1[0:2], main.J1[2:4], main.J1[5], main.J1[6], main.J1[4] )
wire( arith.O, main.J3[0:2] )
wire( arith.COUT, main.J3[2] )

EndCircuit()


