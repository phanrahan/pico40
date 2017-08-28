from magma import wire, EndCircuit
from loam.boards.icestick import IceStick
from pico40.cpu.alu import Logic

icestick = IceStick()
for i in range(6):
    icestick.J1[i].input().on()
for i in range(2):
    icestick.J3[i].output().on()

main = icestick.main()

logic = Logic(2)

logic( main.J1[0:2], main.J1[2:4], main.J1[4], main.J1[5] )
wire( logic.O, main.J3 )

EndCircuit()
