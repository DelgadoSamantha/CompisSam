from globals import TokenType 
from nltk.tree import Tree
import os
from jsonparse import *


MAXCHILDREN = 3

global palabras
global indice
#archivo='testSintaxis.txt'
indice=0
tkstrg=''
raiz=Tree('PROGRAMA',[])
token=-1
source = open('archtoken.txt','r')
lineno=0
colpos=0

""" def getTokenSintactico():
    global source
    global lineno
    global colpos
    linea = source.readline()
    global tokenString
    if  linea:
        elementos = linea.split('\t')
        elementos = [elemento.replace("\n", "") for elemento in elementos]
        lts = []
        aux = elementos[0]
        if len(elementos)>=2:
            tokenString = elementos[1]
            lineno = elementos[2]
            colpos = elementos[3]
        if(elementos[0] == 'RESERVED-WORD'):
           aux = TokenType[elementos[1].upper()].value 
        else:
            aux = TokenType[aux.upper()].value 
        return aux   
    else:
        return TokenType.ENDFILE.value  
 """

def obtener_siguiente_linea():
    with open(os.path.join(os.getcwd(),'archToken.txt'), "r") as archivo:
        lineas = archivo.readlines()
        obtener_siguiente_linea.indice += 1  # Variable estática para rastrear el índice
 
        if obtener_siguiente_linea.indice <= len(lineas):
            return lineas[obtener_siguiente_linea.indice - 1].strip()
        else:
            return None
 
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

def lista_declaracion()->Tree:
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
   
    if(token==TokenType.FLOAT.value):
        tr2.append(Tree(str(TokenType.FLOAT.value),[]))
        match(TokenType.FLOAT.value)
    elif(token==TokenType.INT.value):
        tr2.append(Tree(str(TokenType.INT.value),[]))
        match(TokenType.INT.value)
    elif(token==TokenType.BOOLEAN.value):
        tr2.append(Tree(str(TokenType.BOOLEAN.value),[]))
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

    if(token==TokenType.FLOAT.value or token==TokenType.INT.value or token==TokenType.BOOLEAN.value):
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
    elif(token==TokenType.FLOAT.value):
        tr=Tree('REAL',[])
        tr.append(Tree(tkstrg,[]))
        match(TokenType.FLOAT.value)
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

""" tok=getTokenSintactico()
print(tok)
while(tok!="ENDFILE"):
    print(tok)
    tok=getTokenSintactico()   """

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

tree_nltk = Tree('S', [Tree('NP', ['John']), Tree('VP', ['sleeps'])])

window = tk.Tk()
window.title("Árbol de NLTK")

treeview = ttk.Treeview(window)
treeview["columns"] = ("Label", "Parent")
treeview.heading("#0", text="ID")
treeview.heading("Label", text="Label")
treeview.heading("Parent", text="Parent")




def add_tree_node(tree, parent_node=""):
    node_id = str(id(tree))  
    label = tree.label()
    treeview.insert(parent_node, tk.END, node_id, text=node_id, values=(label, parent_node))
    if isinstance(tree, Tree):
        for child in tree:
            add_tree_node(child, parent_node=node_id)


add_tree_node(arbol)

treeview.pack()
window.mainloop()