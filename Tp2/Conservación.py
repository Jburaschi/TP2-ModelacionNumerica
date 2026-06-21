import numpy as np
import matplotlib.pyplot as plt
from propagador import propagar, orbitas, G

def analizar_conservacion_magnitudes(paso_h, horas):
 
    n_pasos = int(horas * 3600 / paso_h)
    t_array_segundos = np.linspace(0, horas * 3600, n_pasos + 1)
    t_array_horas = t_array_segundos / 3600  # Convertimos a horas para un eje X más legible

    fig, axs = plt.subplots(3, 1, figsize=(10, 12))
    
    fig.suptitle(f"Conservación de Magnitudes\nTiempo total: {horas} horas | Paso (h): {paso_h} s", fontsize=14, fontweight='bold')

    for nombre_orbita, (p0, v0) in orbitas.items():
        trayectoria = propagar(p0, v0, paso_h, n_pasos)

        h_norma = np.zeros(n_pasos + 1)
        h_dot_norma = np.zeros(n_pasos + 1)
        energia_esp = np.zeros(n_pasos + 1)

        for i in range(n_pasos + 1):
            r_vec = trayectoria[i, :3]
            v_vec = trayectoria[i, 3:]
            r_norm = np.linalg.norm(r_vec)

            # Aceleración gravitatoria
            a_vec = -G * r_vec / r_norm**3

            # Momento angular: h = r x v
            h_vec = np.cross(r_vec, v_vec)
            h_norma[i] = np.linalg.norm(h_vec)

            # Derivada del momento angular: h_dot = r x a
            h_dot_vec = np.cross(r_vec, a_vec)
            h_dot_norma[i] = np.linalg.norm(h_dot_vec)

            # Energía: epsilon = 1/2 v*v - mu/r
            energia_esp[i] = 0.5 * np.dot(v_vec, v_vec) - G / r_norm

        axs[0].plot(t_array_horas, h_norma, label=nombre_orbita)
        axs[1].plot(t_array_horas, h_dot_norma, label=nombre_orbita)
        axs[2].plot(t_array_horas, energia_esp, label=nombre_orbita)

    # Configuraciones estéticas
    axs[0].set_title("Magnitud del Momento Angular (h)")
    axs[0].set_ylabel("h [km²/s]")
    axs[0].grid(True); axs[0].legend(loc='upper right')

    axs[1].set_title("Magnitud de la Derivada del Momento Angular (h_dot)")
    axs[1].set_ylabel("h_dot [km²/s²]")
    axs[1].grid(True); axs[1].legend(loc='upper right')

    axs[2].set_title("Energía Total Específica ($\epsilon$)")
    axs[2].set_ylabel("$\epsilon$ [km²/s²]")
    axs[2].set_xlabel("Tiempo [horas]")
    axs[2].grid(True); axs[2].legend(loc='upper right')

    plt.tight_layout()
    plt.subplots_adjust(top=0.92) 

    nombre_archivo_png = f"conservacion_h{int(paso_h)}s_t{int(horas)}h.png"
    plt.savefig(nombre_archivo_png, dpi=300)
    
    plt.show()
