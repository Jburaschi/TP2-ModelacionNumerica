import numpy as np
import matplotlib.pyplot as plt

from lector import cargar_datos
from spline import SplineNatural


def comparar_spline_vs_real():

    # Datos cada 600 s (para construir la spline)
    t600, x600, y600, z600 = cargar_datos(
        "SACD_TPV_step_600s.txt"
    )

    # Datos cada 1 s (referencia "real")
    t1, x1, y1, z1 = cargar_datos(
        "SACD_TPV_step_1s.txt"
    )

    # Construir spline con datos cada 600 s
    sx = SplineNatural(t600, x600)
    sy = SplineNatural(t600, y600)
    sz = SplineNatural(t600, z600)

    # Filtrar solo 1 periodo orbital
    periodo = 110 * 60

    mascara = t1 <= periodo

    t_eval = t1[mascara]
    x_real = x1[mascara]
    y_real = y1[mascara]
    z_real = z1[mascara]

    # Evaluar spline en cada segundo
    x_spline = np.zeros(len(t_eval))
    y_spline = np.zeros(len(t_eval))
    z_spline = np.zeros(len(t_eval))

    for i in range(len(t_eval)):
        x_spline[i] = sx.evaluar(t_eval[i])
        y_spline[i] = sy.evaluar(t_eval[i])
        z_spline[i] = sz.evaluar(t_eval[i])

    # Calcular errores
    error_x = x_spline - x_real
    error_y = y_spline - y_real
    error_z = z_spline - z_real

    # Grafico de errores
    plt.figure(figsize=(12, 6))

    plt.plot(t_eval, error_x, label="Error X")
    plt.plot(t_eval, error_y, label="Error Y")
    plt.plot(t_eval, error_z, label="Error Z")

    plt.title(
        "Error de interpolacion: spline (600s) vs posiciones reales (1s)"
    )
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Error [km]")
    plt.legend()
    plt.grid()

    plt.savefig("error_interpolacion.png")
    plt.show()

    # Errores maximos
    print("\nErrores maximos de interpolacion:")
    print(f"  Error maximo X = {np.max(np.abs(error_x)):.6f} km")
    print(f"  Error maximo Y = {np.max(np.abs(error_y)):.6f} km")
    print(f"  Error maximo Z = {np.max(np.abs(error_z)):.6f} km")

    print(
        "\nObservacion: los errores son del orden de decimas de km,"
        " mayores en los intervalos donde la orbita tiene mayor curvatura."
        " La spline cubica natural reproduce bien la trayectoria"
        " con muestras cada 10 minutos."
    )