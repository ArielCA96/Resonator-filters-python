import numpy as np

def modosmn(a, b, mte, nte, fc):
    """
    Calcula los modos TE y TM para una guía de onda rectangular.
    Filtra los modos que tienen una frecuencia de corte menor que la frecuencia de operación fc.
    """

    co = 3e8  # Velocidad de la luz en el vacío

    # Cálculo de los índices de los modos TE
    m = np.arange(1, mte + 1, 2)
    n = np.arange(0, nte + 1, 2)
    x, y = np.meshgrid(m, n)
    ind_m = x.ravel()
    ind_n = y.ravel()
    gmte = np.vstack((ind_m, ind_n)).T

    # Cálculo de los índices de los modos TM
    m = np.arange(1, mte + 1, 2)
    n = np.arange(2, nte + 1, 2)
    x, y = np.meshgrid(m, n)
    ind_m = x.ravel()
    ind_n = y.ravel()
    gmtm = np.vstack((ind_m, ind_n)).T

    # Frecuencia de corte para modos TE
    fcor = (co / 2) * np.sqrt((gmte[:, 0] / a) ** 2 + (gmte[:, 1] / b) ** 2)
    booleana = fcor < fc
    gmte = gmte[booleana]
    if gmte.shape[0] == 0:
        print('La frecuencia de corte es demasiado baja')
        # Al menos el modo TE10 debe propagarse...

    # Frecuencia de corte para modos TM
    fcor = (co / 2) * np.sqrt((gmtm[:, 0] / a) ** 2 + (gmtm[:, 1] / b) ** 2)
    booleana = fcor < fc
    gmtm = gmtm[booleana]
    if gmtm.shape[0] == 0:
        gmtm = np.array([[1, 2]])

    return gmte, gmtm

"""# Ejemplo de uso
a = 1.0
b = 0.5
mte = 10
nte = 10
fc = 10e9

gmte, gmtm = modosmn(a, b, mte, nte, fc)
print("Modos TE:", gmte)
print("Modos TM:", gmtm)"""