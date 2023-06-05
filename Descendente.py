import sys
import os

indicador = 0

#######################################
#####                             #####
#####    Analizador sintáctico    #####
#####                             #####
#######################################

#Errores
def error():
    print("\nError en la linea " + str(globalLin[indicador]))
    print("No se esperaba el token " + globalTokens[indicador] + '\n')
    sys.exit(1)


#Ejecución del analizado sintáctico
def program():
    global indicador
    declaration()
    if globalTokens[indicador] == 'EOF':
        print("La cadena fue valida")
    else:
        print("Error de la cadena")

#Declaraciones---------------------------------------------
def declaration():
    if class_decl():
        declaration()
    elif fun_decl():
        declaration()
    elif var_decl():
        declaration()
    elif statement():
        declaration()
    else: pass
        
def class_decl():
    global indicador
    if globalTokens[indicador] == 'CLASS':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if class_inher():
                if globalTokens[indicador] == '{':
                    indicador += 1
                    if functions():
                        if globalTokens[indicador] == '}':
                            indicador += 1
                            return True
                        else: error()
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def class_inher():
    global indicador
    if globalTokens[indicador] == '<':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            return True
        else: error()
    else: return True

def fun_decl():
    global indicador
    if globalTokens[indicador] == 'FUN':
        indicador += 1
        if funct(): return True
    else: return False

def var_decl():
    global indicador
    if globalTokens[indicador] == 'VAR':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if var_init():
                if globalTokens[indicador] == ';':
                    indicador += 1
                    return True
                else: error()
            else: error()
        else: error()
    else: return False

def var_init():
    global indicador
    if globalTokens[indicador] == '=':
        indicador += 1
        if expression():
            return True
    else: return True

#Sentencias------------------------------------------------
def statement():
    global indicador
    if expr_stmt():
        return True
    elif for_stmt():
        return True
    elif if_stmt():
        return True
    elif print_stmt():
        return True
    elif return_stmt():
        return True
    elif while_stmt():
        return True
    elif block():
        return True
    else: return False

def expr_stmt():
    global indicador
    if expression():
        if globalTokens[indicador] == ';':
            indicador += 1
            return True
        else: error()
    else: return False

def for_stmt():
    global indicador
    if globalTokens[indicador] == 'FOR':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if for_stmt_1():
                if for_stmt_2():
                    if for_stmt_3():
                        if globalTokens[indicador] == ')':
                            indicador += 1
                            if statement():
                                return True
                            else: error()
                        else: error()
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def for_stmt_1():
    global indicador
    if var_decl():
        return True
    elif expr_stmt():
        return True
    elif globalTokens[indicador] == ';':
        indicador += 1
        return True
    else: return False

def for_stmt_2():
    global indicador
    if expression():
        if globalTokens[indicador] == ';':
            indicador += 1
            return True
        else: error()
    elif globalTokens[indicador] == ';':
        indicador += 1
        return True
    else: return False

def for_stmt_3():
    global indicador
    if expression():
        return True
    else: return True

def if_stmt():
    global indicador
    if globalTokens[indicador] == 'IF':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if expression():
                if globalTokens[indicador] == ')':
                    indicador += 1
                    if statement():
                        if else_statement():
                            return True
                        else: error()
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def else_statement():
    global indicador
    if globalTokens[indicador] == 'ELSE':
        indicador += 1
        if statement():
            return True
        else: error()
    else: return True

def print_stmt():
    global indicador
    if globalTokens[indicador] == 'PRINT':
        indicador += 1
        if expression():
            if globalTokens[indicador] == ';':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

def return_stmt():
    global indicador
    if globalTokens[indicador] == 'RETURN':
        indicador += 1
        if return_exp_opc():
            if globalTokens[indicador] == ';':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

def return_exp_opc():
    global indicador
    if expression():
        return True
    else: return True

def while_stmt():
    global indicador
    if globalTokens[indicador] == 'WHILE':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if expression():
                if globalTokens[indicador] == ')':
                    indicador += 1
                    if statement():
                        return True
                    else: error()
                else: error()
            else: error()
        else: error()   
    else: return False

def block():
    global indicador
    if globalTokens[indicador] == '{':
        indicador += 1
        if block_decl():
            if globalTokens[indicador] == '}':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

def block_decl():
    global indicador
    if declaration():
        if block_decl():
            return True
        else: error()
    else: return True

#Expresiones----------------------------------------------
def expression():
    global indicador
    if assignment(): return True
    else: return False

def assignment():
    global indicador
    if logic_or():
        if assignment_opc(): return True
        else: error()
    else: return False

def assignment_opc():
    global indicador
    if globalTokens[indicador] == '=':
        indicador += 1
        if expression(): return True
        else: error()
    else: return True

def logic_or():
    global indicador
    if logic_and():
        if logic_or_2(): return True
        else: error()
    else: return False

def logic_or_2():
    global indicador
    if globalTokens[indicador] == 'OR':
        indicador += 1
        if logic_and():
            if logic_or_2(): return True
            else: error()
        else: error()
    else: return True

def logic_and():
    global indicador
    if equality():
        if logic_and_2(): return True
        else: error()
    else: return False

def logic_and_2():
    global indicador
    if globalTokens[indicador] == 'AND':
        indicador += 1
        if equality():
            if logic_and_2(): return True
            else: error()
        else: error()
    else: return True

def equality():
    global indicador
    if comparison():
        if equality_2(): return True
        else: error()
    else: return False

def equality_2():
    global indicador
    if globalTokens[indicador] == '!=':
        indicador += 1
        if comparison():
            if equality_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '==':
        indicador += 1
        if comparison():
            if equality_2(): return True
            else: error()
        else: error()
    else: return True

def comparison():
    global indicador
    if term():
        if comparison_2(): return True
        else: error()
    else: return False

def comparison_2():
    global indicador
    if globalTokens[indicador] == '>':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '>=':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '<':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '<=':
        indicador += 1
        if term():
            if comparison_2(): return True
            else: error()
        else: error()
    else: return True

def term():
    global indicador
    if factor():
        if term_2(): return True
        else: error()
    else: return False

def term_2():
    global indicador
    if globalTokens[indicador] == '-':
        indicador += 1
        if factor():
            if term_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '+':
        indicador += 1
        if factor():
            if term_2(): return True
            else: error()
        else: error()
    else: return True

def factor():
    global indicador
    if unary():
        if factor_2(): return True
        else: error()
    else: return False

def factor_2():
    global indicador
    if globalTokens[indicador] == '/':
        indicador += 1
        if unary():
            if factor_2(): return True
            else: error()
        else: error()
    elif globalTokens[indicador] == '*':
        indicador += 1
        if unary():
            if factor_2(): return True
            else: error()
        else: error()
    else: return True

def unary():
    global indicador
    if globalTokens[indicador] == '!':
        indicador += 1
        if unary(): return True
        else: error()
    elif globalTokens[indicador] == '-':
        indicador += 1
        if unary(): return True
        else: error()
    elif call(): return True
    else: return False

def call():
    global indicador
    if primary():
        if call_2(): return True
        else: error()
    else: return False

def call_2():
    global indicador
    if globalTokens[indicador] == '(':
        indicador += 1
        if arguments_opc():
            if globalTokens[indicador] == ')':
                indicador += 1
                if call_2(): return True
                else: error()
            else: error()
        else: error()
    elif globalTokens[indicador] == '.':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if call_2(): return True
            else: error()
        else: error()
    else: return True

def call_opc():
    global indicador
    
def primary():
    global indicador
    if globalTokens[indicador] == 'TRUE':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'FALSE':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'NULL':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'THIS':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'INT':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'FLOAT':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'STRING':
        indicador += 1
        return True
    elif globalTokens[indicador] == 'ID':
        indicador += 1
        return True
    elif globalTokens[indicador] == '(':
        indicador += 1
        if expression():
            if globalTokens[indicador] == ')':
                indicador += 1
                return True
            else: error()
        else: error()
    elif globalTokens[indicador] == 'SUPER':
        indicador += 1
        if globalTokens[indicador] == '.':
            indicador += 1
            if globalTokens[indicador] == 'ID':
                indicador += 1
                return True
            else: error()
        else: error()
    else: return False

#Otras----------------------------------------------------
def funct():
    global indicador
    if globalTokens[indicador] == 'ID':
        indicador += 1
        if globalTokens[indicador] == '(':
            indicador += 1
            if parameters_opc():
                if globalTokens[indicador] == ')':
                    indicador += 1
                    if block(): return True
                    else: error()
                else: error()
            else: error()
        else: error()
    else: return False

def functions():
    global indicador
    if funct():
        if functions(): return True
        else: error()
    else: return True

def parameters_opc():
    global indicador
    if parameters(): return True
    else: return True

def parameters():
    global indicador
    if globalTokens[indicador] == 'ID':
        indicador += 1
        if parameters_2(): return True
        else: error()
    else: False

def parameters_2():
    global indicador
    if globalTokens[indicador] == ',':
        indicador += 1
        if globalTokens[indicador] == 'ID':
            indicador += 1
            if parameters_2(): return True
            else: error()
        else: error()
    else: return True

def arguments_opc():
    global indicador
    if arguments(): return True
    else: return True

def arguments():
    global indicador
    if expression():
        if arguments_2(): return True
        else: error()
    else: False

def arguments_2():
    global indicador
    if globalTokens[indicador] == ',':
        indicador += 1
        if expression():
            if arguments_2(): return True
            else: error()
        else: error()
    else: return True



###################################
#####                         #####
#####    Analizador léxico    #####
#####                         #####
###################################

#Quita comillas
def convCadena(cadena):
        newPala = []
        for c in cadena:
            if c != "\"":
                newPala += c
        return "".join(newPala)

#Imprime tokens
"""def imprimeTokens(cadenas, tokens):
    for i in range(len(cadenas)):
        #Para floats
        if tokens[i] == 'FLOAT':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}, Valor: {float(cadenas[i])}')
        #Para enteros
        elif tokens[i] == 'INT':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}, Valor: {int(cadenas[i])}')
        #Para cadenas
        elif tokens[i] == 'STRING':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}, Valor: {str(convCadena(cadenas[i]))}')
        #Para los otros
        elif cadenas[i] != '\n':
            print(f'Token: {tokens[i]}, Lexema: {cadenas[i]}')
    return"""

#Comprueba si es un numero flotante
def compfloat(cadena):
    for c in cadena:
        if c == '.':
            return True 
    return False

#Palabras reservadas
def reservadas(cadena):
    palabrasHM = {'for':'FOR', 'fun':'FUN', 'false':'FALSE', 'if':'IF', 'print':'PRINT', 'return':'RETURN', 
                'true':'TRUE', 'var':'VAR', 'else':'ELSE', 'or':'OR', 'null':'NULL', 'try':'TRY',
                'not':'NOT', 'break':'BREAK', 'and':'AND', 'identificador':'ID', 'float':'FLOAT',
                'int':'INT', 'string':'STRING', '=':'=', 'while':'WHILE',
                '+':'+', '-':'-', '/':'/', '*':'*', '+=':'+=',
                '<=':'<=', '>=':'>=', '==':'==', '!=':'!=', '<':'<', '>':'>',
                '-=':'-=', '{':'{', '}':'}', '[':'[', ']':']',
                '(':'(', ')':')', ';':';', '.':'.', ',':',',
                'class':'CLASS', 'this':'THIS', 'super':'SUPER'}
    if cadena in palabrasHM :
        return palabrasHM[cadena]
    else: 
        return False
  
#Asignar palabras reservadas en tokens
def PalRe(cadena):
    tokens=[]
    for cad in cadena:
        if(reservadas(cad))!=False:
            tokens.append(reservadas(cad)) 
        elif (letras(cad[0])):
            tokens.append(reservadas('identificador'))
        #Tipo de número
        elif(numeros(cad[0]) or cad[0] == '.'):
            if(compfloat(cad)):
                tokens.append(reservadas('float'))
            else:
                tokens.append(reservadas('int'))
        #Tipo de dato
        elif(comillas(cad[0])):
            if(len(cad)>2):
                tokens.append(reservadas('string'))
            else:
                tokens.append(reservadas(cad))
        else:
            tokens.append(reservadas(cad))

    #Agrega EOF al último
    tokens.append('EOF')

    return tokens

#Categorias
def comillas(caracter):
    return caracter in "\""
def simbolos(caracter):
    return caracter in "(){}[],.:;-+*/!=<>%&"
def espacios(caracter):
    return caracter in " \n\t"
def letras(caracter):
    return caracter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWX_"
def numeros(caracter):
    return caracter in "1234567890"
def operadores(caracter):
    return caracter in ["!=", "==", "<=", ">="]
def operaciones(caracter):
    return caracter in "/=+-*"
def llaves(caracter):
    return caracter in "{[()]}"

#Comprueba que sea numero
def compnum(cadena):
    validar = True
    for n in cadena:
        if numeros(n) == False:
            validar = False
    return validar

#Separa cada token
def separador(cadena):
    lineas = []
    estado = 0
    tokens = []
    tokenaux = []
    listado = []
    #Separa letras(cadenas), numeros, operadores, espacios, palabras reservadas
    for c in cadena:
        #Estado 0 - Inicio
        if letras(c) and estado == 0:
            estado = 1
            tokenaux += c
        elif numeros(c) and estado == 0:
            estado = 2 
            tokenaux += c
        elif comillas(c) and estado == 0:
            estado = 3
            tokenaux += c
        elif simbolos(c) and estado == 0:
            tokens += c
        elif espacios(c) and estado == 0:
            tokens += c
        #Estado 1 - Letras
        elif (letras(c) or numeros(c)) and estado == 1:
            tokenaux += c
        elif comillas(c) and estado == 1:
            estado = 3
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif simbolos(c) and estado == 1:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif espacios(c) and estado == 1:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        #Estado 2 - Números
        elif numeros(c) and estado == 2:
            tokenaux += c
        elif comillas(c) and estado == 2:
            estado = 3
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        elif simbolos(c) and estado == 2:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif espacios(c) and estado == 2:
            estado = 0
            tokens.append("".join(tokenaux))
            tokens += c
            tokenaux.clear()
        elif letras(c) and estado == 2:
            estado = 1
            tokens.append("".join(tokenaux))
            tokenaux.clear()
            tokenaux += c
        #Estado 3 - Cadenas
        elif not(comillas(c)) and estado == 3:
            tokenaux += c
        elif comillas(c) and estado == 3:
            estado = 0
            tokenaux += c
            tokens.append("".join(tokenaux))
            tokenaux.clear()
    if estado == 3:
        print("Error léxico, una cadena no fue terminanda")
        sys.exit(1)
    if estado == 2 or estado == 1:
        tokens.append("".join(tokenaux))
        tokenaux.clear()
    tokenaux.clear()

    #Junta los operadores: "<=" ">=" "==" "!=" "+="
    for i in range(len(tokens)):
        try:
            if (tokens[i] in "!=+-<>") and tokens[i+1] == "=":
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                tokenaux.clear()
        except IndexError:
            pass
    tokenaux.clear()

    #Junta los numeros flotantes
    compru = 0
    for i in range(len(tokens)):
        try:    
            if compru != 0:
                compru -= 1
            elif compnum(tokens[i]) and tokens[i+1] == "." and compnum(tokens[i+2]):
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokenaux += tokens[i+2]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                tokens[i+2] = ""
                listado.append(i+1)
                listado.append(i+2)
                compru = 2
                tokenaux.clear() 
            elif tokens[i] == "." and compnum(tokens[i+1]):
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()
            elif compnum(tokens[i]) and tokens[i+1] == '.':
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()

        except IndexError:
            if (i + 2) > len(tokens):
                compru = 0
            elif tokens[i] == "." and compnum(tokens[i+1]):
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()
            elif compnum(tokens[i]) and tokens[i+1] == '.':
                tokenaux += tokens[i]
                tokenaux += tokens[i+1]
                tokens[i] = "".join(tokenaux)
                tokens[i+1] = ""
                listado.append(i+1)
                compru = 1
                tokenaux.clear()
         
    tokenaux.clear()

    #Elimina los datos sobrados
    listado.sort()
    cont = 0
    for num in listado:
        num -= cont
        tokens.pop(num)
        cont += 1
    
    #Elimina espacios
    cont=0
    for i in range(len(tokens)):
        if tokens[i]==' ':
            cont+=1
    for j in range(cont):
        tokens.remove(' ')

    #Elimina espacios \t
    cont=0
    for i in range(len(tokens)):
        if tokens[i]=='\t':
            cont+=1
    for j in range(cont):
        tokens.remove(' \t')
    
    #Elimina saltos de linea
    cont=0

    for i in range(len(tokens)):    
        if tokens[i]=='\n':
            cont+=1
        else: lineas.append(cont+1)
    for j in range(cont):
        tokens.remove('\n')

    return tokens, lineas

#Omite los comentarios
def remove(cadena):
    estado = 0
    cad = []
    for c in cadena:
        #estado 0
        if estado == 0 and c == '/':
            estado = 1
            cad += c
        elif estado == 0 and c != '/':
            cad += c
        #estado 1
        elif estado == 1 and c == '/':
            estado = 2
            cad.pop()
        elif estado == 1 and c == '*':
            estado = 3
            cad.pop()
        elif estado == 1 and c != '/':
            estado = 0
            cad += c
        #estado 2
        elif estado == 2 and c == '\n':
            estado = 0
            cad += c
        #estado 3
        elif estado == 3 and c == '*':
            estado = 4
        #estado 4
        elif estado == 4 and c == '*':
            estado = 4 
        elif estado == 4 and c == '/':
            estado = 0
        elif estado == 4 and c != '/':
            estado = 3  
        if estado != 0:
            if c == '\n':
                cad += c
    return cad



#############################
###                       ###
###   Función principal   ###
###                       ###
#############################

def lexico(cadena):
    cad = remove(cadena)
    global globalLex, globalLin
    globalLex, globalLin = separador(cad)
    global globalTokens 
    globalTokens = PalRe(globalLex)

    program()
    



#Transforma archivo txt a cadena
def transforma(archivo):
    if  not os.path.exists(archivo):
        return False
    arch = open(archivo, "r")
    cadena = []
    for linea in arch: 
        for c in linea: 
            cadena += c
    arch.close()
    return cadena



######################
#####            #####
#####    Main    #####
#####            #####
######################

#Comprueba si se introdujo un texto
if len(sys.argv) == 2:
    cadena = transforma(sys.argv[1])
    if (not cadena):
        print("Error al leer el archivo. No existe. Error 404")
    else :
        lexico(cadena)
#Comprueba si no se intodujo texto
elif len(sys.argv) == 1:
    cadena =[]
    print("Para terminar esciba 'ok'")
    while True:
        escrito = input('>>')
        if escrito != 'ok':
            cadena += escrito + '\n'
        else: break
    lexico(cadena)
#Manda error si no se cumple lo anterior    
else:
    print("Error de ejecución")