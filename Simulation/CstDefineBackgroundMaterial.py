def CstDefineBackgroundMaterial(mws, type):
    background = mws.Background
    material = mws.Material

    background.ResetBackground()
    background.XminSpace(str(0))
    background.XmaxSpace(str(0))
    background.YminSpace(str(0))
    background.YmaxSpace(str(0))
    background.ZminSpace(str(0))
    background.ZmaxSpace(str(0))
    background.ApplyInAllDirections('False')

    material.Reset()
    material.Rho('0.0')
    material.ThermalType('Normal')
    material.ThermalConductivity('0.0')
    material.SpecificHeat('0', "J/K/kg")
    material.DynamicViscosity('0')
    material.Emissivity('0')
    material.MetabolicRate('0')
    material.VoxelConvection('0')
    material.BloodFlow('0')
    material.MechanicsType("Unused")
    material.IntrinsicCarrierDensity('0')
    material.FrqType('all')
    material.Type(type)
    material.MaterialUnit('Frequency', 'Hz')
    material.MaterialUnit('Geometry', 'm')
    material.MaterialUnit('Time', 's')
    material.MaterialUnit('Temperature', 'Kelvin')

    material.Epsilon('1.0')
    material.Mue('1.0')
    material.Sigma('0.0')
    material.TanD('0.0')
    material.TanDFreq('0.0')
    material.TanDGiven('False')
    material.TanDModel('ConstSigma')
    material.SetConstTanDStrategyEps('AutomaticOrder')
    material.ConstTanDModelOrderEps('3')
    material.DjordjevicSarkarUpperFreqEps( "0")
    material.SetElParametricConductivity('False')
    material.ReferenceCoordSystem('Global')
    material.CoordSystemType('Cartesian')
    material.SigmaM('0')
    material.TanDM('0.0')
    material.TanDMFreq('0.0')
    material.TanDMGiven('False')
    material.TanDMModel('ConstSigma')
    material.SetConstTanDStrategyMu("AutomaticOrder")
    material.ConstTanDModelOrderMue('3')
    material.DjordjevicSarkarUpperFreqMu("0")
    material.SetMagParametricConductivity('False')
    material.DispModelEps('None')
    material.DispModelMue('None')
    material.DispersiveFittingSchemeEps('Nth Order')
    material.MaximalOrderNthModelFitEps('10')
    material.ErrorLimitNthModelFitEps('0.1')
    material.UseOnlyDataInSimFreqRangeNthModelEps('False')
    material.DispersiveFittingSchemeMue('Nth Order')
    material.MaximalOrderNthModelFitMue('10')
    material.ErrorLimitNthModelFitMue('0.1')
    material.UseOnlyDataInSimFreqRangeNthModelMue('False')
    material.UseGeneralDispersionEps('False')
    material.UseGeneralDispersionMue('False')
    material.NLAnisotropy('False')
    material.NLAStackingFactor('1')
    material.NLADirectionX('1')
    material.NLADirectionY('0')
    material.NLADirectionZ('0')
    material.Colour('0.6', '0.6', '0.6')
    material.Wireframe('False')
    material.Reflection('False')
    material.Allowoutline('True')
    material.Transparentoutline('False')
    material.Transparency('0')
    material.ChangeBackgroundMaterial()
