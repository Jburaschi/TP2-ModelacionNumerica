import math
import numpy as np


def resolver_tridiagonal(a, b, c, d):

    n = len(b)

    cp = np.zeros(n)
    dp = np.zeros(n)

    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]

    for i in range(1, n):

        denominador = b[i] - a[i] * cp[i - 1]

        # Validación de división por cero en la matriz
        if math.isclose(denominador, 0.0, abs_tol=1e-12):
            raise ZeroDivisionError(
                "Error numérico: denominador casi nulo en algoritmo tridiagonal."
            )

        cp[i] = c[i] / denominador if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / denominador

    x = np.zeros(n)

    x[n - 1] = dp[n - 1]

    for i in range(n - 2, -1, -1):

        x[i] = dp[i] - cp[i] * x[i + 1]

    return x



class SplineNatural:

    def __init__(self, t, y):

        self.t = t
        self.y = y

        self.calcular()

    def calcular(self):

        n = len(self.t)

        h = np.zeros(n - 1)

        for i in range(n - 1):
            h[i] = self.t[i + 1] - self.t[i]
            # Uso de math.isclose (lo pide el enunciado)
            if math.isclose(h[i], 0.0, abs_tol=1e-9):
                raise ValueError(
                    f"Puntos de tiempo idénticos o demasiado cercanos detectados en el índice {i}."
                )

        a = np.zeros(n)
        b = np.zeros(n)
        c = np.zeros(n)
        d = np.zeros(n)

        b[0] = 1.0
        b[n - 1] = 1.0

        for i in range(1, n - 1):

            a[i] = h[i - 1]

            b[i] = 2.0 * (h[i - 1] + h[i])

            c[i] = h[i]

            d[i] = 6.0 * (
                (self.y[i + 1] - self.y[i]) / h[i]
                - (self.y[i] - self.y[i - 1]) / h[i - 1]
            )

        self.M = resolver_tridiagonal(a, b, c, d)

    def evaluar(self, tiempo):
        n = len(self.t)

        # Control extra-rango tolerante por errores de redondeo de flotantes
        if tiempo < self.t[0]:
            tiempo = self.t[0]
        if tiempo > self.t[-1]:
            tiempo = self.t[-1]

        # Búsqueda (log N) para encontrar el intervalo
        izq = 0
        der = n - 1
        intervalo = 0

        while izq <= der:
            medio = (izq + der) // 2
            if medio < n - 1 and self.t[medio] <= tiempo <= self.t[medio + 1]:
                intervalo = medio
                break
            elif medio < n - 1 and self.t[medio + 1] < tiempo:
                izq = medio + 1
            else:
                der = medio - 1

        h = self.t[intervalo + 1] - self.t[intervalo]

        A = (self.t[intervalo + 1] - tiempo) / h
        B = (tiempo - self.t[intervalo]) / h

        resultado = (
            A * self.y[intervalo]
            + B * self.y[intervalo + 1]
            + ((A**3 - A) * self.M[intervalo] + (B**3 - B) * self.M[intervalo + 1])
            * h**2
            / 6.0
        )

        return resultado