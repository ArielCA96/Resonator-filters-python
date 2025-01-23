from Geometria.CstBrick import Cstbrick
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig

def CrearFiltroResonante(mws, Config: FiltroResonanteConfig):
    brick = mws.Brick

    # Puertos
    a0 = Config.a0  # mm
    b0 = Config.b0  # mm
    l0 = Config.l0 # mm
    
    # Resonadores
    num_resonators = Config.num_resonators
    filter_width = Config.filter_width  # mm
    filter_height = Config.filter_height  # mm
    filter_length = Config.filter_length  # mm

    # Acopladores
    coupling_length = Config.coupling_length  # mm
    grid_width = Config.grid_width  # mm
    num_holes = Config.num_holes  # [ancho, alto]
    matriz = Config.matrix
    matriz = matriz[::-1]

    brick_height = Config.brick_height  # mm
    brick_width = Config.brick_width  # mm

    coupling_height = num_holes[1] * (brick_height + grid_width) + grid_width
    coupling_width = num_holes[0] * (brick_width + grid_width) + grid_width

    # Crear puerto 1    
    Name = 'puerto 1'
    component = 'Port'
    material = 'Vacuum'
    Xrange = [0,l0]
    Yrange = [-b0/2,b0/2]
    Zrange = [-a0/2,a0/2]
    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)

    # Crear puerto 2    
    port_position = l0 + num_resonators*filter_length + (num_resonators+1)*coupling_length
    Name = 'puerto 2'
    component = 'Port'
    material = 'Vacuum'
    Xrange = [port_position, port_position+l0]
    Yrange = [-b0/2,b0/2]
    Zrange = [-a0/2,a0/2]
    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)

    # Crear resonadores
    for i in range(num_resonators):
        filter_start =  l0 + coupling_length + i*(filter_length+coupling_length)
        Name = 'resonador ' + str(i)
        component = 'Resonators'
        material = 'Vacuum'
        Xrange = [filter_start, filter_start + filter_length]
        Yrange = [-filter_height/2, filter_height/2]
        Zrange = [-filter_width/2, filter_width/2]
        Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)
    
    # Crear acopladores
    point = [-coupling_width/2 + grid_width, -coupling_height/2 + grid_width]
    for i in range(num_resonators + 1):
        coupling_start = l0 + i * (filter_length + coupling_length)
        for j in range(num_holes[0]):
            for k in range(num_holes[1]):
                if matriz[k][j] == 1:  # Note: matriz[k][j] instead of matriz[j][k] to match the dimensions
                    
                    Name = f'acoplador {i}_{j}_{k}'
                    component = 'Coupling'
                    material = 'Vacuum'
                    Xrange = [coupling_start, coupling_start + coupling_length]
                    Yrange = [point[1] + brick_height*(k+1) + grid_width*k, point[1] + brick_height*k + grid_width*k ]
                    Zrange = [point[0] + brick_width*(j+1) + grid_width*j, point[0] + brick_width*j + grid_width*j ]
                    Cstbrick(mws, Name, component, material, Xrange, Yrange, Zrange)