from ctypes import Union
from enum import Enum


MAXRESERVED = 14
FALSE = 0
TRUE = 1
linepos = 0
lineno = 0
EchoSource = None
MAXCHILDREN=3

class TokenType(Enum):
    ENDFILE=0
    ERROR=1

    IF=2
    THEN=3
    ELSE=4
    END=5
    REPEAT=6
    UNTIL=7
    MAIN=8
    DO=9
    WHILE=10
    CIN=11
    COUT=12
    BOOLEAN=13
    INT=14
    REAL=15
    
    ID=16
    NREAL=17
    ENTERO=18
    
    SUMA=19
    RESTA=20
    MULTI=21
    DIV=22
    RES=23
    MENOR=24
    MENOREQ=25
    MAYOR=26
    MAYOREQ=27
    IGUALDAD=28
    DIFERENTEDE=29
    ASIGNACION=30
    PARENIZQ=31
    PARENDERE=32
    LLAVEDER=33
    LLAVEIZQ=34 
    PLUSPLUS=35
    MENOSMENOS=36
    COMA=37
    PUNTOCOMA=38
    COMMENT=39
    MULTICOMMENT=40


    
class NodoKind(Enum):
    STKD=1
    EXPD=2
    DEKD=3


class SentenciaKind(Enum):
    IFKD=1
    WHILEKD=2
    DOKD=3
    UNTILKD=4
    CINKD=5
    COUTKD=6
    ASIGKD=7
    ASIGPREKD=8
    ASIGPOSTKD=9
    MAINKD=10
    DECKD=11
    TYPEDEFIKD=12
    LISTAIDKD=13
    ELSEKD=14

class ExpresionKind(Enum):
    OPERKD=1
    CONSTKD=2
    CONSTFKD=3
    IDKD=4

class DeclaracionKind(Enum):
    INTKD=1
    REALKD=2
    BOOLEANKD=3
    VOIDKD=4

class TreeNode:
    def __init__(self,lineno,nodoKind,kind) -> None:
        self.child:list = [None]*MAXCHILDREN
        self.sibling:TreeNode = None
        self.lineno:int = lineno
        self.nodeKind:NodoKind = nodoKind
        self.kind:Union[SentenciaKind, ExpresionKind] = kind
        self.attr:Union[TokenType,int,float,str] = ""
        self.type:DeclaracionKind = -1

    def getChild(self,pos)->list:
        return self.child[pos]
    def setChild(self,child,pos)->None:
        self.child.insert(pos,child) 
    def getSibling(self):
        return self.sibling
    def setSibling(self,sibling)->None:
        self.sibling=sibling
    def getType(self)->DeclaracionKind:
        return self.type
    def setType(self,type:DeclaracionKind)->None:
        self.type=type
    def getAttr(self):
        return self.attr
    def setAttr(self,attr)->None:
        self.attr=attr
    def getNodeKind(self)->NodoKind:
        return self.nodeKind
    def getKind(self):
        return self.kind
