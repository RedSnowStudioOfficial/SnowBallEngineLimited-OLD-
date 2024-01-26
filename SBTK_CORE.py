import os #Для возможности прописи сценариев взаимодействующих с OS (Выключение ПК или что либо ещё)

import time as tm #Попытка обновлять всё за время физические процессы*

import tkinter as tk
from tkinter import ttk

import Settings as STT

class GameCanvas(tk.Canvas):
    
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()
        
        self.counter = 0
        
        print("CanvaTool активированна", "\n")
        
    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, wscale, hscale)
        
    def resize_obj(self, obj):
        pass

    def update_by_tick(self, misec, upd_func):
        self.update_idletasks()
        self.after(int(misec), upd_func)
    
    def update_by_time(self):
        pass

class GameWindow(tk.Tk):

    def __init__(self, title:str, width:float, height:float, resizable:bool, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.title(title)
        self.geometry(str(width)+"x"+str(height))
        self.resizable(resizable, resizable)

        # self.attributes('-fullscreen', False)
        # self.fullscreen_state = False
        # self.bind("<F4>", self.toggleFullScreen)
        # self.bind("<Escape>", self.quitFullScreen)
        
        print("WindowTool активированна", "\n")
    
    def update_by_tick(self, ms, func):
        self.update()

        self.after(ms, func)

    def game_mainloop(self, canva):
        canva.pack(expand=True, fill="both")

        self.mainloop()

'''
    # def toggleFullScreen(self, event):
        # if self.ratio == "Rect":
            # self.canva.pack_configure(padx=155, ipadx=155)
        # elif self.ratio == "Wide":
            # self.canva.pack_configure(padx=0, ipadx=0)
        # self.fullScreenState = True
        # self.attributes("-fullscreen", self.fullScreenState)

    # def quitFullScreen(self, event):
        # self.canva.pack_configure(padx=0, ipadx=0)
        # self.fullScreenState = False
        # self.attributes("-fullscreen", self.fullScreenState)
'''

class InputTool:
    
    def __init__(self, parent) -> None:
        self.parent = parent

        self.key = ""
        self.PRESSED = False
        self.RELEASED = False

        print("InputTool активированна", "\n")
        
    def key_press(self, event):
        #print("Нажата клавиша", event.keysym, event)
        self.key = event.keysym
        self.PRESSED = True
        self.RELEASED = False

    def key_release(self, event):
        #print("Нажата клавиша", event.keysym, event)
        self.key = event.keysym
        self.PRESSED = False
        self.RELEASED = True

    def get_key(self):
        return self.key
    
    def get_press_state(self):
        return self.PRESSED

    def get_release_state(self):
        return self.RELEASED

    def UPDATE(self):
    
        self.parent.bind_all("<KeyPress>", self.key_press)
        self.parent.bind_all("<KeyRelease>", self.key_release)
        
        self.parent.focus_set()

class AudioTool:

    def __init__(self):
        pass

    def play_sound(self, audio):
        pass

class SpriteObject:
    
    def __init__(self, name, canva, source_image, x1, y1, width, height):

        self.source_image = source_image
        
        self.canva = canva

        self.sprite_info = tk.PhotoImage(width=width, height=height)
        self.sprite_info_mirror = tk.PhotoImage(width=width, height=height)

        for i in range(0, width):
            for j in range(0, height):
                self.sprite_info.put('#%02x%02x%02x' % source_image.get(x1+i, y1+j), to=(i, j))
        
        self.sprite_obj = None
        
    def set_transperent_color_rgb(self, color):
        width, height = self.sprite_info.width(), self.sprite_info.height()
    
        #Удаление заднего слоя на прозрачность
        #Пробегаемся по пикселям картинки
        for x in range(width): #Берём параметр ширины и высоты и пробегаемся по всем пиксялям
            for y in range(height):
                if self.sprite_info.get(x, y) == color:
                    self.sprite_info.transparency_set(x, y, 1)

    def make_mirror_copy(self):
        width, height = self.sprite_info.width(), self.sprite_info.height()
        
        for x in range(width):
            for y in range(height):
                self.sprite_info.put('#%02x%02x%02x' % self.sprite_info.get(width - x, y + 1), to=(x, y))
    
    def scale(self, amount:int):
        if amount < 0:
            amount = amount * -1

            self.sprite_info = self.sprite_info.subsample(amount, amount)

        else:
        
            self.sprite_info = self.sprite_info.zoom(amount, amount)
        
    def draw_in(self, Xpos, Ypos): #, h_mirror:bool, v_mirror:bool):
        self.sprite_obj = self.canva.create_image(Xpos, Ypos, image=self.sprite_info)

    def clear_out(self):
        self.canva.delete(self.sprite_obj)
     
class AnimFrameObject:
    def __init__(self, sprite):
        self.current_frame = sprite # Объект спрайта
        self.nextFrame = None # Слудующий кадр
        self.prevFrame = None # Предыдущий кадр
        #self.duration = 0.0 # Время задержки на кадре*

class AnimationTool:
    def __init__(self, canva):
        self.canva = canva
        
        self._Start = None
        self._End = None
        
        self.Loop = False

        self.TimerINT : int = 0
        self.TimerFLOAT : float = 0.0

        self.main_sprite = None
        
    def Add_New_Frame_IN_END(self, sprite):
        
        new_ = AnimFrameObject(sprite)
        
        if self._Start == None:
            self._Start = new_
            self._End = new_
        else:
            self._End.nextFrame = new_
            self._End = new_
        
    def Add_New_Frame_IN_BEGIN(self, sprite, duration):
        
        new_ = AnimFrameObject(sprite, duration)

        if self._Start == None:
            self._Start = new_
            self._End = new_
        else:
            new_.nextFrame = self._Start
            self._Start = new_

    def add_between(self, elem, pos):
        
        new_ = Node(elem)

        p = self._Start
        prev = None

        counter = 0

        if p == None:
            self.Add_in_end(elem)
        else:
            if pos == 0:
                self.Add_in_begin(elem)
            else:
                while p != None and counter != pos:
                    counter += 1
                    prev = p
                    p = p.nextNode
                        
                else:
                    new_.nextNode = p
                    prev.nextNode = new_

'''
class Poligon2DObject:
    def __init__(self, elem):
        self.elem = elem

class Poligon2DTool:
    def __init__(self):
        """
        Эксперементально! Позволяет создавать псевдо 3Д объекты
        с помощью 2Д примитивов и картинок
        """
        pass
'''

if __name__ == "__main__":
    pass
    
