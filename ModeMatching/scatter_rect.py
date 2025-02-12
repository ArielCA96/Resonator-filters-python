import numpy as np
import time

from ModeMatching.caaza import caaza
from ModeMatching.enlace import enlace


def scatt_rect(a, b, z, f, mte, nte, fc, distrib_z_modos):
    """
    Esta función es el punto de entrada principal para el análisis de una estructura 
    rectangular dividida en secciones. Inicializa matrices de resultados y llama a 
    la función caaza para calcular los parámetros de dispersión (S-parameters) de cada sección.
    """
    # Inicialización de matrices de resultados
    sizda11 = []
    sizda12 = []
    sizda21 = []
    sizda22 = []

    # Primera llamada a caaza
    start_time = time.time()
    gm1, gm2, del1, del2, adm1, adm2, nm1, nm2, sa11, sa12, sa21, sa22, teent, tment = caaza(a[0], b[0], a[0], b[0], f, mte, nte, fc)
    print(f'Simulation time: {time.time() - start_time} s')

    for j in range(len(a) - 1):
        if (a[j] >= a[j + 1]) and (b[j] >= b[j + 1]):
            # Si la guía se estrecha tanto en altura como en anchura, o se mantiene igual
            gm1, gm2, del1, del2, adm1, adm2, nm1, nmsal, sb11, sb12, sb21, sb22, tesal, tmsal = caaza(a[j], b[j], a[j + 1], b[j + 1], f, mte, nte, fc)
        else:
            if (a[j] < a[j + 1]) and (b[j] > b[j + 1]):
                # Si la guía aumenta de anchura, pero baja la altura
                gm1, gmc, del1, delc, adm1, admc, nm1, nmc, sc11, sc12, sc21, sc22, tesal, tmsal = caaza(a[j], b[j], a[j], b[j + 1], f, mte, nte, fc)
                gm2, gmc, del2, delc, adm2, admc, nmsal, nmc, sb22, sb21, sb12, sb11, tesal, tmsal = caaza(a[j + 1], b[j + 1], a[j], b[j + 1], f, mte, nte, fc)
                gmtr = np.exp(-gmc * (z[j] - z[j]))
                sb11, sb12, sb21, sb22 = enlace(nm1, nmc, nmsal, gmtr, sb11, sb12, sb21, sb22, sc11, sc12, sc21, sc22)
            elif (a[j] > a[j + 1]) and (b[j] < b[j + 1]):
                # Si la guía baja de anchura, pero aumenta la altura
                gm1, gmc, del1, delc, adm1, admc, nm1, nmc, sc11, sc12, sc21, sc22, tesal, tmsal = caaza(a[j], b[j], a[j + 1], b[j], f, mte, nte, fc)
                gm2, gmc, del2, delc, adm2, admc, nmsal, nmc, sb22, sb21, sb12, sb11, tesal, tmsal = caaza(a[j + 1], b[j + 1], a[j + 1], b[j], f, mte, nte, fc)
                gmtr = np.exp(-gmc * (z[j] - z[j]))
                sb11, sb12, sb21, sb22 = enlace(nm1, nmc, nmsal, gmtr, sb11, sb12, sb21, sb22, sc11, sc12, sc21, sc22)
            else:
                # Si la guía aumenta en altura y anchura
                gm2, gm1, del2, del1, adm2, adm1, nmsal, nm1, sb22, sb21, sb12, sb11, tesal, tmsal = caaza(a[j + 1], b[j + 1], a[j], b[j], f, mte, nte, fc)

        gmtr = np.exp(-gm1 * (z[j + 1] - z[j]))

        if distrib_z_modos == 1:
            T = np.diag(gmtr)
            sizda11.append(sa11)
            sizda12.append(sa12)
            sizda21.append(sa21)
            sizda22.append(sa22)

    return sizda11, sizda12, sizda21, sizda22

# Ejemplo de uso
a = np.array([1.0, 0.8, 0.6])
b = np.array([0.5, 0.4, 0.3])
z = np.array([0.0, 0.5, 1.0])
f = 10e9
mte = 10
nte = 10
fc = 10e9
distrib_z_modos = 1

sizda11, sizda12, sizda21, sizda22 = scatt_rect(a, b, z, f, mte, nte, fc, distrib_z_modos)