from enum import Enum


MAXRESERVED = 8
FALSE = 0
TRUE = 1
linepos = 0
lineno = 0
EchoSource = None

class TokenType(Enum):
    ENDFILE=1
    ERROR=2

    IF=3
    THEN=4
    ELSE=5
    END=6
    REPEAT=7
    UNTIL=8
    MAIN=9
    DO=10
    WHILE=11
    CIN=12
    COUT=13
    BOOLEAN=14
    INT=15
    REAL=16
    
    ID=17
    NREAL=18
    ENTERO=19
    
    SUMA=20
    RESTA=21
    MULTI=22
    DIV=23
    RES=24
    MENOR=25
    MENOREQ=26
    MAYOR=27
    MAYOREQ=27
    IGUALDAD=28
    DIFERENTEDE=29
    ASIGNACION=30
    PARENIZQ=31
    PARENDERE=32
    LLAVEIZQ=33
    LLAVEDER=34
    PLUSPLUS=35
    MENOSMENOS=36
    COMA=37
    PUNTOCOMA=38
    COMMENT=39
    MULTICOMMENT=40


    
