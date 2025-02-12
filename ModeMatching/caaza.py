import numpy as np
import cupy as cp

from ModeMatching.spriz import spriz
from ModeMatching.scruz import scruz

def caaza(a1, b1, a2, b2, f, mte, nte, fc):
    """
    Calcula los parámetros de dispersión para dos secciones consecutivas.
    Utiliza spriz para calcular los modos y scruz para calcular los cruces entre modos.
    """
    # Convertir las entradas a arrays de CuPy para GPU
    a1 = cp.asarray(a1)
    b1 = cp.asarray(b1)
    a2 = cp.asarray(a2)
    b2 = cp.asarray(b2)
    f = cp.asarray(f)
    mte = cp.asarray(mte)
    nte = cp.asarray(nte)
    fc = cp.asarray(fc)

    # Inicialización de parámetros
    mtes = mte
    ntes = nte

    c0 = cp.complex(0, 0)
    ur = cp.complex(1, 0)
    ui = cp.complex(0, 1)
    c2 = cp.complex(2, 0)

    er1 = ur
    er2 = ur
    ur1 = ur
    ur2 = ur

    # Cálculo de modos TE y TM de entrada
    gm1, adm1, del1, gmtee, gmtme = spriz(a1, b1, f, mte, nte, er1, ur1, fc)
    gm2, adm2, del2, gmtes, gmtms = spriz(a2, b2, f, mtes, ntes, er2, ur2, fc)

    # Cálculo de cruces
    yb33 = scruz(a1, a2, b1, b2, gmtee, gmtme, gmtes, gmtms, del1, del2, gm1, gm2, f)

    nm1 = len(gmtee) + len(gmtme)
    nm2 = len(gmtes) + len(gmtms)

    yb13 = yb33
    yb31 = yb13.T

    # Cálculo de matrices delta y diagonal
    yb22 = yb13 @ yb31
    ident = cp.eye(nm2) * ur
    yb23 = yb22 + ident
    yb33 = ident - yb22

    return gm1, gm2, del1, del2, adm1, adm2, nm1, nm2, yb13, yb31, yb22, yb23, gmtes, gmtms

"""# Ejemplo de uso
a1 = 1.0
b1 = 0.5
a2 = 1.0
b2 = 0.5
f = 10e9
mte = 10
nte = 10
fc = 10e9

gm1, gm2, del1, del2, adm1, adm2, nm1, nm2, yb13, yb31, yb22, yb23, gmtes, gmtms = caaza(a1, b1, a2, b2, f, mte, nte, fc)
print("gm1:", gm1)
print("gm2:", gm2)
print("del1:", del1)
print("del2:", del2)
print("adm1:", adm1)
print("adm2:", adm2)
print("nm1:", nm1)
print("nm2:", nm2)
print("yb13:", yb13)
print("yb31:", yb31)
print("yb22:", yb22)
print("yb23:", yb23)
print("gmtes:", gmtes)
print("gmtms:", gmtms)"""