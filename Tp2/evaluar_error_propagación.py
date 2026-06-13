import numpy as np
import matplotlib.pyplot as plt

from lector_telemetria import leer_telemetria_satelital 
from spline import SplineNatural
from propagador import propagar

def evaluar_desviacion_orbital():
    t600, x600, y600, z600, vx600, vy600, vz600 = leer_telemetria_satelital("SACD_TPV_step_600s.txt")

    # Condición inicial t=0
    pos_inicial = [x600[0], y600[0], z600[0]]
    vel_inicial = [vx600[0], vy600[0], vz600[0]]

    # 1 periodo orbital aproximado (110 min = 6600 segundos)
    periodo_segundos = 110 * 60

    # Propagar paso de 600s 
    paso_grueso = 600.0
    n_pasos_grueso = int(periodo_segundos / paso_grueso)
    trayectoria_600 = propagar(pos_inicial, vel_inicial, paso_grueso, n_pasos_grueso)
    t_prop_600 = np.linspace(0, n_pasos_grueso * paso_grueso, n_pasos_grueso + 1)

    #  Interpolar 
    spline_prop_x = SplineNatural(t_prop_600, trayectoria_600[:, 0])
    spline_prop_y = SplineNatural(t_prop_600, trayectoria_600[:, 1])
    spline_prop_z = SplineNatural(t_prop_600, trayectoria_600[:, 2])

  
    mascara_tiempo = t600 <= periodo_segundos
    spline_gps_x = SplineNatural(t600[mascara_tiempo], x600[mascara_tiempo])
    spline_gps_y = SplineNatural(t600[mascara_tiempo], y600[mascara_tiempo])
    spline_gps_z = SplineNatural(t600[mascara_tiempo], z600[mascara_tiempo])

    t_evaluacion = np.linspace(0, periodo_segundos, int(periodo_segundos) + 1)
    deriva_vs_gps = np.zeros(len(t_evaluacion))

   # diferencia de norma 
    for i, t in enumerate(t_evaluacion):
        pos_calculada = np.array([spline_prop_x.evaluar(t), spline_prop_y.evaluar(t), spline_prop_z.evaluar(t)])
        pos_real_gps  = np.array([spline_gps_x.evaluar(t), spline_gps_y.evaluar(t), spline_gps_z.evaluar(t)])
        deriva_vs_gps[i] = np.linalg.norm(pos_calculada - pos_real_gps)

    # Propaga con RK4 a paso fino de 1s
    paso_fino = 1.0
    n_pasos_fino = int(periodo_segundos / paso_fino)
    trayectoria_fina = propagar(pos_inicial, vel_inicial, paso_fino, n_pasos_fino)

    deriva_paso_grueso_fino = np.zeros(len(t_evaluacion))
    
    for i, t in enumerate(t_evaluacion):
        pos_gruesa_interp = np.array([spline_prop_x.evaluar(t), spline_prop_y.evaluar(t), spline_prop_z.evaluar(t)])
        pos_fina = trayectoria_fina[i, :3]
        deriva_paso_grueso_fino[i] = np.linalg.norm(pos_gruesa_interp - pos_fina)

    # Gráficos
    fig, axs = plt.subplots(2, 1, figsize=(10, 10))

    axs[0].plot(t_evaluacion, deriva_vs_gps, color='crimson')
    axs[0].set_title("Deriva: Modelo RK4 (Paso 600s) vs Telemetría GPS Real")
    axs[0].set_ylabel("Error de Posición [km]")
    axs[0].grid(True)

    axs[1].plot(t_evaluacion, deriva_paso_grueso_fino, color='teal')
    axs[1].set_title("Error por Discretización: RK4 (600s) vs RK4 (1s)")
    axs[1].set_ylabel("Diferencia de Posición [km]")
    axs[1].set_xlabel("Tiempo Transcurrido [s]")
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig("analisis_desviacion_orbital.png")
    plt.show()

