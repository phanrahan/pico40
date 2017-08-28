from .isa import *

# pseudoinstructions

def nop():
    mov(r0, r0)

def jz(pc):
    jmpc( 0x0, pc )

def jnz(pc):
    jmpc( 0x1, pc )

def jc(pc):
    jmpc( 0x2, pc )

def jnc(pc):
    jmpc( 0x3, pc )

def jmp(pc):
    jmpc( 0xf, pc )

