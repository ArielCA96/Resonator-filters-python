import numpy as np

def ctct(a, b, rm, rn, rp):
    """
    Función ctct para calcular una matriz de resultados.

    Parámetros de entrada:
    a -> límite inferior
    b -> límite superior
    rm -> vector de índices m
    rn -> vector de índices n
    rp -> vector de parámetros rp

    Parámetros de salida:
    res -> matriz de resultados
    """
    rment, rnent = np.meshgrid(rm, rn)
    resta = rment - rnent
    rpent = np.tile(rp, (1, resta.shape[1]))
    rpent = rpent.reshape(1, -1)
    resta1 = resta.reshape(1, -1)
    in_mask = np.abs(resta1) > 0.0001
    ind = np.where(in_mask)
    out_mask = ~in_mask
    outd = np.where(out_mask)

    resta1[0, ind] = (np.sin(resta1[0, ind] * b - rpent[0, ind]) - np.sin(resta1[0, ind] * a - rpent[0, ind])) / resta1[0, ind]
    resta1[0, outd] = (b - a) * np.cos(rpent[0, outd])

    suma = rment + rnent
    suma1 = suma.reshape(1, -1)
    in_mask = np.abs(suma1) > 0.0001
    ind = np.where(in_mask)
    out_mask = ~in_mask
    outd = np.where(out_mask)

    suma1[0, ind] = (np.sin(suma1[0, ind] * b + rpent[0, ind]) - np.sin(suma1[0, ind] * a + rpent[0, ind])) / suma1[0, ind]
    suma1[0, outd] = (b - a) * np.cos(rpent[0, outd])

    res = (resta1 + suma1) / 2
    res = res.reshape(resta.shape)

    return res

"""# Ejemplo de uso
a = 1.0
b = 2.0
rm = np.array([1, 2, 3])
rn = np.array([4, 5, 6])
rp = np.array([0.1, 0.2, 0.3])

res = ctct(a, b, rm, rn, rp)
print("res:", res)"""