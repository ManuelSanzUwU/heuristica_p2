import csv
import random


def leer(archivo: str) -> tuple:
    with open(archivo) as csvfile:
        datos = []
        todo = csv.reader(csvfile, delimiter=" ")
        for row in todo:
            datos.append(row)
        if len(datos) < 3:
            ...
        x = int(datos[0][0][0])
        y = int(datos[0][0][2])

        plazas_carga = datos[1][1:]

        v = []
        for ve in datos[2:]:
            v.append(ve[0])

        r = ((x, y), plazas_carga, v)

        return r


def escribir(archivo: str, resultados) -> None:
    with open(archivo, 'w', newline='') as csvfile:
        escritor = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        escritor.writerow(["N. Sol:", len(resultados[1])])
        resultado = resultados[1][random.randint(0, len(resultados[1])-1)]
        for i in range(1, resultados[0][0] + 1):
            linea = []
            for j in range(1, resultados[0][1] + 1):
                falso = True
                for res in resultado:
                    if int(resultado[res][1]) == i and int(resultado[res][3]) == j:
                        linea.append(res)
                        falso = False
                if falso:
                    linea.append("-")
            escritor.writerow(linea)

