from lector import cargar_datos
from spline import SplineNatural
from graficos import graficar_orbita, graficar_componentes
from comparacion import comparar_spline_vs_real


# PUNTO B Interpolacion y graficos del SAC-D
t, x, y, z = cargar_datos(
    "SACD_TPV_step_600s.txt"
)

sx = SplineNatural(t, x)
sy = SplineNatural(t, y)
sz = SplineNatural(t, z)

print("INTERPOLADOR ORBITAL SAC-D")
print(f"Rango de tiempo disponible: {t[0]:.1f} s a {t[-1]:.1f} s")

tiempo = float(
    input("\nIngrese tiempo a interpolar [s]: ")
)

if tiempo < t[0] or tiempo > t[-1]:

    print("\nTiempo fuera del rango de interpolacion")

else:

    print("\nPosicion interpolada:")
    print(f"  X = {sx.evaluar(tiempo):.6f} km")
    print(f"  Y = {sy.evaluar(tiempo):.6f} km")
    print(f"  Z = {sz.evaluar(tiempo):.6f} km")

# Graficos punto B
graficar_orbita(t, x, y, z, sx, sy, sz)
graficar_componentes(t, x, y, z, sx, sy, sz)

# punto c Comparacion spline (600s) vs datos (1s)

comparar_spline_vs_real()