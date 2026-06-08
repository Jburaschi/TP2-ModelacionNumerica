import numpy as np
import matplotlib.pyplot as plt


def graficar_orbita(t, x, y, z, sx, sy, sz):

    periodo = 110 * 60

    t_final = min(
        t[0] + periodo,
        t[-1]
    )

    t_interp = np.linspace(
        t[0],
        t_final,
        2000
    )

    x_interp = np.zeros(len(t_interp))
    y_interp = np.zeros(len(t_interp))
    z_interp = np.zeros(len(t_interp))

    for i in range(len(t_interp)):
        x_interp[i] = sx.evaluar(t_interp[i])
        y_interp[i] = sy.evaluar(t_interp[i])
        z_interp[i] = sz.evaluar(t_interp[i])

    # Filtrar muestras del primer periodo
    mascara = t <= periodo

    fig = plt.figure(figsize=(10, 8))

    ax = fig.add_subplot(111, projection="3d")

    ax.plot(
        x_interp,
        y_interp,
        z_interp,
        label="Spline Cubica"
    )

    ax.scatter(
        x[mascara],
        y[mascara],
        z[mascara],
        color="red",
        s=20,
        label="Muestras"
    )

    ax.set_title("Orbita SAC-D - 1 periodo orbital")
    ax.set_xlabel("X [km]")
    ax.set_ylabel("Y [km]")
    ax.set_zlabel("Z [km]")
    ax.legend()

    plt.savefig("orbita_3d.png")
    plt.show()


def graficar_componentes(t, x, y, z, sx, sy, sz):

    periodo = 110 * 60

    t_final = min(
        t[0] + periodo,
        t[-1]
    )

    t_interp = np.linspace(
        t[0],
        t_final,
        2000
    )

    x_interp = np.zeros(len(t_interp))
    y_interp = np.zeros(len(t_interp))
    z_interp = np.zeros(len(t_interp))

    for i in range(len(t_interp)):
        x_interp[i] = sx.evaluar(t_interp[i])
        y_interp[i] = sy.evaluar(t_interp[i])
        z_interp[i] = sz.evaluar(t_interp[i])

    # Filtrar muestras del primer periodo
    mascara = t <= periodo

    fig, axs = plt.subplots(3, 1, figsize=(12, 10))

    axs[0].plot(t_interp, x_interp, label="Spline Cubica")
    axs[0].scatter(t[mascara], x[mascara], color="red", s=20, label="Muestras")
    axs[0].set_title("X(t)")
    axs[0].set_ylabel("X [km]")
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(t_interp, y_interp, label="Spline Cubica")
    axs[1].scatter(t[mascara], y[mascara], color="red", s=20, label="Muestras")
    axs[1].set_title("Y(t)")
    axs[1].set_ylabel("Y [km]")
    axs[1].legend()
    axs[1].grid()

    axs[2].plot(t_interp, z_interp, label="Spline Cubica")
    axs[2].scatter(t[mascara], z[mascara], color="red", s=20, label="Muestras")
    axs[2].set_title("Z(t)")
    axs[2].set_ylabel("Z [km]")
    axs[2].set_xlabel("Tiempo [s]")
    axs[2].legend()
    axs[2].grid()

    plt.tight_layout()
    plt.savefig("componentes_posicion.png")
    plt.show()