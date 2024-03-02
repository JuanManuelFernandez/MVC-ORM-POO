"""
main:
        archivo que se utiliza para ejecutar la app
"""

from tkinter import Tk
import vista

if __name__ == "__main__":
    root = Tk()
    vista.CreacionVentana(root)
    root.mainloop()