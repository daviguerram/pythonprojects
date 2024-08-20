# app.py
from tkinter import Tk
from frontend import Gui
from backend import TransactionObject

# Inicializar o banco de dados (caso ainda não tenha sido feito)
TransactionObject().initDB()

# Inicializar a interface gráfica
window = Tk()
app = Gui(window)
app.run()
