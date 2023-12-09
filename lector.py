import csv


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

def escribir(archivo: str) -> None:
