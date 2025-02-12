import cupy as cp

from ModeMatching.modosmn import modosmn

def spriz(a1, b1, f, mte, nte, er1, ur1, fc):
    """
    Calcula los parámetros de dispersión (admitancia y propagación) para los modos TE y TM.
    Utiliza los modos calculados en modosmn
    """

    c = cp.float64(3e8)  # Velocidad de la luz
    u = cp.float64(4 * cp.pi * 1e-7)  # Permeabilidad del vacío
    e = cp.float64(8.854187817e-12)  # Permisividad del vacío
    mu = cp.sqrt(u / e)
    ka = 2 * cp.pi * f / c

    c0 = cp.complex(0, 0)
    ur = cp.complex(1, 0)
    ui = cp.complex(0, 1)
    c2 = cp.complex(2, 0)

    ur1 = ur
    er1 = 1

    gmte, gmtm = modosmn(a1, b1, mte, nte, fc)

    gmpp = cp.sqrt(-ka**2 * ur1 * er1 + (gmte[:, 0] * cp.pi / a1)**2 + (gmte[:, 1] * cp.pi / b1)**2)
    admpp = gmpp / (ui * ka * mu)
    delpp = (ui * ka * mu) * gmpp * (a1 * b1 / 4) / ((gmte[:, 0] * cp.pi / a1)**2 + (gmte[:, 1] * cp.pi / b1)**2)
    boole = gmte[:, 1] == 0
    k = cp.where(boole)
    delpp[k] = delpp[k] * 2

    gmp2 = cp.sqrt(-ka**2 * ur1 * er1 + (gmtm[:, 0] * cp.pi / a1)**2 + (gmtm[:, 1] * cp.pi / b1)**2)
    delp22 = ka * er1 * a1 * b1 * gmp2 / (4 * mu)
    delp222 = delp22 / ((gmtm[:, 0] * cp.pi / a1)**2 + (gmtm[:, 1] * cp.pi / b1)**2)
    delp2 = delp222 * ui * 1e12
    admp2 = (gmp2 * mu) / (ka * er1)
    admp2 = 1.0 / (admp2 * ui)

    gmp = cp.concatenate((gmpp, gmp2))
    admp = cp.concatenate((admpp, admp2))
    delp = cp.concatenate((delpp, delp2))

    return gmp, admp, delp, gmte, gmtm