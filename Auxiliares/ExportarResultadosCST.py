import os
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
import numpy as np

def ExportarResultadosCST(mws, Config: FiltroResonanteConfig):
    results_path = Config.get_simulation_results_path()
    filename = Config.generate_filename()
    file_path = os.path.join(results_path, filename)
    Config.save_config(results_path, filename)

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