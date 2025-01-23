def CstDefineElectricBoundary(mws):
    boundary = mws.Boundary
    #plot = mws.Plot
    boundary.Xmin("electric")
    boundary.Xmax("electric")
    boundary.Ymin("electric")
    boundary.Ymax("electric")
    boundary.Zmin("electric")
    boundary.Zmax("electric")
    boundary.Xsymmetry('none')
    boundary.Ysymmetry('none')
    boundary.Zsymmetry('none')
    boundary.ApplyInAllDirections('True')