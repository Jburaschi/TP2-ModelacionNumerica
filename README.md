# TP2 - Modelación Numérica

## Integrantes

* Agustín Bardi Hourclé - Padrón 112734
* Jonathan David Buraschi - Padrón 107633
* Nombre Apellido - Padrón ######

## Requisitos

El trabajo fue desarrollado en Python 3.

Se utilizaron las bibliotecas `numpy` y `matplotlib`.


## Ejecución

### Interpolador

Ejecutar desde la carpeta Tp2:

```bash
python main.py
```

El programa solicita un tiempo en segundos para realizar la interpolación y luego genera los gráficos correspondientes.
Ingrese tiempo [s]: 6000

### Propagador

Ejecutar desde la carpeta Tp2:

```bash
python propagador.py
```

### Conservación de magnitudes

Abrir una consola de Python desde la carpeta del proyecto y ejecutar:

```python
from Conservación import analizar_conservacion_magnitudes

analizar_conservacion_magnitudes(1, 24)
analizar_conservacion_magnitudes(480, 36)
```
