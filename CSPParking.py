import time
import lector
import sys
from constraint import *
ti = time.time()


if len(sys.argv) < 2:
    print("numero de argumentos no valido")
    sys.exit(1)


def restr4(a, b):
    """si un TSU y un TNU estan en la misma fila, el TNU debe estar detras"""
    if a[1] == b[1]:
        return a[3] > b[3]
    return True


def contiguos(a, b):
    """recibe dos coordenadas y devuelve true si son congiguos o false si no, se asume q si se llama a esta
    funcion ya se a comprobado q estan en la misma columna"""
    return int(a[1]) == int(b[1])+1 or int(a[1]) == int(b[1])-1


def _restr5(a, b, c):
    """se asegura de que un vehiculo b no es contiguo con a y c al mismo tiempo"""
    if contiguos(a, b) and contiguos(c, b):
        return False
    return True


def restr5(a, b, c):
    """para tres variables se asegura de que ninguna esta justo entre las otras 2"""
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
        """si a y b son contiguos, tienen la misma Y """
        return not (a[3] == b[3] and contiguos(a, b) and (int(a[1]) in [1, x_max] or int(b[1]) in [0, x_max]))

    problem = Problem()

    dominio = []
    for i in range(1, x_max + 1):
        for j in range(1, y_max + 1):
            dominio.append("(" + str(i) + "," + str(j) + ")")

    dominio_reducido = []
    for el in dominio:
        if el in plazas_carga:
            dominio_reducido.append(el)

    for v in vehiculos:
        if v[6] == "X":
            problem.addVariable(v, dominio)
        else:
            problem.addVariable(v, dominio_reducido)

    """
    Restriccion 1 todo vehiculo debe tener asignada una plaza y solo una
    (contemplada por el dominio de los valores de los vehiculos)
    """

    """
    Restriccion 2 Dos vehiculos distintos no pueden ocupar la misma plaza
    """
    problem.addConstraint(AllDifferentConstraint())

    """
    Restriccion 3 Los vehiculos provistos de congelador solo pueden ocupar plazas con conexion a la red electrica
    contemplada al crear los dominios de las variables
    """

    """ 
    Restriccion 4 Un vehiculo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningun otro vehiculo
    excepto si este es tambien de este tipo
    se recorre la lista vehículos localizando los vehículos TSU y para cada TSU se recorre la lista localizando los TNU,
    se establece una condición entre cada par TSU-TNU que garantiza la resticcion, esta explicda en la funcion restr4
    """
    for v in vehiculos:
        if v[3] == "S":
            for v2 in vehiculos:
                if v2[3] == "N":
                    problem.addConstraint(restr4, (v, v2))

    """
    Restriccion 5 Por cuestiones de maniobrabilidad dentro del parking
    todo vehiculo debe tener libre una plaza a izquierda o derecha
    el primer bucle recorre la lista de vehiculos y para cada par de vehiculos, se asegura de q no son adyacentes
    si uno de ellos esta en el borde superior o inferior (__restr5)
    el segundo bucle busca todas las combinaciones posibles de 3 vehiculos distintos y establece la restriccion de que
    no puede uno de ellos ser contiguo a los otros dos (restr5)
    """
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
