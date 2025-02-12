import win32com.client
import numpy as np

from Auxiliares.ExportarAcople import ExportarAcople
from Home.CstDefineUnits import CstDefineUnits
from Simulation.CstDefineFrequencyRange import CstDefineFrequencyRange
from Simulation.CstDefineFrequencyDomainSolver import CstDefineFrequencyDomainSolver
from Simulation.CstDefineBackgroundMaterial import CstDefineBackgroundMaterial
from Simulation.CstDefineMesh import CstDefineMesh
from Simulation.CstStartSimulation import CstStartSimulation
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
from Estructuras.CstDefineElectricBoundary import CstDefineElectricBoundary
from Geometria.CrearPortAcopling import CrearPortAcopling
from Geometria.CrearFiltroIris import CrearFiltroIris
from Geometria.FilterPorts import FilterPorts

a0=19.05
b0=9.525
l0 = 20
fres = 12.5    #GHz

filter_width = a0
filter_height = b0 
filter_length = 15.45

#variante 2
filter_length = b0
filter_height = 15.45

coupling_length = 5
iris_width = [ 3]
num_resonators = len(iris_width) - 1

Config = FiltroResonanteConfig(
            a0=a0, 
            b0=b0, 
            l0=l0, 
            filter_width = filter_width,
            filter_height = filter_height,
            filter_length = filter_length,
            coupling_length = coupling_length,
            iris_width = iris_width,
            num_resonators=num_resonators,

        )

Qext_m = []
range_iris_width = [3.658, 4]
numero_puntos = 5
i_values = np.linspace(range_iris_width[0], range_iris_width[1], numero_puntos)
for i in i_values:
    Config.iris_width = [i]

    cst = win32com.client.Dispatch('CSTStudio.Application')
    mws = cst.NewMWS()

    Geometry = 'mm'
    Frequency = 'GHz'
    Time = 'ns'
    TemperatureUnit = 'Kelvin'
    Voltage = 'V'
    Current = 'A'
    Resistance = 'Ohm'
    Conductance = 'S'
    Capacitance = 'PikoF'
    Inductance = 'NanoH'

    CstDefineUnits(mws, Geometry, Frequency, Time, TemperatureUnit, Voltage, Current, Resistance, Conductance, Capacitance,
                Inductance)

    startFreq = '12.1'
    endFreq = '12.9'
    CstDefineFrequencyRange(mws, startFreq, endFreq)

    samples = '1'
    SourceType = '1'
    CstDefineFrequencyDomainSolver(mws,startFreq,endFreq,samples,SourceType)

    CstDefineElectricBoundary(mws)

    type = 'Pec'
    CstDefineBackgroundMaterial(mws,type)

    CrearPortAcopling(mws, a0, b0, l0, filter_width, filter_height, filter_length, coupling_length, Config.iris_width, model=2)

    steps_per_box_near = 11
    steps_per_box_far = 2
    CstDefineMesh(mws, steps_per_box_near, steps_per_box_far)

    # Port 1
    PortNumber = 1
    NumberOfModes = 1
    Xrange = Config.xrange_p1
    Yrange = Config.yrange_p1
    Zrange = Config.zrange_p1
    XrangeAdd = [0, 0]
    YrangeAdd = [0, 0]
    ZrangeAdd = [0, 0]
    Coordinates = 'Free'
    Orientation = 'xmin'
    FilterPorts(mws, PortNumber, NumberOfModes, Xrange, Yrange, Zrange, XrangeAdd, YrangeAdd, ZrangeAdd, Coordinates, Orientation, )

    CstStartSimulation(mws)

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.interpolate import interp1d
    import os
    import json

    TreeItem = "1D Results\\S-Parameters\\S1,1"
    IDs = mws.Resulttree.GetResultIDsFromTreeItem(TreeItem)
    spara = mws.Resulttree.GetResultFromTreeItem(TreeItem, IDs[0])
    FrequencyRange = np.array(spara.GetArray("x"))
    SRE = spara.GetArray("yre")
    SIM = spara.GetArray("yim")
    # Calculate the magnitude in dB
    s11_dB = 20 * np.log10(np.sqrt(np.array(SRE)**2 + np.array(SIM)**2))

    # Calculate the phase in degrees
    s11_phase = np.degrees(np.arctan2(SIM, SRE))
    s11_derivative = np.diff(s11_phase) / np.diff(FrequencyRange)
    # Find the point where the slope changes sign
    positive_slope_indices = np.where(s11_derivative > 0)[0]
    
    for idx in positive_slope_indices:
        s11_phase[idx + 1:] -= 360
    s11_derivative = np.diff(s11_phase) / np.diff(FrequencyRange)
    min_slope_index = np.argmin(s11_derivative)

    f0 = FrequencyRange[min_slope_index]
    target_phase = s11_phase[min_slope_index] + 90
    f1 = np.interp(target_phase, s11_phase[::-1], FrequencyRange[::-1])
    target_phase = s11_phase[min_slope_index] - 90
    f2 = np.interp(target_phase, s11_phase[::-1], FrequencyRange[::-1] )

    Qext = f0 / (f2 - f1)
    print(f0, f1, f2, Qext)
    c = 299792458  # Velocidad de la luz en m/s
    delta_l = np.pi / np.sqrt((fres * 1e9 * 2 * np.pi / c)**2 - (np.pi / (a0 * 1e-3))**2) - \
             np.pi / np.sqrt((f0 * 1e9 * 2 * np.pi / c)**2 - (np.pi / (a0 * 1e-3))**2)
    print(delta_l, i)


    plt.plot(f0, s11_phase[min_slope_index], 'ro') 
    plt.plot(f1, s11_phase[min_slope_index]+90, 'bo')
    plt.plot(f2, s11_phase[min_slope_index]-90, 'go')

    # Plot the phase
    plt.plot(FrequencyRange, s11_phase)
    plt.xlabel('Frequency (GHz)')
    plt.ylabel('Phase (degrees)')
    plt.title('S11 Phase vs Frequency')
    plt.grid(True)
    plt.show()

    Qext_m.append(Qext)

# Plot Qext_m
"""iris_width = 7
plt.plot([iris_width + add_value * i for i in range(1, 11)], Qext_m, marker='o')
plt.xlabel('Iris Width (mm)')
plt.ylabel('Qext')
plt.title('Qext vs Iris Width')
plt.grid(True)
plt.show()"""