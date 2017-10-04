def reg():
    ldlo(r0, 0x55)
    mov(r1, r0)
    st(r1)
    jmp(0)

+ reg
- connect register output to register input

wire( regaval, pico.O )

wire( pico.O, main.J3 )

