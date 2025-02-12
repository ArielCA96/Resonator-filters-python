import numpy as np

range_iris_width = [3, 4]
numero_puntos = 5
i_values = np.linspace(range_iris_width[0], range_iris_width[1], numero_puntos)
print(i_values)


y = np.array([4., 3.75, 3.5,  3.25, 3.  ])
x = np.array([51.4952, 56.2780, 61.88953, 68.825, 77.357])
target_phase = 58.3252

# Interpolación
f1 = np.interp(target_phase, x, y)
print(f1)  # Resultado interpolado

y = np.array([8.6, 8.56])
x = np.array([58.0094, 59.4932])
target_phase = 58.325

# Interpolación
f1 = np.interp(target_phase, x, y)
print(f1)

c = 299792458
f0 = 11*1e9
f1 = 10.85*1e9
f2 = 11.15*1e9
a = 22.86*1e-3
l = 16.972
def delta(f,a):
    delta = (c/f)/(1-(c/(2*a*f)))**0.5
    return delta
delta_l = (delta(f1,a) - delta(f2,a))/delta(f0,a)
print(delta_l)

delta_l = np.pi / np.sqrt((11 * 1e9 * 2 * np.pi / c)**2 - (np.pi / (22.86 * 1e-3))**2)
print(delta_l*1e3)

s11 = -0.954-0.278j
s12 = -0.017+0.06j
Xs = abs((1-s12+s11)/(1-s11+s12))
Xp = abs((2*s12)/((1-s11)**2-s12**2))
print(Xs)
print(Xp)
