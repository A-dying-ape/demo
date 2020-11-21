import time
import tkinter as tk
from view import Make_UI


def expired():
    curry_time = int(time.time())
    if curry_time >= (1604656363 + 2*60*60):
        return
    else:
        window = tk.Tk()
        mu = Make_UI(window)
        mu.decorate_page()
        window.mainloop()


if __name__ == '__main__':
    expired()