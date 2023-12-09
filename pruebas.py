import time
from constraint import *
ti = time.time()


def imp_sol(z):
    print(len(z))

    print(z)

    tf = time.time()

    print(tf - ti)


def restr4(a, b):
    if a[1] == b[1]:
        return a[2] > b[2]
    return True


def __restr5(a, b, x_max=3):
    return not (a[2] == b[2] and contiguos(a, b) and (int(a[1]) in [1, x_max] or int(b[1]) in [0, x_max]))


def contiguos(a, b):
    return int(a[1]) == int(b[1])+1 or int(a[1]) == int(b[1])-1


def _restr5(a, b, c):
    if contiguos(a, b) and contiguos(c, b):
        return False
    return True


def restr5(a, b, c):
    if a[2] == b[2] == c[2]:
        return _restr5(a, b, c) and _restr5(b, c, a) and _restr5(c, a, b)
    return True


problem = Problem()

vehiculos = ["1-TSU-C", "2-TNU-X", "3-TNU-X", "4-TNU-C", "5-TSU-X", "6-TNU-X", "7-TNU-C", "8-TSU-C"]

dominio = []
for i in range(1, 6):
    for j in range(1, 7):
        dominio.append("X" + str(i) + str(j))

dominio_reducido = [dominio[0], dominio[1], dominio[6], dominio[18], dominio[24], dominio[25]]
print(dominio)
print(dominio_reducido)

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

# Restriccion 4 Un vehiculo de tipo TSU no puede tener aparcado por delante, en su misma fila, a ningun otro vehiculo
# excepto si este es tambien de este tipo
for v in vehiculos:
    if v[2:5] == "TSU":
        for v2 in vehiculos:
            if v2[2:5] == "TNU":
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


imp_sol(problem.getSolutions())



