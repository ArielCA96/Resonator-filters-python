

def AddToHistoryWithCommand(mws, Tag, Command):
    mws._FlagAsMethod("AddToHistory")
    mws.AddToHistory(Tag, Command)

def Subtract( mws, Tag, component1, name1, component2, name2):
    sCommand = f'Solid.Subtract "{component1}:{name1}", "{component2}:{name2}"'
    AddToHistoryWithCommand(Tag, sCommand)

def Add( mws, Tag, component1, name1, component2, name2):
    sCommand = f'Solid.Add "{component1}:{name1}", "{component2}:{name2}"'
    AddToHistoryWithCommand(mws, Tag, sCommand) 

def BlendEdge(mws, Tag, radius):
    sCommand = f'Solid.BlendEdge "{radius}"'
    AddToHistoryWithCommand(mws, Tag, sCommand)

def Insert(mws, Tag, component1, name1, component2, name2):
    sCommand = f'Solid.Insert "{component1}:{name1}", "{component2}:{name2}"'
    AddToHistoryWithCommand(mws, Tag, sCommand)