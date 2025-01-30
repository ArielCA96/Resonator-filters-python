import win32com.client

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

filter_width = a0
filter_height = b0
filter_length = 15.45

coupling_length = 1
iris_width = [ 3, 7, 3]
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
for i in range(30, 91, 10):
    Config.iris_width = [3, i / 10, 3]

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

    CrearFiltroIris(mws, a0, b0, l0, num_resonators, filter_width, filter_height, filter_length, coupling_length, Config.iris_width)

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

    coupling = ExportarAcople(mws, Config)

    array_coupling.append(coupling)

import matplotlib.pyplot as plt

i_values = [i / 10 for i in range(30, 91, 10)]

plt.plot(i_values, array_coupling)
plt.xlabel('Iris Width (mm)')
plt.ylabel('Coupling')
plt.title('Coupling vs Iris Width')
plt.grid(True)
plt.show()