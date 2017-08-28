from .util import checku
from .asm import emit

def mov ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x0 | (a<<8) | (b<<4) )

def and_ ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x1000 | (a<<8) | (b<<4) )

def or_ ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x2000 | (a<<8) | (b<<4) )

def xor ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x3000 | (a<<8) | (b<<4) )

def add ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x4000 | (a<<8) | (b<<4) )

def sub ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x5000 | (a<<8) | (b<<4) )

def adc ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x6000 | (a<<8) | (b<<4) )

def sbc ( a, b ):
    a = checku ( a , 4 )
    b = checku ( b , 4 )
    emit( 0x7000 | (a<<8) | (b<<4) )

def ldlo ( a, i ):
    a = checku ( a , 4 )
    i = checku ( i , 8 )
    emit( 0x8000 | (a<<8) | (i<<0) )

def ldhi ( a, i ):
    a = checku ( a , 4 )
    i = checku ( i , 8 )
    emit( 0x9000 | (a<<8) | (i<<0) )

def ld ( a, i ):
    a = checku ( a , 4 )
    i = checku ( i , 8 )
    emit( 0xa000 | (a<<8) | (i<<0) )

def st ( a, i ):
    a = checku ( a , 4 )
    i = checku ( i , 8 )
    emit( 0xb000 | (a<<8) | (i<<0) )

def jmpc ( c, i ):
    c = checku ( c , 4 )
    i = checku ( i , 8 )
    emit( 0xc000 | (c<<8) | (i<<0) )

def callc ( c, i ):
    c = checku ( c , 4 )
    i = checku ( i , 8 )
    emit( 0xd000 | (c<<8) | (i<<0) )

def retc ( c ):
    c = checku ( c , 4 )
    emit( 0xe000 | (c<<8) )

r0 = 0
r1 = 1
r2 = 2
r3 = 3
r4 = 4
r5 = 5
r6 = 6
r7 = 7
r8 = 8
r9 = 9
r10 = 10
r11 = 11
r12 = 12
r13 = 13
r14 = 14
r15 = 15
