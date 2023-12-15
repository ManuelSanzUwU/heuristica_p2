import lector
import sys
import time
import heapq

ti = time.time()


def tiempo():
    tf = time.time()
    return tf - ti


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
            for j in range(len(self.mapa[i])):
                if not other.mapa[i][j] == self.mapa[i][j]:
                    return False

        for i in range(2):
            if not other.transporte[i] == self.transporte[i]:
                return False

        if len(other.transporte[2]) == len(self.transporte[2]):
            for i in range(len(self.transporte[2])):
                if not other.transporte[2].count("N") == self.transporte[2].count("N") \
                        and not other.transporte[2].count("C") == self.transporte[2].count("C"):
                    return False
        else:
            return False

        return self.energia == other.energia

    def copiar_mapa(self) -> list:
        m = []
        for lista in self.mapa:
            m.append(lista.copy())
        return m


class Nodo:
    def __init__(self, valor: Estado, apuntando, c: int):
        self.valor = valor
        self.puntero = apuntando
        self.c = c

    def __lt__(self, other):
        return f(self) < f(other)

    def __str__(self):
        return str(self.valor.mapa) + str(self.valor.transporte) + "e: " + str(self.valor.energia) + ", c:" + str(self.c)

    def __eq__(self, other):
        return self.valor.__eq__(other.valor)

    def coste_e(self):
        if self.puntero is None:
            return self.coste_e2()
        else:
            return self.puntero.coste_e() + self.coste_e2()

    def coste_e2(self):
        z = self.valor.mapa[self.valor.transporte[0]][self.valor.transporte[1]]
        if z == "P":
            return 0
        elif z.isdigit():
            return int(z)
        else:
            return 1

    def impr_sol(self) -> list:
        if self.puntero is None:
            return [self.impr_sol2()]
        else:
            return self.puntero.impr_sol() + [self.impr_sol2()]

    def impr_sol2(self) -> str:
        a = "(" + str(self.valor.transporte[0]) + "," + str(self.valor.transporte[1]) + ")"
        b = self.valor.mapa[self.valor.transporte[0]][self.valor.transporte[1]]
        c = str(self.valor.energia)
        return a + ":" + b + ":" + c

    def expandir(self) -> list:
        z = [Nodo(self.mover_a((self.valor.transporte[0]+1, self.valor.transporte[1],
                                self.valor.transporte[2].copy())), None, self.c + 1),
             Nodo(self.mover_a((self.valor.transporte[0]-1, self.valor.transporte[1],
                                self.valor.transporte[2].copy())), None, self.c + 1),
             Nodo(self.mover_a((self.valor.transporte[0], self.valor.transporte[1]+1,
                                self.valor.transporte[2].copy())), None, self.c + 1),
             Nodo(self.mover_a((self.valor.transporte[0], self.valor.transporte[1]-1,
                                self.valor.transporte[2].copy())), None, self.c + 1)]
        j = 0
        for i in range(len(z)):
            if z[i-j].valor is None:
                z.__delitem__(i-j)
                j += 1
        return z

    def coste(self) -> int:
        if self.puntero is not None:
            return self.puntero.coste()
        else:
            return 0

    def apuntar(self, obj) -> None:
        self.puntero = obj

    def mover_a(self, tr):
        if tr[0] < 0 or tr[1] < 0:
            return None
        if len(self.valor.mapa) <= tr[0] or len(self.valor.mapa[tr[0]]) <= tr[1]:
            return None
        z = self.valor.mapa[tr[0]][tr[1]]
        mapa = self.valor.copiar_mapa()
        e = self.valor.energia
        if z.isdigit():
            e -= int(z)
        else:
            if z == "N":
                if len(tr[2]) < 10 and "C" not in tr[2]:
                    tr[2].append("N")
                    mapa[tr[0]][tr[1]] = "1"
                e -= 1
            elif z == "C":
                if tr[2].count("N") <= 8 and tr[2].count("C") < 2:
                    tr[2].append("C")
                    mapa[tr[0]][tr[1]] = "1"
                e -= 1
            elif z == "CN":
                if "C" not in tr[2]:
                    tr[2].clear()
                e -= 1
            elif z == "CC":
                for i in range(tr[2].count("C")):
                    tr[2].pop(tr[2].index("C"))
                e -= 1
            elif z == "X":
                return None
            elif z == "P":
                e = 50
        if e <= 0:
            return None

        r = Estado(mapa, tr, e)
        return r


class Grafo:
    def __init__(self, nodos: list):
        self.nodos = nodos

    def añadir(self, nodo):
        self.nodos.append(nodo)

    def long(self):
        return len(self.nodos)


def f(nodo: Nodo):
    return heuristica(nodo) + nodo.c


def heuristica(nodo: Nodo):
    if sys.argv[2] == "1":
        return heuristica_1(nodo)
    elif sys.argv[2] == "2":
        return heuristica_2(nodo)
    else:
        return heuristica_sin_informar()


def heuristica_sin_informar():
    return 50


def heuristica_1(nodo: Nodo):
    estado = nodo.valor
    n = 0
    c = 0
    for i in range(len(estado.mapa)):
        for j in range(len(estado.mapa[i])):
            if estado.mapa[i][j] == "N":
                n += 1
            elif estado.mapa[i][j] == "C":
                c += 1
    return (n + c)*10 + len(estado.transporte[2])


def calc_distancia(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def heuristica_2(nodo: Nodo):
    distancia = 0
    estado = nodo.valor
    for i in range(len(estado.mapa)):
        for j in range(len(estado.mapa[i])):
            if estado.mapa[i][j] == "N":
                distancia += calc_distancia(estado.transporte, (i, j))
            elif estado.mapa[i][j] == "C":
                distancia += calc_distancia(estado.transporte, (i, j))
    return distancia


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
                return i, j, []


def esta(nodo, lista) -> bool:
    for e in lista:
        if e.__eq__(nodo):
            return True
    return False


def a_estella(estado_inicial: Estado, estado_final: Estado):
    I = Nodo(estado_inicial, None, 0)
    G = Grafo([I])
    abierta = [I]
    heapq.heapify(abierta)
    cerrada = []
    falso = False
    iteracion = 0
    sol = None
    while len(abierta) and not falso:
        n = heapq.heappop(abierta)
        appends = []
        if estado_final.__eq__(n.valor):
            falso = True
            sol = n
        else:
            S = n.expandir()
            cerrada.append(n)
            for s in S:
                if not(esta(s, abierta) or esta(s, cerrada)):
                    G.añadir(s.apuntar(n))
                    appends.append(s)
                elif esta(s, abierta):
                    for i in range(len(abierta)):
                        if abierta[i].__eq__(s):
                            if f(s) < f(abierta[i]):
                                G.añadir(s.apuntar(n))
                                abierta.remove(abierta[i])
                                heapq.heapify(abierta)
                                heapq.heappush(abierta, s)
                                break

            lista = []
            for append in appends:
                heapq.heappush(abierta, append)

        iteracion += 1

    print(falso)
    if falso:
        print(iteracion)
        mapa = sys.argv[1][:len(sys.argv[1])-4]
        lector.escribir_para_aestrella(mapa + "-" + str(sys.argv[2] + ".output"), sol.impr_sol())
        lector.escribir_para_aestrella2(mapa + "-" + str(sys.argv[2] + ".stat"), [tiempo(), sol.coste_e(), sol.c, G.long()])


inicial = lector.leer(sys.argv[1])
final = generar_e_final(inicial)

I = Estado(inicial, localizar_parking(inicial), 50)
F = Estado(final, localizar_parking(inicial), 50)

a_estella(I, F)