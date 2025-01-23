import os

class FiltroResonanteConfig:
    def __init__(self, a0=19.05, b0=9.525, l0=5, num_resonators=5, filter_width=30, filter_height=15, filter_length=8, 
                 coupling_length=1, grid_width=0.3, num_holes=[5, 3], matrix=None, brick_height=2, brick_width=2, id=0):
        
        # Puertos
        self.a0 = a0    #mm
        self.b0 = b0    #mm
        self.l0 = l0    #mm

        # Resonadores
        self.num_resonators = num_resonators
        self.filter_width = filter_width    #mm
        self.filter_height = filter_height    #mm
        self.filter_length = filter_length    #mm

        # Acopladores
        self.coupling_length = coupling_length    #mm
        self.grid_width = grid_width             #mm
        self.num_holes = num_holes
        self.matrix = matrix if matrix else [[1 for _ in range(self.num_holes[0])] for _ in range(self.num_holes[1])]
        self.brick_height = brick_height        #mm
        self.brick_width = brick_width          #mm

        # Port 1
        self.xrange_p1 =[0,0]
        self.yrange_p1 = [b0/2, -b0/2]
        self.zrange_p1 = [a0/2, -a0/2]

        # Port 2 
        end_filter = l0*2 + num_resonators*filter_length + (num_resonators+1)*coupling_length
        self.xrange_p2 =[end_filter, end_filter]
        self.yrange_p2 = [b0/2, -b0/2]
        self.zrange_p2 = [a0/2, -a0/2]

        self.id = id



    def get_simulation_results_path(self):
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_path = os.path.join(base_path, 'Resultados de simulación')
        return results_path

    def generate_filename(self):
        filename = f"Re_{self.num_resonators}_Ma_{self.num_holes[0]}_{self.num_holes[1]}_Id_{self.id}"
        return filename
