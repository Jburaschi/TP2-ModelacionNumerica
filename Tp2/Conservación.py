import numpy as np
import matplotlib.pyplot as plt
from propagador import propagar, orbitas, G

def analizar_conservacion_magnitudes():
    paso_h = 1.0
    # 24 horas paso 1s
    n_pasos = int(24 * 3600 / paso_h)
    t_array = np.linspace(0, 24 * 3600, n_pasos + 1)

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    for nombre_orbita, (p0, v0) in orbitas.items():
        trayectoria = propagar(p0, v0, paso_h, n_pasos)

        h_norma = np.zeros(n_pasos + 1)
        h_dot_norma = np.zeros(n_pasos + 1)
        energia_esp = np.zeros(n_pasos + 1)

        for i in range(n_pasos + 1):
            r_vec = trayectoria[i, :3]
            v_vec = trayectoria[i, 3:]
            r_norm = np.linalg.norm(r_vec)

            # Ac gravitatoria
            a_vec = -G * r_vec / r_norm**3

            # Mom ang: h = r x v
            h_vec = np.cross(r_vec, v_vec)
            h_norma[i] = np.linalg.norm(h_vec)

            # Der mom ang: h_dot = r x a
            h_dot_vec = np.cross(r_vec, a_vec)
            h_dot_norma[i] = np.linalg.norm(h_dot_vec)

            # Energía: epsilon = 1/2 v*v - mu/r
            energia_esp[i] = 0.5 * np.dot(v_vec, v_vec) - G / r_norm

        axs[0].plot(t_array, h_norma, label=nombre_orbita)
        axs[1].plot(t_array, h_dot_norma, label=nombre_orbita)
        axs[2].plot(t_array, energia_esp, label=nombre_orbita)

    axs[0].set_title("Magnitud del Momento Angular (h)")
    axs[0].set_ylabel("h [km^2/s]")
    axs[0].grid(); axs[0].legend()

    axs[1].set_title("Magnitud de la Derivada del Momento Angular (h_dot)")
    axs[1].set_ylabel("h_dot [km^2/s^2]")
    axs[1].grid(); axs[1].legend()

    axs[2].set_title("Energía Total Específica ($\epsilon$)")
    axs[2].set_ylabel("$\epsilon$ [km^2/s^2]")
    axs[2].set_xlabel("Tiempo [s]")
    axs[2].grid(); axs[2].legend()

    plt.tight_layout()
    plt.savefig("conservacion_magnitudes.png")
    plt.show()


