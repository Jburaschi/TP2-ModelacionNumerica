import numpy as np



def parsear_segundos(fecha_str, hora_str):
    anio, mes, dia = map(int, fecha_str.split("/"))
    
    partes_hora = hora_str.split(":")
    hora   = int(partes_hora[0])
    minuto = int(partes_hora[1])
    segundo = float(partes_hora[2])
    seg_int  = int(segundo)
    microseg = int(round((segundo - seg_int) * 1_000_000))

    dt = datetime.datetime(anio, mes, dia, hora, minuto, seg_int, microseg)
    
    return dt.timestamp()

def cargar_datos(nombre_archivo):

    datos = np.genfromtxt(
        nombre_archivo,
        dtype=str
    )

    cantidad = len(datos)

    t = np.zeros(cantidad)
    x = np.zeros(cantidad)
    y = np.zeros(cantidad)
    z = np.zeros(cantidad)

    for i in range(cantidad):

        t[i] = parsear_segundos(
            datos[i][0],
            datos[i][1]
        )

        x[i] = float(datos[i][2])
        y[i] = float(datos[i][3])
        z[i] = float(datos[i][4])

    # Tiempo relativo al primer instante
    t = t - t[0]

    return t, x, y, z