def cstFR4Lossy(mws):
    # Nombre del material
    name = 'FR-4 (lossy)'

    # Comando en formato de cadena
    sCommand = f"""
    With Material
        .Reset
        .Name "{name}"
        .Folder ""
        .FrqType "all"
        .Type "Normal"
        .SetMaterialUnit "GHz", "mm"
        .Epsilon "4.3"
        .Mu "1.0"
        .Kappa "0.0"
        .TanD "0.025"
        .TanDFreq "10.0"
        .TanDGiven "True"
        .TanDModel "ConstTanD"
        .KappaM "0.0"
        .TanDM "0.0"
        .TanDMFreq "0.0"
        .TanDMGiven "False"
        .TanDMModel "ConstKappa"
        .DispModelEps "None"
        .DispModelMu "None"
        .DispersiveFittingSchemeEps "General 1st"
        .DispersiveFittingSchemeMu "General 1st"
        .UseGeneralDispersionEps "False"
        .UseGeneralDispersionMu "False"
        .Rho "0.0"
        .ThermalType "Normal"
        .ThermalConductivity "0.3"
        .SetActiveMaterial "all"
        .Colour "0.94", "0.82", "0.76"
        .Wireframe "False"
        .Transparency "0"
        .Create
    End With
    """

    # Agregar a la historia
    mws._FlagAsMethod("AddToHistory")
    mws.AddToHistory('define material: FR-4 (lossy)', sCommand)