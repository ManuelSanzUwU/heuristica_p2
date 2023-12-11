import lector
import sys


if len(sys.argv) < 3:
    print("numero de argumentos no valido")
    sys.exit(1)


class Estado:
    def __init__(self, mapa: list, transporte: tuple, energia: int):
        self.mapa = mapa
        self.transporte = transporte
        self.energia = energia

    def __eq__(self, other):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa)):
                if not other.mapa[i][j] == self.mapa[i][j]:
                    return False

        for i in range(2):
            if not other.transporte[i] == self.transporte[i]:
                return False

        return self.energia == other.energia


class Nodo:
    def __init__(self, valor, apuntando):
        self.valor = valor
        self.puntero = apuntando

    def __eq__(self, other):
        self.valor.__eq__(other.valor)

    def expandir(self) -> list:
        z = [Nodo(self.mover_a((self.valor.transporte[0]+1, self.valor.transporte[1])), None),
             Nodo(self.mover_a((self.valor.transporte[0]-1, self.valor.transporte[1])), None),
             Nodo(self.mover_a((self.valor.transporte[0], self.valor.transporte[1]+1)), None),
             Nodo(self.mover_a((self.valor.transporte[0], self.valor.transporte[1]-1)), None)]
        j = 0
        for i in range(len(z)):
            if z[i-j].valor is None:
                j+=1
                z.__delitem__(i-j)
        return z

    def coste(self) -> int:
        if self.puntero is not None:
            return self.puntero.coste()
        else:
            return 0

    def apuntar(self, obj) -> None:
        self.puntero = obj

    def mover_a(self, tr):
        if len(self.valor.mapa) <= tr[0] or len(self.valor.mapa[tr[0]]) <= tr[1]:
            return None
        z = self.valor.mapa[tr[0]][tr[1]]
        e = self.valor.energia
        if z.isdigit():
            e -= int(z)
        return Estado(self.valor.mapa, tr, e)


class Grafo:
    def __init__(self, nodos: list):
        self.nodos = nodos

    def añadir(self, nodo):
        self.nodos.append(nodo)

    def contiene(self, estado) -> bool:
        """recibe un estado y devuleve true si el estado ya esta presente en el grafo"""


def heuristica_1(estado):
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
    I = Nodo(estado_inicial, None)
    G = Grafo([I])
    abierta = [I]
    cerrada = []
    falso = False
    while len(abierta) or falso:
        n = abierta[0]
        abierta.__delitem__(0)
        cerrada.append(n)
        if estado_final.__eq__(n.valor):
            falso = True
        else:
            S = n.expandir()
            for s in S:
                if not G.contiene(s):
                    G.añadir(s.apuntar(n))
                esta = False
                for e in abierta:
                    if e.__eq__(s):
                        if s.coste() < e.coste():
                            e.apuntar(n)
                            esta = True
                if not esta:
                    abierta.append(s)

                esta = False
                for e in cerrada:
                    if e.__eq__(s):
                        if s.coste() < e.coste():
                            e.apuntar(n)
                            esta = True
                if not esta:
                    cerrada.append(s)

            lista = []
            for i in range(len(abierta)):
                min = heuristica_1(abierta[0])
                z = 0
                for j in range(len(abierta)):
                    if heuristica_1(abierta[j]) < min:
                        z = j
                lista.append(abierta[z])
            abierta = lista
        print(abierta)

    print(falso)


inicial = lector.leer(sys.argv[1])
final = generar_e_final(inicial)

I = Estado(inicial, localizar_parking(inicial), 50)
F = Estado(final, localizar_parking(inicial), 50)

a_estella(I, F)

