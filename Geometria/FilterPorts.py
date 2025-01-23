def FilterPorts(mws, PortNumber, NumberOfModes, Xrange, Yrange, Zrange, XrangeAdd, YrangeAdd, ZrangeAdd, Coordinates, Orientation):
    port = mws.Port
    port.Reset()
    port.PortNumber(str(PortNumber))
    port.Label('')
    port.Folder('')
    port.NumberOfModes(str(NumberOfModes))
    port.AdjustPolarization('False')
    port.PolarizationAngle('0.0')
    port.ReferencePlaneDistance('0')
    port.TextSize('50')
    port.TextMaxLimit('0')
    port.Coordinates(Coordinates)
    port.Orientation(Orientation)
    port.PortOnBound('True')
    port.ClipPickedPortToBound('False')
    port.Xrange(str(Xrange[1]), str(Xrange[0]))
    port.Yrange(str(Yrange[1]), str(Yrange[0]))
    port.Zrange(str(Zrange[1]), str(Zrange[0]))
    port.XrangeAdd(str(XrangeAdd[0]), str(XrangeAdd[1]))
    port.YrangeAdd(str(YrangeAdd[0]), str(YrangeAdd[1]))
    port.ZrangeAdd(str(ZrangeAdd[0]), str(ZrangeAdd[1]))
    port.SingleEnded('False')
    port.WaveguideMonitor('False')
    port.Create()




