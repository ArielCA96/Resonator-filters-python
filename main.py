import win32com.client

from Auxiliares.ExportarResultadosCST import ExportarResultadosCST
from Home.CstDefineUnits import CstDefineUnits
from Simulation.CstDefineFrequencyRange import CstDefineFrequencyRange
from Simulation.CstDefineFrequencyDomainSolver import CstDefineFrequencyDomainSolver
from Simulation.CstDefineBackgroundMaterial import CstDefineBackgroundMaterial
from Simulation.CstDefineMesh import CstDefineMesh
from Simulation.CstStartSimulation import CstStartSimulation
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
from Estructuras.CstDefineElectricBoundary import CstDefineElectricBoundary
from Geometria.CrearFiltroResonante import CrearFiltroResonante
from Geometria.FilterPorts import FilterPorts


Config = FiltroResonanteConfig(
            a0=19.05, 
            b0=9.525, 
            l0=5, 
            num_resonators=0, 
            filter_width=19.05, 
            filter_height=9.525, 
            filter_length=8, 
            coupling_length=0.1, 
            grid_width=0.1, 
            num_holes=[4, 1], 
            matrix = None,
            brick_height=4, 
            brick_width=4,
        )

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

CrearFiltroResonante(mws, Config)

steps_per_box_near = 11
steps_per_box_far = 2
CstDefineMesh(mws, steps_per_box_near, steps_per_box_far)

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

ExportarResultadosCST(mws, Config)

