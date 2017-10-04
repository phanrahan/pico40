def ldloprog():
    ldlo(r0, 0x55)
    ldlo(r0, 0xaa)
    jmp(0)

+io
- add io.O

wire( imm, pico.O )

wire( pico.O, main.J3 )

