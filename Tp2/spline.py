import numpy as np


def resolver_tridiagonal(a, b, c, d):

    n = len(b)

    cp = np.zeros(n)
    dp = np.zeros(n)

    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]

    for i in range(1, n):

        denominador = b[i] - a[i] * cp[i - 1]

        cp[i] = c[i] / denominador if i < n - 1 else 0.0

        dp[i] = (
            d[i] - a[i] * dp[i - 1]
        ) / denominador

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
                -
                (self.y[i] - self.y[i - 1]) / h[i - 1]
            )

        self.M = resolver_tridiagonal(
            a,
            b,
            c,
            d
        )

    def evaluar(self, tiempo):

        n = len(self.t)

        intervalo = 0

        for i in range(n - 1):

            if self.t[i] <= tiempo <= self.t[i + 1]:
                intervalo = i
                break

        h = self.t[intervalo + 1] - self.t[intervalo]

        A = (
            self.t[intervalo + 1] - tiempo
        ) / h

        B = (
            tiempo - self.t[intervalo]
        ) / h

        resultado = (
            A * self.y[intervalo]
            +
            B * self.y[intervalo + 1]
            +
            (
                (A**3 - A)
                * self.M[intervalo]
                +
                (B**3 - B)
                * self.M[intervalo + 1]
            )
            * h**2
            / 6.0
        )

        return resultado