import tkinter as tk
from view import Make_UI


window = tk.Tk()
mu = Make_UI(window)
mu.decorate_page()
window.mainloop()