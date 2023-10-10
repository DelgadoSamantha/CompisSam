import globals
from globals import TokenType as tokp

from globals import TreeNode,ExpresionKind,SentenciaKind,DeclaracionKind,NodoKind

def newStmtNode(kind:SentenciaKind)->TreeNode:
    tr=TreeNode(globals.lineno,NodoKind.STKD,kind)
    return tr

def newExpNode(kind:ExpresionKind)->TreeNode:
    tr=TreeNode(globals.lineno,NodoKind.EXPD,kind)
    return tr


def creacionarbol(raiz:TreeNode)->dict:
    if(raiz is None):
        return None
    return{
        "valor":raiz.getAttr(),
        "nodoKind":raiz.getNodeKind().value,
        "kind":raiz.getKind(),
        "type":raiz.getType(),
        "firstChild":creacionarbol(raiz.getChild(0)),
        "secondChild":creacionarbol(raiz.getChild(1)),
        "thirdChild":creacionarbol(raiz.getChild(2)),
        "sibling":creacionarbol(raiz.getSibling())
    }
    