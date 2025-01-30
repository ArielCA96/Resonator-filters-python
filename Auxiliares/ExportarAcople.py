import os
from Simulation.FiltroResonanteConfig import FiltroResonanteConfig
import numpy as np

def ExportarAcople(mws, Config: FiltroResonanteConfig):
    results_path = Config.get_iris_copling_results_path()
    filename = Config.generate_iris_copling_filename()
    file_path = os.path.join(results_path, filename)

    TreeItem = "1D Results\\S-Parameters\\S1,1"
    IDs = mws.Resulttree.GetResultIDsFromTreeItem(TreeItem)
    spara = mws.Resulttree.GetResultFromTreeItem(TreeItem, IDs[0])
    FrequencyRange = np.array(spara.GetArray("x"))
    SRE = spara.GetArray("yre")
    SIM = spara.GetArray("yim")
    # Calculate the magnitude in dB
    s11_dB = 20 * np.log10(np.sqrt(np.array(SRE)**2 + np.array(SIM)**2))

    TreeItem = "1D Results\\S-Parameters\\S2,1"
    IDs = mws.Resulttree.GetResultIDsFromTreeItem(TreeItem)
    spara = mws.Resulttree.GetResultFromTreeItem(TreeItem, IDs[0])
    SRE = spara.GetArray("yre")
    SIM = spara.GetArray("yim")
    # Calculate the magnitude in dB
    s21_dB = 20 * np.log10(np.sqrt(np.array(SRE)**2 + np.array(SIM)**2))

    import matplotlib.pyplot as plt


    # Calculate the derivative of s21 using central difference method
    s21_derivative = np.diff(s21_dB) / np.diff(FrequencyRange)
    # Adjust the length of the derivative array to match the original data length
    s21_derivative = np.concatenate(([s21_derivative[0]], s21_derivative))
    

    # Find the points where the slope changes from positive to negative
    zero_derivative_indices = np.where(np.diff(np.sign(s21_derivative)))[0]
    # Get the two points with the highest s21 values
    top_two_indices = np.argsort(s21_dB[zero_derivative_indices])[-2:]
    zero_derivative_indices = zero_derivative_indices[top_two_indices]

    f1 = FrequencyRange[zero_derivative_indices[0]]
    f2 = FrequencyRange[zero_derivative_indices[1]]
    coupling = (f1 **2 - f2**2)/(f1**2 + f2**2)
    coupling = abs(coupling)

    Config.save_config_iris_filter(results_path, filename, s21_dB, s11_dB, FrequencyRange[zero_derivative_indices], coupling)

    # Plot the curve S21
    """plt.figure(figsize=(10, 6))
    plt.plot(FrequencyRange, s21_dB, label='S21 (dB)')
    plt.scatter(FrequencyRange[zero_derivative_indices], s21_dB[zero_derivative_indices], color='red', zorder=5, label='Zero Derivative Points')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('S21 (dB)')
    plt.title('S21 vs Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()"""

    return coupling