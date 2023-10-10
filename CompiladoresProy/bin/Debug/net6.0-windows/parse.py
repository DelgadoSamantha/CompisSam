from globals import TokenType 
from nltk.tree import Tree
from globals import TreeNode
from globals import SentenciaKind, ExpresionKind, DeclaracionKind, NodoKind
from util import newStmtNode,newExpNode
import json

MAXCHILDREN = 3

global palabras
global indice
#archivo='testSintaxis.txt'
indice=0
tkstrg=''
#raiz=Tree('PROGRAMA',[])
raiz:TreeNode = None
token=-1
source = open('archToken.txt','r')
lineno=0
colpos=0

def obtener_siguiente_linea():
    with open('archToken.txt', "r") as archivo:
        lineas = archivo.readlines()
        obtener_siguiente_linea.indice += 1  # Variable estática para rastrear el índice
 
        if obtener_siguiente_linea.indice <= len(lineas):
            return lineas[obtener_siguiente_linea.indice - 1].strip()
        else:
            return None
 
# Inicializar la variable estática
obtener_siguiente_linea.indice = 0
 
def getTokenSintactico():
    global tkstrg
    linea = obtener_siguiente_linea()
    if linea is not None:
        palabras = linea.split('\t')
        palabras = [palabra.replace("\n","") for palabra in palabras]
        print("Token -->  "+palabras[0])
        print("TokenString -->  "+palabras[1])
        print("Linea -->  "+palabras[2])
        print("Columna -->  "+palabras[3])
        #print(linea)
        print("\n-------------------------------")
        tkstrg = palabras[1]
        a = palabras[0]
        if(palabras[0] == 'PALABRARESERVADA'):
           a = TokenType[palabras[1].upper()].value 
        else:
            a = TokenType[a.upper()].value 
        return a  
    else:
        return TokenType.ENDFILE.value

""" def lista_declaracion()->Tree:
    global token
    tr=Tree('LISTA_DECLARACION',[])
    #pd=tr.append(declaracion())
    pd=tr.extend(declaracion())

    while( token != TokenType.ENDFILE.value 
        and token != TokenType.ELSE.value
        and token != TokenType.UNTIL.value 
        and token != TokenType.END.value
        and token !=TokenType.LLAVEDER.value): #llave o parentesis? RBPAREN
        #match(TokenType.PUNTOCOMA.value)
        dec = declaracion()
        #tr.append(dec)
        tr.extend(dec) 
    if(len(tr)==0):
        tr=Tree('',[])  
    return tr
    

def declaracion_variable()->Tree:
    global token
    global tkstrg
    tr=Tree('DECLARACION_VARIABLE',[])
    tr2=Tree('DECLARACION_VARIABLE',[])
   
    if(token==TokenType.REAL.value):
        tr2.append(Tree(str(TokenType.REAL.name),[]))
        match(TokenType.REAL.value)
    elif(token==TokenType.INT.value):
        tr2.append(Tree(str(TokenType.INT.name),[]))
        match(TokenType.INT.value)
    elif(token==TokenType.BOOLEAN.value):
        tr2.append(Tree(str(TokenType.BOOLEAN.name),[]))
        match(TokenType.BOOLEAN.value)
    else:
        #sintaxError('Unknown Data')
        token=getTokenSintactico()
    tr2.append(lista_identificadores())
    if(token== TokenType.PUNTOCOMA.value):
        match(TokenType.PUNTOCOMA.value)
    else:
        #sintaxError("Unknow Token "+tkstrg)
        pass
    tr.append(tr2)
    #match(TokenType.PUNTOCOMA.value)
    return tr

def declaracion()->Tree:
    global token
    tr=Tree('',[])

    if(token==TokenType.REAL.value or token==TokenType.INT.value or token==TokenType.BOOLEAN.value):
        tr=declaracion_variable()
    else:
        tr=lista_sentencias()
    return tr

def lista_sentencias()->Tree:
    global token
    global tkstrg
    tr=Tree('LISTA_SENTENCIAS',[])

    if(token==TokenType.IF.value 
        or token==TokenType.DO.value
        or token==TokenType.WHILE.value
        or token==TokenType.CIN.value 
        or token==TokenType.COUT.value 
        or token==TokenType.ID.value
        or token==TokenType.MAIN.value
        or token==TokenType.PLUSPLUS.value
        or token==TokenType.MENOSMENOS.value):
        tr=Tree('LISTA_SENTENCIAS',[])
        while(token==TokenType.IF.value 
            or token==TokenType.DO.value
            or token==TokenType.WHILE.value
            or token==TokenType.CIN.value 
            or token==TokenType.COUT.value 
            or token==TokenType.ID.value
            or token==TokenType.MAIN.value
            or token==TokenType.PLUSPLUS.value
            or token==TokenType.MENOSMENOS.value):
                tr.append(sentencias())
    else:
        tr=Tree('',[])
        #sintaxError("Unknow Token "+tkstrg)
        token=getTokenSintactico()
    return tr

def lista_identificadores():
    global token
    global tkstrg
    tr=Tree('',[])
    if(token==TokenType.ID.value):
        tr=Tree('VAR',[])
        tr.append(Tree(tkstrg,[]))
        match(TokenType.ID.value)
        while(token==TokenType.COMA.value):
            match(TokenType.COMA.value)
            if(token==TokenType.ID.value):
                tr.append(Tree(tkstrg,[]))
                match(TokenType.ID.value)
    
    return tr


def sentencias()->Tree:
    global token
    global tkstrg
    tr=Tree('',[])

    if(token==TokenType.IF.value):
        tr=sentencia_if()
    elif(token==TokenType.DO.value):
        tr=sentencia_do()
    elif(token==TokenType.WHILE.value):
        tr=sentencia_while()
    elif(token==TokenType.CIN.value):
        tr=sentencia_cin()
    elif(token==TokenType.COUT.value):
        tr=sentencia_cout()
    elif(token==TokenType.ID.value 
        or token==TokenType.PLUSPLUS.value
        or token==TokenType.MENOSMENOS.value):
        tr=sentencia_asignaciongeneral()
    elif(token==TokenType.MAIN.value):
        tr=sentencia_main()
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        token=getTokenSintactico()
    return tr

def sentencia_if()->Tree:
    global token
    tr=Tree('IF',[])
    match(TokenType.IF.value)
    tr.append(expresion())
    tr.extend(lista_declaracion())
    if(token==TokenType.ELSE.value):
        match(TokenType.ELSE.value)
        els=Tree('ELSE',[])
        els.extend(lista_declaracion())
        tr.append(els)
    match(TokenType.END.value)
    return tr

def sentencia_do()->Tree:
    global token
    tr=Tree('DO',[])
    match(TokenType.DO.value)
    tr.append(lista_declaracion())
    match(TokenType.UNTIL.value)
    tr.append(expresion())
    match(TokenType.PUNTOCOMA.value)
    return tr

def sentencia_while()->Tree:
    global token
    tr=Tree('WHILE',[])
    match(TokenType.WHILE.value)
    tr.append(expresion())
    match(TokenType.LLAVEIZQ.value)
    tr.extend(lista_declaracion())
    match(TokenType.LLAVEDER.value)
    return tr

def sentencia_cin()->Tree:
    global token
    global tkstrg
    tr=Tree('CIN',[])
    match(TokenType.CIN.value)
    if(token==TokenType.ID.value):
        tr.append(Tree(tkstrg,[]))
    match(TokenType.ID.value)
    match(TokenType.PUNTOCOMA.value)
    return tr

def sentencia_cout()->Tree:
    global token
    tr=Tree('COUT',[])
    match(TokenType.COUT.value)
    tr.append(expresion())
    match(TokenType.PUNTOCOMA.value)
    return tr

def sentencia_asignaciongeneral()->Tree:
    global token
    global tkstrg
    tr=Tree('ASIGNACION',[])
    if(token==TokenType.MENOSMENOS.value
       or token==TokenType.PLUSPLUS.value):
        tr.extend(asignacion_prefijo())
    elif (token==TokenType.ID.value):
        tr.extend(asignacion_sencilla())
    return tr

def asignacion_prefijo()->Tree:
    global tkstrg
    global token
    tr=Tree('ASIGNACION',[])
    tr.append(Tree(tkstrg,[]))
    match(token)
    if(token==TokenType.ID.value):
        tr[0].append(Tree(tkstrg,[]))
        match(TokenType.ID.value)
        match(TokenType.PUNTOCOMA.value)
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        token=getTokenSintactico()
    return tr


def asignacion_postfijo()->Tree:
    global tkstrg
    global token
    tr=Tree('ASIGNACION',[])
    tr.append(Tree(tkstrg,[]))
    match(token)
    if(token==TokenType.MENOSMENOS.value
       or token==TokenType.PLUSPLUS.value):
        tr[0].append(Tree(tkstrg,[]))
        match(token)
        match(TokenType.PUNTOCOMA.value)
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        token=getTokenSintactico()
    return tr

def asignacion_sencilla()->Tree:
    global tkstrg
    global token
    tr=Tree('ASIGNACION',[])
    #tr.append(Tree(tkstrg,[]))
    #match(token)
    if(token==TokenType.ID.value):
        tr.append(Tree(tkstrg,[]))
    match(TokenType.ID.value)
    if(token==TokenType.ASIGNACION.value):
        match(TokenType.ASIGNACION.value)
        tr.extend(sentencia_exp())
    elif(token==TokenType.MENOSMENOS.value
        or token==TokenType.PLUSPLUS.value):
        tr.extend(asignacion_postfijo())
    else:
        tr.append(Tree('',[]))
    return tr


def sentencia_main()->Tree:
    tr=Tree('MAIN',[])
    match(TokenType.MAIN.value)
    match(TokenType.LLAVEIZQ.value)
    tr.extend(lista_declaracion())
    match(TokenType.LLAVEDER.value)
    return tr


def sentencia_exp()->Tree:
    global token
    tr=Tree('SENTENCIA_EXPRESION',[])
    if(token==TokenType.PUNTOCOMA.value):
        tr.append(Tree(';',[]))
        match(TokenType.PUNTOCOMA.value)
    else:
        tr.append(expresion())
        match(TokenType.PUNTOCOMA.value)
    return tr

def expresion()->Tree:
    global token
    global tkstrg
    tr=expresion_simple()
    if((token==TokenType.IGUALDAD.value)
       or (token==TokenType.DIFERENTEDE.value)
       or (token==TokenType.MAYOR.value)
       or (token==TokenType.MAYOREQ.value)
       or (token==TokenType.MENOR.value)
       or (token==TokenType.MENOREQ.value)):
        pd=Tree(tkstrg,[])
        pd.append(tr)
        tr=pd
        match(token)
        tr.append(expresion_simple())
    return tr


def termino()->Tree:
    global token
    tr=factor()
    while(token==TokenType.MULTI.value or token==TokenType.DIV.value or token==TokenType.RES.value):
        pd=Tree(tkstrg,[])
        pd.append(tr)
        tr=pd
        match(token)
        pd.append(factor())
    return tr
   
def expresion_simple()->Tree:
    global token
    global tkstrg
    tr=termino()
    while((token==TokenType.SUMA.value) 
        or (token==TokenType.PLUSPLUS.value) 
        or (token==TokenType.RESTA.value)
        or (token==TokenType.MENOSMENOS.value)):
        pd=Tree(tkstrg,[])
        pd.append(tr)
        tr=pd
        match(token)
        pd.append(termino())
    return tr

def factor()->Tree:
    global token
    global tkstrg
    tr=Tree('',[])

    if(token==TokenType.ID.value):
        tr=Tree('ID',[])
        tr.append(Tree(tkstrg,[]))
        match(TokenType.ID.value)
    elif(token==TokenType.ENTERO.value):
        tr=Tree('ENTERO',[])
        tr.append(Tree(tkstrg,[]))
        match(TokenType.ENTERO.value)
    elif(token==TokenType.NREAL.value):
        tr=Tree('REAL',[])
        tr.append(Tree(tkstrg,[]))
        match(TokenType.NREAL.value)
    elif(token==TokenType.PARENIZQ.value):
        match(TokenType.PARENIZQ.value)
        tr=expresion()
        match(TokenType.PARENDERE.value)
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        token=getTokenSintactico()
    return tr
     

def match(expected:TokenType):
    global token
    if(token==expected):
        token=getTokenSintactico()
    else:
        #sintaxError("Unexpected Token "+tkstrg)
        pass

tok=getTokenSintactico()
print(tok)
while(tok!="ENDFILE"):
    print(tok)
    tok=getTokenSintactico() 

def parse()->Tree:
    global token
    global raiz
    raiz=Tree('PROGRAMA',[])
    token=getTokenSintactico()
    raiz.append(lista_declaracion())
    if(token!=TokenType.ENDFILE.value):
        #sintaxError('Code ends before file\n')
        print("Code ends before file\n")
    return raiz
   
def sintaxError(message):
   global palabras
   #print("\n>>> Syntax error at line {}: {}".format(palabras[2], message))
   
arbol=parse()
transform_json(arbol)

source.close()

import tkinter as tk
from tkinter import ttk
from nltk import Tree
# Ejemplo de un árbol de NLTK

tree_nltk = Tree('S', [Tree('NP', ['John']), Tree('VP', ['sleeps'])])

window = tk.Tk()
#window.geometry("800x600")
window.title("Árbol de NLTK")

treeview = ttk.Treeview(window)
treeview["columns"] = ("Label", "Parent")
treeview.heading("#0", text="ID")
treeview.heading("Label", text="Label")
treeview.heading("Parent", text="Parent")



def add_tree_node(tree, parent_node=""):
    node_id = str(id(tree))  # Generar un identificador único para el nodo
    label = tree.label()
    treeview.insert(parent_node, tk.END, node_id, text=node_id, values=(label, parent_node))
    if isinstance(tree, Tree):
        for child in tree:
            add_tree_node(child, parent_node=node_id)


add_tree_node(arbol)

treeview.pack()
window.mainloop() """
def lista_declaracion()->TreeNode:
    global token
    #tr=Tree('LISTA_DECLARACION',[])
    tr=sentencias()
    pr=tr
    #pd=tr.append(declaracion())
    #pd=tr.extend(declaracion())

    while( token != TokenType.ENDFILE.value 
        and token != TokenType.ELSE.value
        and token != TokenType.UNTIL.value 
        and token != TokenType.END.value
        and token !=TokenType.LLAVEDER.value): #llave o parentesis? RBPAREN
        qr = sentencias()
        if(qr!=None):
            if(tr==None):
                tr = pr = qr
            else:
                pr.setSibling(qr)
                pr = qr
        #match(TokenType.PUNTOCOMA.value)
        #dec = declaracion()
        #tr.append(dec)
        #tr.extend(dec) 
    #if(len(tr)==0):
        #tr=Tree('',[])  
    return tr

    

def declaracion_variable()->TreeNode:
    global token
    global tkstrg
    #tr=Tree('DECLARACION_VARIABLE',[])
    #tr2=Tree('DECLARACION_VARIABLE',[])
    tr=newStmtNode(SentenciaKind.DECKD.value)
    tr2=newStmtNode(SentenciaKind.TYPEDEFIKD.value)


    if(token==TokenType.REAL.value):
        #tr2.append(Tree(str(TokenType.REAL.name),[]))
        tr2.setType(DeclaracionKind.REALKD.value)
        tr2.setAttr(TokenType.REAL.value)
        match(TokenType.REAL.value)
    elif(token==TokenType.INT.value):
        #tr2.append(Tree(str(TokenType.INT.name),[]))
        tr2.setType(DeclaracionKind.INTKD.value)
        tr2.setAttr(TokenType.INT.value)
        match(TokenType.INT.value)
    elif(token==TokenType.BOOLEAN.value):
        #tr2.append(Tree(str(TokenType.BOOLEAN.name),[]))
        tr2.setType(DeclaracionKind.BOOLEANKD.value)
        tr2.setAttr(TokenType.BOOLEAN.value)
        match(TokenType.BOOLEAN.value)
    else:
        #sintaxError('Unknown Data')
        #token=getTokenSintactico()
        recuperacion()
        return tr
    #tr2.append(lista_identificadores())
    tr.setChild(tr2,0)
    id=newExpNode(ExpresionKind.IDKD.value)
    
    if(token==TokenType.ID.value):
        id.setAttr(tkstrg)
        id.setType(tr2.getType())
        tr.setChild(id,1)
        match(TokenType.ID.value)
        while(token==TokenType.COMA.value):
            match(TokenType.COMA.value)
            id2 = newExpNode(ExpresionKind.IDKD.value)
            id2.setAttr(tkstrg)
            id2.setType(tr2.getType())

            id.setSibling(id2)
            id = id2

            match(TokenType.ID.value)
    
    if(token== TokenType.PUNTOCOMA.value):
        match(TokenType.PUNTOCOMA.value)
    else:
        #sintaxError("Unknow Token "+tkstrg)
        recuperacion()
    #tr.append(tr2)
    #match(TokenType.PUNTOCOMA.value)
    return tr

def declaracion()->TreeNode:
    global token
    tr=Tree('',[])

    if(token==TokenType.REAL.value or token==TokenType.INT.value or token==TokenType.BOOLEAN.value):
        tr=declaracion_variable()
    else:
        tr=lista_sentencias()
    return tr

def lista_sentencias()->TreeNode:
    global token
    global tkstrg
    tr=Tree('LISTA_SENTENCIAS',[])

    if(token==TokenType.IF.value 
        or token==TokenType.DO.value
        or token==TokenType.WHILE.value
        or token==TokenType.CIN.value 
        or token==TokenType.COUT.value 
        or token==TokenType.ID.value
        or token==TokenType.MAIN.value
        or token==TokenType.PLUSPLUS.value
        or token==TokenType.MENOSMENOS.value):
        tr=Tree('LISTA_SENTENCIAS',[])
        while(token==TokenType.IF.value 
            or token==TokenType.DO.value
            or token==TokenType.WHILE.value
            or token==TokenType.CIN.value 
            or token==TokenType.COUT.value 
            or token==TokenType.ID.value
            or token==TokenType.MAIN.value
            or token==TokenType.PLUSPLUS.value
            or token==TokenType.MENOSMENOS.value):
                tr.append(sentencias())
    else:
        tr=Tree('',[])
        #sintaxError("Unknow Token "+tkstrg)
        token=getTokenSintactico()
    return tr

def lista_identificadores():
    global token
    global tkstrg
    tr=Tree('',[])
    if(token==TokenType.ID.value):
        tr=Tree('VAR',[])
        tr.append(Tree(tkstrg,[]))
        match(TokenType.ID.value)
        while(token==TokenType.COMA.value):
            match(TokenType.COMA.value)
            if(token==TokenType.ID.value):
                tr.append(Tree(tkstrg,[]))
                match(TokenType.ID.value)
    
    return tr


def sentencias()->TreeNode|None:
    global token
    global tkstrg
    #tr=Tree('',[])
    tr=None

    if(token==TokenType.IF.value):
        tr=sentencia_if()
    elif(token==TokenType.DO.value):
        tr=sentencia_do()
    elif(token==TokenType.WHILE.value):
        tr=sentencia_while()
    elif(token==TokenType.CIN.value):
        tr=sentencia_cin()
    elif(token==TokenType.COUT.value):
        tr=sentencia_cout()
    elif(token==TokenType.ID.value 
        or token==TokenType.PLUSPLUS.value
        or token==TokenType.MENOSMENOS.value):
        tr=asignacion_sencilla()
    elif(token==TokenType.MAIN.value):
        tr=sentencia_main()
    elif(token==TokenType.BOOLEAN.value or token==TokenType.INT.value or token==TokenType.REAL.value):
        tr=declaracion_variable()
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        #token=getTokenSintactico()
        recuperacion()
    return tr

def sentencia_if()->TreeNode:
    global token
    #tr=Tree('IF',[])
    tr = newStmtNode(SentenciaKind.IFKD.value)
    match(TokenType.IF.value)
    #tr.append(expresion())
    #tr.extend(lista_declaracion())
    tr.setChild(expresion(),0)
    tr.setChild(lista_declaracion(),1)
    if(token==TokenType.ELSE.value):
        match(TokenType.ELSE.value)
        #els=Tree('ELSE',[])
        #els.extend(lista_declaracion())
        #tr.append(els)
        tr2 = newStmtNode(SentenciaKind.ELSEKD.value)
        tr2.setChild(lista_declaracion(),0)
        tr.setChild(tr2,2)
    match(TokenType.END.value)
    return tr

def sentencia_do()->TreeNode:
    #global token
    #tr=Tree('DO',[])
    tr = newStmtNode(SentenciaKind.UNTILKD.value)
    match(TokenType.DO.value)
    #tr.append(lista_declaracion())
    tr.setChild(lista_declaracion(),0)
    match(TokenType.UNTIL.value)
    #tr.append(expresion())
    tr.setChild(expresion(),1)
    match(TokenType.PUNTOCOMA.value)
    return tr

def sentencia_while()->TreeNode:
    global token
    #tr=Tree('WHILE',[])
    tr = newStmtNode(SentenciaKind.WHILEKD.value)
    match(TokenType.WHILE.value)
    #tr.append(expresion())
    tr.setChild(expresion(),0)
    match(TokenType.LLAVEIZQ.value)
    #tr.extend(lista_declaracion())
    tr.setChild(lista_declaracion(),1)
    match(TokenType.LLAVEDER.value)
    return tr

def sentencia_cin()->TreeNode:
    global token
    global tkstrg
    #tr=Tree('CIN',[])
    tr = newStmtNode(SentenciaKind.CINKD.value)
    match(TokenType.CIN.value)
    if(token==TokenType.ID.value):
        #tr.append(Tree(tkstrg,[]))
        tr.setAttr(tkstrg)
    match(TokenType.ID.value)
    match(TokenType.PUNTOCOMA.value)
    return tr

def sentencia_cout()->TreeNode:
    global token
    #tr=Tree('COUT',[])
    tr = newStmtNode(SentenciaKind.COUTKD.value)
    match(TokenType.COUT.value)
    #tr.append(expresion())
    tr.setChild(expresion(),0)
    match(TokenType.PUNTOCOMA.value)
    return tr

"""def sentencia_asignaciongeneral()->TreeNode:
    global token
    global tkstrg
    tr=Tree('ASIGNACION',[])
    if(token==TokenType.MENOSMENOS.value
       or token==TokenType.PLUSPLUS.value):
        tr.extend(asignacion_prefijo())
    elif (token==TokenType.ID.value):
        tr.extend(asignacion_sencilla())
    return tr"""

def asignacion_prefijo()->TreeNode:
    global tkstrg
    global token
    #tr=Tree('ASIGNACION',[])
    #tr.append(Tree(tkstrg,[]))
    tr = newExpNode(ExpresionKind.OPERKD.value)
    tr.setAttr(token)
    match(token)
    id = newExpNode(ExpresionKind.IDKD.value)
    id.setAttr(tkstrg)
    ag = newExpNode(ExpresionKind.CONSTKD.value)
    ag.setAttr(1)
    tr.setChild(id,0)
    tr.setChild(ag,1)

    return tr

    """ if(token==TokenType.ID.value):
        tr[0].append(Tree(tkstrg,[]))
        match(TokenType.ID.value)
        match(TokenType.PUNTOCOMA.value)
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        token=getTokenSintactico()
    return tr """


def asignacion_postfijo(var:str)->TreeNode:
    global tkstrg
    global token
    tr = newExpNode(ExpresionKind.OPERKD.value)
    tr.setAttr(token)
    id = newExpNode(ExpresionKind.IDKD.value)
    id.setAttr(var)
    ag = newExpNode(ExpresionKind.CONSTKD.value)
    ag.setAttr(1)
    tr.setChild(id,0)
    tr.setChild(ag,1)
    """ tr=Tree('ASIGNACION',[])
    tr.append(Tree(tkstrg,[]))
    match(token)
    if(token==TokenType.MENOSMENOS.value
       or token==TokenType.PLUSPLUS.value):
        tr[0].append(Tree(tkstrg,[]))
        match(token)
        match(TokenType.PUNTOCOMA.value)
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        token=getTokenSintactico() """
    return tr

def asignacion_sencilla()->TreeNode:
    global tkstrg
    global token
    #tr=Tree('ASIGNACION',[])
    #tr.append(Tree(tkstrg,[]))
    tr = newStmtNode(SentenciaKind.ASIGKD.value)
    if(token==TokenType.MENOSMENOS.value or token==TokenType.PLUSPLUS.value):
        tr.setChild(asignacion_prefijo(),0)
        match(token)
    else:
        var=tkstrg
        tr.setAttr(tkstrg)
        match(TokenType.ID.value)
        #match(token)
        #if(token==TokenType.ID.value):
            #tr.append(Tree(tkstrg,[]))
        #match(TokenType.ID.value)
        if(token==TokenType.ASIGNACION.value):
            match(TokenType.ASIGNACION.value)
            #tr.extend(sentencia_exp())
            tr.setChild(expresion(),0)
        elif(token==TokenType.MENOSMENOS.value
            or token==TokenType.PLUSPLUS.value):
            #tr.extend(asignacion_postfijo())
            tr.setChild(asignacion_postfijo(var),0)
            match(token)
        else:
            pass
        #tr.append(Tree('',[]))
    match(TokenType.PUNTOCOMA.value)
    return tr


def sentencia_main()->TreeNode:
    #tr=Tree('MAIN',[])
    tr = newStmtNode(SentenciaKind.MAINKD.value)
    match(TokenType.MAIN.value)
    match(TokenType.LLAVEIZQ.value)
    #tr.extend(lista_declaracion())
    tr.setChild(lista_declaracion(),0)
    match(TokenType.LLAVEDER.value)
    return tr


def sentencia_exp()->TreeNode:
    global token
    tr=Tree('SENTENCIA_EXPRESION',[])
    if(token==TokenType.PUNTOCOMA.value):
        tr.append(Tree(';',[]))
        match(TokenType.PUNTOCOMA.value)
    else:
        tr.append(expresion())
        match(TokenType.PUNTOCOMA.value)
    return tr

def expresion()->TreeNode:
    global token
    global tkstrg
    #tr=expresion_simple()
    tr = expresion_simple()
    if((token==TokenType.IGUALDAD.value)
       or (token==TokenType.DIFERENTEDE.value)
       or (token==TokenType.MAYOR.value)
       or (token==TokenType.MAYOREQ.value)
       or (token==TokenType.MENOR.value)
       or (token==TokenType.MENOREQ.value)):
        #pd=Tree(tkstrg,[])
        pd=newExpNode(ExpresionKind.OPERKD.value)
        pd.setChild(tr,0)
        pd.setAttr(token)
        #pd.append(tr)
        tr=pd
        match(token)
        #tr.append(expresion_simple())
        tr.setChild(expresion_simple(),1)
    return tr


def termino()->TreeNode:
    global token
    tr=factor()
    while(token==TokenType.MULTI.value or token==TokenType.DIV.value or token==TokenType.RES.value):
        #pd=Tree(tkstrg,[])
        pd=newExpNode(ExpresionKind.OPERKD.value)
        pd.setChild(tr,0)
        pd.setAttr(token)
        #pd.append(tr)
        tr=pd
        match(token)
        #pd.append(factor())
        pd.setChild(factor(),1)
    return tr
   
def expresion_simple()->TreeNode:
    global token
    #global tkstrg
    tr=termino()
    while((token==TokenType.SUMA.value) 
        or (token==TokenType.PLUSPLUS.value) 
        or (token==TokenType.RESTA.value)
        or (token==TokenType.MENOSMENOS.value)):
        #pd=Tree(tkstrg,[])
        pd=newExpNode(ExpresionKind.OPERKD.value)
        pd.setChild(tr,0)
        pd.setAttr(token)
        #pd.append(tr)
        tr=pd
        match(token)
        #pd.append(termino())
        pd.setChild(termino(),1)
    return tr

def factor()->TreeNode:
    global token
    global tkstrg
    #tr=Tree('',[])
    tr=None
    if(token==TokenType.ID.value):
        #tr=Tree('ID',[])
        tr=newExpNode(ExpresionKind.IDKD.value)
        tr.setAttr(str(tkstrg))
        #tr.append(Tree(tkstrg,[]))
        match(TokenType.ID.value)
    elif(token==TokenType.ENTERO.value):
        #tr=Tree('ENTERO',[])
        tr=newExpNode(ExpresionKind.CONSTKD.value)
        tr.setAttr(int(tkstrg))
        #tr.append(Tree(tkstrg,[]))
        match(TokenType.ENTERO.value)
    elif(token==TokenType.NREAL.value):
        #tr=Tree('REAL',[])
        tr=newExpNode(ExpresionKind.CONSTFKD.value)
        tr.setAttr(float(tkstrg))
        #tr.append(Tree(tkstrg,[]))
        match(TokenType.NREAL.value)
    elif(token==TokenType.PARENIZQ.value):
        match(TokenType.PARENIZQ.value)
        tr=expresion()
        match(TokenType.PARENDERE.value)
    else:
        #sintaxError('Unexpected Token '+tkstrg)
        #token=getTokenSintactico()
        recuperacion()
    return tr
     

def match(expected:TokenType):
    global token
    if(token==expected):
        token=getTokenSintactico()
    else:
        #sintaxError("Unexpected Token "+tkstrg)
        pass


def parse()->TreeNode:
    global token
    global raiz
    #raiz=Tree('PROGRAMA',[])
    raiz=None
    token=getTokenSintactico()
    #raiz.append(lista_declaracion())
    raiz=lista_declaracion()
    if(token!=TokenType.ENDFILE.value):
        #sintaxError('Code ends before file\n')
        print("Code ends before file\n")
    return raiz

def recuperacion():
    global token
    while(not(token==TokenType.IF.value or token==TokenType.CIN.value or token==TokenType.COUT.value or
              token==TokenType.ENDFILE.value or token==TokenType.DO.value or token==TokenType.MAIN.value or 
              token==TokenType.END.value or token==TokenType.THEN.value or token==TokenType.ELSE.value or
              token==TokenType.WHILE.value or token==TokenType.REAL.value or token==TokenType.UNTIL.value or
              token==TokenType.INT.value or token==TokenType.REPEAT.value or token==TokenType.BOOLEAN.value or
              token==TokenType.LLAVEDER.value or token==TokenType.PUNTOCOMA.value)):
        token=getTokenSintactico()
    if(token==TokenType.PUNTOCOMA.value):
           token=getTokenSintactico()
        


def sintaxError(message):
   global palabras
   #print("\n>>> Syntax error at line {}: {}".format(palabras[2], message))

arbol=parse()

from util import creacionarbol
with open('arbolSin.json','w') as arch:
    arb=creacionarbol(arbol)
    json.dump(arb,arch)
