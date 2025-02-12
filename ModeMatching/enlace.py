import numpy as np

def enlace(nm1, nme, nm2, gmtr, sb11, sb12, sb21, sb22, sa11, sa12, sa21, sa22):
    """
    Esta función combina los parámetros de dispersión de dos secciones adyacentes de la guía de onda.
    
    Función enlace para calcular la matriz de scattering completa.

    Parámetros de entrada:
    nm1 -> número de modos
    nme -> número de modos
    nm2 -> número de modos
    gmtr -> gmtr=exp(-gm1*(z(j+1)-z(j))) en la parte 1
    sb11 -> S11 de la matriz derecha
    sb12 -> S12 de la matriz derecha
    sb21 -> S21 de la matriz derecha
    sb22 -> S22 de la matriz derecha
    sa11 -> S11 de la matriz izquierda
    sa12 -> S12 de la matriz izquierda
    sa21 -> S21 de la matriz izquierda
    sa22 -> S22 de la matriz izquierda

    Parámetros de salida:
    st11 -> S11 de la matriz de scattering completa
    st12 -> S12 de la matriz de scattering completa
    st21 -> S21 de la matriz de scattering completa
    st22 -> S22 de la matriz de scattering completa
    """
    ur = 1 + 0j
    st11 = np.zeros((nm1, nm2), dtype=complex)
    st12 = np.zeros((nm1, nm2), dtype=complex)
    st21 = np.zeros((nm1, nm2), dtype=complex)
    st22 = np.zeros((nm1, nm2), dtype=complex)

    T = np.diag(gmtr)
    sa12 = sa12 @ T
    sa21 = T @ sa21
    sa22 = T @ sa22 @ T

    ff = np.eye(nme) - sa22 @ sb11
    ff = np.linalg.pinv(ff)
    Aux1 = ff @ sa22
    Aux2 = ff @ sa21

    st11 = sa11 + sa12 @ sb11 @ Aux2
    st12 = sa12 @ (np.eye(nme) + sb11 @ Aux1) @ sb12
    st21 = sb21 @ Aux2
    st22 = sb22 + sb21 @ Aux1 @ sb12

    return st11, st12, st21, st22

"""# Ejemplo de uso
nm1 = 10
nme = 10
nm2 = 10
gmtr = np.exp(-np.random.rand(nm1))
sb11 = np.random.rand(nme, nme) + 1j * np.random.rand(nme, nme)
sb12 = np.random.rand(nme, nm2) + 1j * np.random.rand(nme, nm2)
sb21 = np.random.rand(nm2, nme) + 1j * np.random.rand(nm2, nme)
sb22 = np.random.rand(nm2, nm2) + 1j * np.random.rand(nm2, nm2)
sa11 = np.random.rand(nm1, nme) + 1j * np.random.rand(nm1, nme)
sa12 = np.random.rand(nm1, nm2) + 1j * np.random.rand(nm1, nm2)
sa21 = np.random.rand(nm2, nme) + 1j * np.random.rand(nm2, nme)
sa22 = np.random.rand(nm2, nm2) + 1j * np.random.rand(nm2, nm2)

st11, st12, st21, st22 = enlace(nm1, nme, nm2, gmtr, sb11, sb12, sb21, sb22, sa11, sa12, sa21, sa22)
print("st11:", st11)
print("st12:", st12)
print("st21:", st21)
print("st22:", st22)"""