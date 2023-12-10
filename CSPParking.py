import random
import time
import lector
import sys
from constraint import *
ti = time.time()


if len(sys.argv) < 2:
    print("numero de argumentos no valido")
    sys.exit(1)


def imp_sol(z):
    print(len(z))
    print(z[random.randint(0, len(z) - 1)])

    tf = time.time()
    print(tf - ti)


def restr4(a, b):
    if a[1] == b[1]:
        return a[3] > b[3]
    return True


def contiguos(a, b):
    return int(a[1]) == int(b[1])+1 or int(a[1]) == int(b[1])-1


def _restr5(a, b, c):
    if contiguos(a, b) and contiguos(c, b):
        return False
    return True


def restr5(a, b, c):
    if a[3] == b[3] == c[3]:
        return _restr5(a, b, c) and _restr5(b, c, a) and _restr5(c, a, b)
    return True


def resolver_problema(path_entrada: str):
    datos = lector.leer(path_entrada)
    x_max = datos[0][0]
    y_max = datos[0][1]
    plazas_carga = datos[1]
    vehiculos = datos[2]

    def __restr5(a, b):
        return not (a[3] == b[3] and contiguos(a, b) and (int(a[1]) in [1, x_max] or int(b[1]) in [0, x_max]))

    problem = Problem()

    dominio = []
    for i in range(1, x_max + 1):
        for j in range(1, y_max + 1):
            dominio.append("(" + str(i) + "," + str(j) + ")")

    dominio_reducido = []  # igual se puede eliminar esto
    for el in dominio:
        if el in plazas_carga:
            dominio_reducido.append(el)

    for v in vehiculos:
        if v[6] == "X":
            problem.addVariable(v, dominio)
        else:
            problem.addVariable(v, dominio_reducido)

    # Restriccion 1 todo vehiculo debe tener asignada una plaza y solo una
    # (contemplada por el dominio de los valores de los vehiculos)

    # Restriccion 2 Dos vehiculos distintos no pueden ocupar la misma plaza
    problem.addConstraint(AllDifferentConstraint())

    # Restriccion 3 Los vehiculos provistos de congelador solo pueden ocupar plazas con conexion a la red electrica
    # contemplada al crear los dominios de las variables

    # Restriccion 4 Un vehiculo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningun otro
    # vehiculo excepto si este es tambien de este tipo
    for v in vehiculos:
        if v[3] == "S":
            for v2 in vehiculos:
                if v2[3] == "N":
                    problem.addConstraint(restr4, (v, v2))

    # Restriccion 5 Por cuestiones de maniobrabilidad dentro del parking
    # todo vehiculo debe tener libre una plaza a izquierda o derecha
    if len(vehiculos) > 1:
        for i in range(len(vehiculos)):
            for j in range(len(vehiculos)):
                if i != j:
                    problem.addConstraint(__restr5, (vehiculos[i], vehiculos[j]))

    if len(vehiculos) > 2:
        for i in range(len(vehiculos)):
            for j in range(len(vehiculos)):
                for k in range(len(vehiculos)):
                    if i != j != k != i:
                        problem.addConstraint(restr5, (vehiculos[i], vehiculos[j], vehiculos[k]))

    return (x_max, y_max), problem.getSolutions()


path = sys.argv[1]
lector.escribir(path[:len(path)-3] + "csv", resolver_problema(path))
