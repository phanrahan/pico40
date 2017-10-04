# mov.py
# and.py
# or.py
# xor.py
# add.py
# sub.py

# and.py
#def prog():
#    ldlo(r0, 0x55)
#    ldlo(r1, 0x0f)
#    and_(r1, r0)
#    st(r1, 0)
#    jmp(0)

# count.py
def prog():
    ldlo(r0,0)
    ldlo(r1,1)
    loop = label()
    add(r0,r1)
    st(r0, 0)
    jmp(loop)

+alu

wire( pico.O, main.J3 )
