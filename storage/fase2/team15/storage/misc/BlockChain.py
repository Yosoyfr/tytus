import hashlib
import json as js
import os
import subprocess


def GenerarHash(cadena):
    return hashlib.sha256(cadena.encode()).hexdigest()


def CreateBlockChain(nombreTabla, ruta):

    ruta = ruta + "\\SafeTables\\" + str(nombreTabla) + ".json"
    file = open(ruta, "w+")
    file.write(js.dumps(['inicio']))
    file.close()


def EsUnaTablaSegura(nombreTabla, ruta):
    ruta = ruta + "\\SafeTables\\" + str(nombreTabla) + ".json"
    return os.path.isfile(ruta)


def updateSafeTable(nombreTabla, datos, datosmodificados, ruta):
    cadena = ''
    cadenaModificcada = ''
    contador = 0
    ruta = ruta + "\\SafeTables\\" + str(nombreTabla) + ".json"

    for dato in datos:
        if contador == len(datos) - 1:
            cadena += str(dato)
        else:
            cadena += (str(dato) + ',')
        contador += 1
    contador = 0

    for dato in datosmodificados:
        if contador == len(datos) - 1:
            cadenaModificcada += str(dato)
        else:
            cadenaModificcada += (str(dato) + ',')
        contador += 1

    file = open(ruta, "r")
    lista = js.loads(file.read())
    file.close()

    for bloque in lista:
        if cadena == bloque[1]:
            bloque[1] = cadenaModificcada
            bloque[3] = GenerarHash(cadenaModificcada)
            file = open(ruta, "w+")
            file.write(js.dumps(lista))
            file.close()
            return True


def insertSafeTable(nombreTabla, datos, ruta):
    cadena = ''
    contador = 0
    ruta = ruta + "\\SafeTables\\" + str(nombreTabla) + ".json"

    for dato in datos:
        if contador == len(datos) - 1:
            cadena += str(dato)
        else:
            cadena += (str(dato) + ',')
        contador += 1

    file = open(ruta, "r")
    lista = js.loads(file.read())
    file.close()

    id = len(lista)
    h = GenerarHash(cadena)
    if id == 1 and lista[0] == 'inicio':
        DatosBloque = [id, cadena, '000000000000000000', h]
        lista.pop()
    else:
        DatosBloque = [id, cadena, lista[id-1][3], h]
    lista.append(DatosBloque)
    file = open(ruta, "w+")
    file.write(js.dumps(lista))
    file.close()


def GraphSafeTable(nombreTabla, ruta):
    ruta = ruta + "\\SafeTables\\" + str(nombreTabla) + ".json"
    file = open(ruta, "r")
    lista = js.loads(file.read())
    file.close()

    file = open('BlockChain.dot', "w")
    file.write("graph grafica{" + os.linesep)
    file.write("rankdir=LR;" + os.linesep)
    contador = 0
    correcta = True
    for bloque in lista:
        if correcta:
            if contador == len(lista)-1:
                file.write('bloque' + str(
                    contador) + ' [shape=record, style=bold,style=filled,fillcolor=lightblue,label="ID:\\n' + str(
                    bloque[0]) + ' | DATOS:\\n' + str(bloque[1]) + ' | ANTERIOR:\\n' + str(
                    bloque[2]) + ' | HASH:\\n' + str(bloque[3]) + '"];' + os.linesep)
            elif bloque[3] == lista[contador + 1][2]:
                file.write('bloque' + str(
                    contador) + ' [shape=record, style=bold,style=filled,fillcolor=lightblue,label="ID:\\n' + str(
                    bloque[0]) + ' | DATOS:\\n' + str(bloque[1]) + ' | ANTERIOR:\\n' + str(
                    bloque[2]) + ' | HASH:\\n' + str(bloque[3]) + '"];' + os.linesep)
            else:
                file.write('bloque' + str(
                    contador) + ' [shape=record, style=bold,style=filled,fillcolor=pink,label="ID:\\n' + str(
                    bloque[0]) + ' | DATOS:\\n' + str(bloque[1]) + ' | ANTERIOR:\\n' + str(
                    bloque[2]) + ' | HASH:\\n' + str(bloque[3]) + '"];' + os.linesep)
                correcta = False
        else:
            file.write('bloque' + str(
                contador) + ' [shape=record, style=bold,style=filled,fillcolor=pink,label="ID:\\n' + str(
                bloque[0]) + ' | DATOS:\\n' + str(bloque[1]) + ' | ANTERIOR:\\n' + str(
                bloque[2]) + ' | HASH:\\n' + str(bloque[3]) + '"];' + os.linesep)

        contador += 1

    for i in range(len(lista)):
        if not i == len(lista)-1:
            file.write('bloque' + str(i) + ' -- bloque' + str(i + 1) + os.linesep)

    file.write('}')
    file.close()
    subprocess.call('dot -Tpng BlockChain.dot -o BlockChain.png')
    os.system('BlockChain.png')
