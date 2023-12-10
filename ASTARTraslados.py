import lector
import sys


if len(sys.argv) < 3:
    print("numero de argumentos no valido")
    sys.exit(1)


class Nodo:
    def __init__(self, valor, apuntando):
        self.valor = valor
        self.puntero = apuntando


class Grafo:
    def __init__(self, nodos: list):
        self.nodos = nodos

    def añadir(self, nodo):
        self.nodos.append(nodo)


class Estado:
    def __init__(self, mapa: list, transporte: tuple, energia: int):
        self.mapa = mapa
        self.transporte = transporte
        self.energia = energia

    def __eq__(self, other):
        ...

    def expandir(self) -> list:
        ...


def heuristica_1():
    return 4


def generar_e_final(e_inicial: list) -> list:
    e_final = []
    for el in e_inicial:
        lista = []
        for e in el:
            if e in ["C", "N"]:
                lista.append("1")
            else:
                lista.append(e)
        e_final.append(lista)
    return e_final


def localizar_parking(mapa: list) -> tuple:
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[i][j] == "P":
                return i, j


def a_estella(estado_inicial: Estado, estado_final: Estado):
    G = Grafo([estado_inicial])
    abierta = [estado_inicial]
    cerrada = [estado_final]
    falso = False
    while len(abierta) or falso:
        n = abierta[0]
        abierta.__delitem__(0)
        cerrada.append(n)
        if estado_final.__eq__(n):
            falso = True
        else:
            S = n.expandir()
            for s in S:
                G.añadir(Nodo(s, n))


inicial = lector.leer(sys.argv[1])
final = generar_e_final(inicial)

I = Estado(inicial, localizar_parking(inicial), 50)
F = Estado(final, localizar_parking(inicial), 50)

a_estella(I, F)

print(final)
