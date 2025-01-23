import os
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
import numpy as np

def ExportarResultadosCST(mws, Config: FiltroResonanteConfig):
    results_path = Config.get_simulation_results_path()
    filename = Config.generate_filename()
    file_path = os.path.join(results_path, filename)
    print(file_path)

    # Seleccionar el primer parámetro S
    #sCommand = f"""
    #        'set the solver type
    #        SelectTreeItem("1D Results\S-Parameters\S1,1")'
    #        """
    #mws._FlagAsMethod("AddToHistory")
    #mws.AddToHistory('Set Solver Type', sCommand)

    TreeItem = "1D Results\\S-Parameters\\S1,1"
    IDs = mws.Resulttree.GetResultIDsFromTreeItem(TreeItem)
    spara = mws.Resulttree.GetResultFromTreeItem(TreeItem, IDs[0])
    FrequencyRange = np.array(spara.GetArray("x"))
    SRE = spara.GetArray("yre")
    SIM = spara.GetArray("yim")
    # Calculate the magnitude in dB
    magnitude_s11_dB = 20 * np.log10(np.sqrt(np.array(SRE)**2 + np.array(SIM)**2))

    TreeItem = "1D Results\\S-Parameters\\S2,1"
    IDs = mws.Resulttree.GetResultIDsFromTreeItem(TreeItem)
    spara = mws.Resulttree.GetResultFromTreeItem(TreeItem, IDs[0])
    SRE = spara.GetArray("yre")
    SIM = spara.GetArray("yim")
    # Calculate the magnitude in dB
    magnitude_s21_dB = 20 * np.log10(np.sqrt(np.array(SRE)**2 + np.array(SIM)**2))

    ep_s11 = f"{file_path}.txt"

    data = np.column_stack((FrequencyRange, magnitude_s11_dB, magnitude_s21_dB))
    os.makedirs(results_path, exist_ok=True)
    np.savetxt(ep_s11, data, delimiter='\t', header='Frequency\tS11(dB)\tS21(dB)', comments='')

    # Save the matrix from Config
    matrix = np.array(Config.matrix)
    matrix_file_path = os.path.join(results_path, f"{filename}_matrix.npy")
    np.save(matrix_file_path, matrix)

    #mws.SelectTreeItem("""'1D Results\S-Parameters\S1,1'""")
    #ascii_export = mws.ASCIIExport
    #ascii_export.Reset()
    #ascii_export.FileName(r"c:\Users\calzadilla.166495\Documents\Filtros\Resonator-filters-python\Simulation\Resultados de simulación\Re_0_Ma_4_1_Id_0_S11.txt")
    #ascii_export.Execute()