from Geometria.CstBrick import Cstbrick
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
from Estructuras.CstComand import Add

def CrearPortAcopling(mws, a0, b0, l0, filter_width, filter_height, filter_length, coupling_length, iris_width, model=1):
    brick = mws.Brick

    #Puertos
    a0 = a0  # mm
    b0 = b0  # mm
    l0 = l0 # mm
    
    # Resonadores
    filter_width = filter_width  # mm
    filter_height = filter_height  # mm
    filter_length = filter_length  # mm

    # Acopladores
    coupling_length = coupling_length  # mm
    iris_width = iris_width[0]  # mm

    # Crear puerto 1    
    Name = 'puerto 1'
    component = 'Port'
    material = 'Vacuum'
    Xrange = [0,l0]
    Yrange = [-b0/2,b0/2]
    Zrange = [-a0/2,a0/2]
    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)


    filter_start =  l0 + coupling_length
    Name = 'resonador'
    component = 'Resonators'
    material = 'Vacuum'
    Xrange = [filter_start, filter_start + filter_length]
    Yrange = [-filter_height/2, filter_height/2]
    Zrange = [-filter_width/2, filter_width/2]
    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
    Add( mws, "Unir acoples", 'Port', 'puerto 1', 'Resonators', Name)
    
    if model == 1:
        coupling_start = l0 
        Name = 'Iris'
        component = 'Coupling'
        material = 'Vacuum'
        Xrange = [coupling_start, coupling_start + coupling_length]
        Yrange = [-filter_height/2, filter_height/2]
        Zrange = [-iris_width/2, iris_width/2]
        Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
        Add( mws, "Unir acoples", 'Port', 'puerto 1', 'Coupling', Name)
    if model == 2:
        coupling_start = l0 
        copling_delay = 4.1
        Name = 'Iris'
        component = 'Coupling'
        material = 'Vacuum'
  
        Xrange = [coupling_start, coupling_start + coupling_length]
        Yrange = [-iris_width/2+copling_delay, iris_width/2+copling_delay]
        Zrange = [-filter_width/2, filter_width/2]

        Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
        Add( mws, "Unir acoples", 'Port', 'puerto 1', 'Coupling', Name)