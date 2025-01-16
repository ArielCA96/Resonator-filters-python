import win32com.client

# Crear una instancia del servidor OLE Automation de CST
cst = win32com.client.Dispatch('CSTStudio.Application')

# Crear una nueva ventana de trabajo
mws = cst.NewMWS()