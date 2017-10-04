def jmpprog():
    mov(r0,r0)
    jmp(0)

def aluprog():
    MAXINSTS = 1 << ADDRN
    for i in range(MAXINSTS/8):
        mov (r0, r0)
        and_(r0, r0)
        or_ (r0, r0)
        xor (r0, r0)
        add (r0, r0)
        sub (r0, r0)
        adc (r0, r0)
        sbc (r0, r0)

remove cond, reg, alu, io

debugmux = Mux(2,8)
wire( debugmux( pc, inst[8:16], phase ), pico.debug )

wire( pico.debug, main.J3 )
