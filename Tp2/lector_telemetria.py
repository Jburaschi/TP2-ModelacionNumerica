import datetime
import numpy as np

def convertir_a_tiempo_absoluto(fecha_str, hora_str):

    anio, mes, dia = map(int, fecha_str.split("/"))
    hora, minuto, segundo_str = hora_str.split(":")
    
    hora = int(hora)
    minuto = int(minuto)
    segundo_float = float(segundo_str)
    
    seg_int = int(segundo_float)
    microseg = int(round((segundo_float - seg_int) * 1_000_000))

    dt = datetime.datetime(anio, mes, dia, hora, minuto, seg_int, microseg)
    return dt.timestamp()

def leer_telemetria_satelital(ruta_archivo):

    datos_crudos = np.genfromtxt(ruta_archivo, dtype=str)
    cantidad_filas = len(datos_crudos)

    t = np.zeros(cantidad_filas)
    pos = np.zeros((cantidad_filas, 3))
    vel = np.zeros((cantidad_filas, 3))

    for i in range(cantidad_filas):
        # Col 0 y 1: Fecha y Hora
        t[i] = convertir_a_tiempo_absoluto(datos_crudos[i][0], datos_crudos[i][1])
        
        # Col 2, 3, 4: Pos (X, Y, Z)
        pos[i, 0] = float(datos_crudos[i][2])
        pos[i, 1] = float(datos_crudos[i][3])
        pos[i, 2] = float(datos_crudos[i][4])
        
        # Col 5, 6, 7: Vel (VX, VY, VZ)
        vel[i, 0] = float(datos_crudos[i][5])
        vel[i, 1] = float(datos_crudos[i][6])
        vel[i, 2] = float(datos_crudos[i][7])

    # (t=0)
    t_relativo = t - t[0]

    return t_relativo, pos[:, 0], pos[:, 1], pos[:, 2], vel[:, 0], vel[:, 1], vel[:, 2]
