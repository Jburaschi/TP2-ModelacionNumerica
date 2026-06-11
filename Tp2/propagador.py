import numpy as np
import matplotlib.pyplot as plt

G = 398600.4418

def f(estado):
    x, y, z, vx, vy, vz = estado
    r = np.sqrt(x**2 + y**2 + z**2)
    
    ax = -G * x / r**3
    ay = -G * y / r**3
    az = -G * z / r**3

    return np.array([vx, vy, vz, ax, ay, az])


def paso_rk4(estado, h):
    k1 = f(estado)
    k2 = f(estado + 0.5 * h * k1)
    k3 = f(estado + 0.5 * h * k2)
    k4 = f(estado + h * k3)

    return estado + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def periodo_orbital(p0, v0):
    r = np.linalg.norm(p0)
    v = np.linalg.norm(v0)
    a = 1.0 / (2.0 / r - v**2 / G)
    return 2.0 * np.pi * np.sqrt(a**3 / G)


def propagar(p0, v0, h, n_pasos):
    estado = np.array([*p0, *v0], dtype=float)
    tray = np.zeros((n_pasos + 1, 6))
    tray[0] = estado
    for i in range(n_pasos):
        estado = paso_rk4(estado, h)
        tray[i + 1] = estado
    return tray


orbitas = {
    "Circular":        ([6125.24, -3547.04, -3.31277],  [-0.519174, -0.903482, 7.43159]),
    "Geoestacionaria": ([-41974.9, 4012.93, 23.5515],   [-0.292606, -3.06063, 0.000293508]),
    "Molniya":         ([305.926, 3162.83, 6324.79],    [-9.86976, 0.326984, 0.313879]),
}

h = 1.0

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

for nombre, (p0, v0) in orbitas.items():
    n = int(periodo_orbital(p0, v0) / h)
    tray = propagar(p0, v0, h, n)
    ax.plot(tray[:, 0], tray[:, 1], tray[:, 2], label=nombre)

ax.scatter(0, 0, 0, color="blue", s=50, label="Tierra")
ax.set_xlabel("X [km]"); ax.set_ylabel("Y [km]"); ax.set_zlabel("Z [km]")
ax.legend()
plt.savefig("orbitas_propagadas.png")
plt.show()