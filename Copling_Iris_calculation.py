import win32com.client
import matplotlib.pyplot as plt
import os
import json
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
from Geometria.CrearFiltroIris import CrearFiltroIris
from Geometria.FilterPorts import FilterPorts


a0=19.05
b0=9.525
l0 = 20
fres = 12.5 #GHz

filter_width = a0
filter_height = b0
filter_length = [15.45 , 15.4]

#variante 2
filter_length = [b0, b0]
filter_height = 15.45



coupling_length = 5
iris_width = [ 3, 5, 3]
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

array_coupling = []
range_iris_width = [2.037 , 4]
numero_puntos = 10
i_values = np.linspace(range_iris_width[0], range_iris_width[1], numero_puntos)
for i in i_values:
    Config.iris_width = [0.3, i, 0.3]
    #print(Config.iris_width)

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

    startFreq = '10.95'
    endFreq = '14.5'
    CstDefineFrequencyRange(mws, startFreq, endFreq)

    samples = '1'
    SourceType = '1'
    CstDefineFrequencyDomainSolver(mws,startFreq,endFreq,samples,SourceType)

    CstDefineElectricBoundary(mws)

    type = 'Pec'
    CstDefineBackgroundMaterial(mws,type)

    CrearFiltroIris(mws, a0, b0, l0, num_resonators, filter_width, filter_height, filter_length, coupling_length, Config.iris_width, model=2)

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
    FilterPorts(mws, PortNumber, NumberOfModes, Xrange, Yrange, Zrange, XrangeAdd, YrangeAdd, ZrangeAdd, Coordinates, Orientation)

    # Port 2
    PortNumber = 2
    NumberOfModes = 1
    Xrange = Config.xrange_p2
    Yrange = Config.yrange_p2
    Zrange = Config.zrange_p2
    XrangeAdd = [0, 0]
    YrangeAdd = [0, 0]
    ZrangeAdd = [0, 0]
    Coordinates = 'Free'
    Orientation = 'xmax'
    FilterPorts(mws, PortNumber, NumberOfModes, Xrange, Yrange, Zrange, XrangeAdd, YrangeAdd, ZrangeAdd, Coordinates, Orientation)

    CstStartSimulation(mws)

    coupling, f0 = ExportarAcople(mws, Config)
    c = 299792458  # Velocidad de la luz en m/s
    delta_l = np.pi / np.sqrt((fres * 1e9 * 2 * np.pi / c)**2 - (np.pi / (a0 * 1e-3))**2) - \
             np.pi / np.sqrt((f0 * 1e9 * 2 * np.pi / c)**2 - (np.pi / (a0 * 1e-3))**2)
    print(delta_l)

    array_coupling.append(coupling)



i_values = np.linspace(range_iris_width[0], range_iris_width[1]-(range_iris_width[1]-range_iris_width[0])/numero_puntos, numero_puntos)
i_values = i_values.tolist()
config_data = {
            'iris_width': i_values ,
            'coupling': array_coupling
        }
results_path = Config.get_iris_copling_results_path()
filename = Config.generate_iris_copling_filename()        
file_path = os.path.join(results_path, f"{filename}.json")
with open(file_path, 'w') as file:
    json.dump(config_data, file, indent=4)

plt.plot(i_values, array_coupling)
plt.xlabel('Iris Width (mm)')
plt.ylabel('Coupling')
plt.title('Coupling vs Iris Width')
plt.grid(True)
plt.show()

#print(i_values)
#print(array_coupling)
#print('-------------------')