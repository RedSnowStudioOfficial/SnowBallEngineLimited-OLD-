import time as tm
import tkinter as tk

game_on = True
FPS = 60
a = 0

root = tk.Tk()

while game_on == True:

    a += 1
    
    if a == 60:
        print(a)
        a = 0
    
    tm.sleep(1/FPS)
