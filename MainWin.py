from SBTK_CORE import *
import tkinter as tk

class MainWin():
    def __init__(self):
        
        self.root = tk.Tk()
        
        self.root.title("SnowBallEngine - Менеджер Окрежением")
        self.root.geometry("400x600")
        
        self.root.configure(bg="black") #Настройка для всех окон! Должна быть общая настройка среды!
        
        #MAIN WIDGET's
        
        '''
        Таблицы с инструментами
        '''
        
        #PACK's
        
        
        self.root.mainloop()
        
    def click_on_tool(self, event):
        pass

MainWin()
