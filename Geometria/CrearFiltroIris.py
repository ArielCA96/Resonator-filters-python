from Geometria.CstBrick import Cstbrick
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
from Estructuras.CstComand import Add
import numpy as np

def CrearFiltroIris(mws, a0, b0, l0, num_resonators, filter_width, filter_height, filter_length, coupling_length, iris_width, model=1):
    brick = mws.Brick

    #Puertos
    a0 = a0  # mm
    b0 = b0  # mm
    l0 = l0 # mm
    
    # Resonadores
    num_resonators = num_resonators
    filter_width = filter_width  # mm
    filter_height = filter_height  # mm
    filter_length = filter_length  # mm

    # Acopladores
    coupling_length = coupling_length  # mm
    iris_width = iris_width  # mm

    # Crear puerto 1    
    Name = 'puerto 1'
    component = 'Port'
    material = 'Vacuum'
    Xrange = [0,l0]
    Yrange = [-b0/2,b0/2]
    Zrange = [-a0/2,a0/2]
    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)

    # Crear puerto 2    
    port_position = l0 + np.sum(filter_length) + (num_resonators+1)*coupling_length
    Name = 'puerto 2'
    component = 'Port'
    material = 'Vacuum'
    Xrange = [port_position, port_position+l0]
    Yrange = [-b0/2,b0/2]
    Zrange = [-a0/2,a0/2]
    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)

    Add( mws, "Unir puertos", 'Port', 'puerto 1', 'Port', 'puerto 2')

    # Crear resonadores
    for i in range(num_resonators):
        filter_start =  l0 + coupling_length + np.sum(filter_length[:i])+coupling_length*i
        Name = 'resonador ' + str(i)
        component = 'Resonators'
        material = 'Vacuum'
        Xrange = [filter_start, filter_start + filter_length[i]]
        Yrange = [-filter_height/2, filter_height/2]
        Zrange = [-filter_width/2, filter_width/2]
        Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
        Add( mws, "Unir resonadores", 'Port', 'puerto 1', 'Resonators', Name)
    
    # Crear acopladores
    if model == 1:
        for i in range(num_resonators + 1):
            coupling_start = l0 + np.sum(filter_length[:i]) + coupling_length*i
            # Rejilla de acopladores 
            Name = 'Iris ' + str(i)
            component = 'Coupling'
            material = 'Vacuum'
            Xrange = [coupling_start, coupling_start + coupling_length]
            Yrange = [-filter_height/2, filter_height/2]
            Zrange = [-iris_width[i]/2, iris_width[i]/2]
            Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
            Add( mws, "Unir acoples", 'Port', 'puerto 1', 'Coupling', Name)
    if model == 2:
        for i in range(num_resonators + 1):
            coupling_start = l0 +  np.sum(filter_length[:i]) + coupling_length*i
            # Rejilla de acopladores 
            copling_delay = 2
            port_delay = -2
            Name = 'Iris ' + str(i)
            component = 'Coupling'
            material = 'Vacuum'
            Xrange = [coupling_start, coupling_start + coupling_length]
            Yrange = [-iris_width[i]/2+copling_delay, iris_width[i]/2+copling_delay]
            if i ==0 or i == (num_resonators):
                Yrange = [-iris_width[i]/2+port_delay, iris_width[i]/2+port_delay]
            Zrange = [-filter_width/2, filter_width/2]
            Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
    if model == 3:
         for i in range(num_resonators + 1):
            coupling_start = l0 + np.sum(filter_length[:i]) + coupling_length*i
            # Rejilla de acopladores 
            Name = 'Iris ' + str(i)
            component = 'Coupling'
            material = 'Vacuum'
            Xrange = [coupling_start, coupling_start + coupling_length]
            Yrange = [-filter_height/2, filter_height/2]
            Zrange = [-iris_width[i]/2, iris_width[i]/2]
            if i ==0 or i == (num_resonators):
                Zrange = [filter_width/2-iris_width[i], filter_width/2]
            Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
            Add( mws, "Unir acoples", 'Port', 'puerto 1', 'Coupling', Name)