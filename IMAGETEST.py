import tkinter as tk
from tkinter import ttk

import Conteiners.spisok as SP

root = tk.Tk()
root.title("IMAGE PPE TEST")
root.geometry("640x480")

canvas = tk.Canvas(bg="#22bf74", width=1000, height=1000)


image = tk.PhotoImage(file="Resources/Tails1.png")

#Увеличивает картинку Х У координаты
#image = image.zoom(2, 2)

#Уменьшает картинку Х У координаты (минусовыми координатами можно отражать картинку по Х и У)
#image = image.subsample(1, 1)

# Получите размер изображения
width = image.width()
height = image.height()

#print(f"Ширина: {width} пикселей")
#print(f"Высота: {height} пикселей")

def color_to_alpha(image, color):
    
    width, height = image.width(), image.height()
    
    #Удаление заднего слоя на прозрачность
    #Пробегаемся по пикселям картинки
    for x in range(width): #Берём параметр ширины и высоты и пробегаемся по всем пиксялям
        for y in range(height):
            if image.get(x, y) == color:
                image.transparency_set(x, y, 1)

def mirror_h(image):
    pass

def copy_sprite_from_image(source_image, x1, y1, width, height):
    
    sprite = tk.PhotoImage(width=width, height=height)
    
    for i in range(0, width):
        for j in range(0, height):
            sprite.put('#%02x%02x%02x' % source_image.get(x1+i, y1+j), to=(i, j))
    
    return sprite

def draw_sprite_frame(image, Xpos, Ypos):

    width=image.width()/2
    height=image.height()/2
    
    canvas.create_image(Xpos, Ypos, image = image)
##    canvas.create_rectangle(Xpos-width, Ypos-height,
##                            Xpos+width, Ypos+height,
##                            fill = "red")
    
f1 = copy_sprite_from_image(image, 1, 1, 24, 32)
f2 = copy_sprite_from_image(image, 26, 1, 24, 32)
f3 = copy_sprite_from_image(image, 51, 1, 24, 32)

f1 = f1.zoom(3,3)
f2 = f2.zoom(3,3)
f3 = f3.zoom(3,3)

color_to_alpha(f1, (255, 0, 255))
color_to_alpha(f2, (255, 0, 255))
color_to_alpha(f3, (255, 0, 255))

sprite = canvas.create_image(640/2, 320/2, image = f1)
# canvas.create_rectangle(500, 5, 550, 55, fill="red")

def frame_next():
    canvas.itemconfigure(sprite, image = f2)

butt = ttk.Button(root, text="Слудующий кадр ->", command=frame_next)
butt.pack()

canvas.pack()
#canvas.create_image(0, 0, image = image)

root.mainloop()




























# from tkinter import *  
# from PIL import ImageTk,Image  

# '''
# box = (100, 100, 400, 400)
# region = im.crop(box)
# '''

# class SpriteTool:
    # def __init__(self, canva, img_path : str, x, y):
        # self.image = ImageTk.PhotoImage(Image.open(img_path))
        
        # self.canva = canva
        
        # self.sprite = None
        
        # self.center = None
        
        # self.x_pos = x
        # self.y_pos = y
        
    # def draw_in(self):
        # self.sprite = self.canva.create_image(self.x_pos,
                                            # self.y_pos,
                                            # image=self.image) 
        
        # self.center = self.canva.create_rectangle(self.x_pos-5,
                                            # self.y_pos-5,
                                            # self.x_pos+5,
                                            # self.y_pos+5,
                                            # fill="red")
        
    
    # def clear_out(self):
        # self.canva.delete(self.sprite)
    
    # def region_crop(self, x1, y1, x2, y2):
        # box = (x1, y1, x2, y2)
        # region = self.image.crop(box)
        
# class AnimateTool:
    # def __init__(self, canva):
        # self.canva = canva
        
        
        
    # def draw_in(self):
        # pass
    
    
# ws = Tk()  
# ws.title('PythonGuides')
# ws.geometry('800x800')

# canva = Canvas(ws, 
                # width = 1000, 
                # height = 1000, bg="black")
                
# canva.pack()

# spr = SpriteTool(canva, 'Resources/Tails1.png', 200, 500)
# spr.region_crop(1, 1, 20, 40)
# spr.draw_in()

# # img = ImageTk.PhotoImage(Image.open('Resources/Tails1.png'))  
# # canvas.create_image(
        # # 10, 
        # # 10, 
        # # anchor=NW, 
        # # image=img
        # # ) 
# ws.mainloop() 


# '''
# from RSS_SDK import *

# import PIL as pl

# win = WindowTool("TOOL's TEST", STT.screen_size[0], STT.screen_size[1], 0)

# canva = CanvasTool(win, width=STT.screen_size[0], height=STT.screen_size[1], bg="black", highlightthickness=0)

# im = pl.Image.open("hopper.ppm")
# im.show()

# win.UPDATE(canva)
# '''

'''
# -Вывод картинки
# -Анимация с вырезкой
# -Анимация с картинками

-Сделать увеличение и уменьшение картинки с статичными координатами
-Сделать вращение картинки
-Сделать смену цветов (палитры)

#############################
Для Poligon2D
-Сделать повороты относительно перспективы
'''

# from PIL import Image, ImageTk
# import tkinter as tk
# from tkinter import ttk

# image_scale = 6

# root = tk.Tk()

# canvas = tk.Canvas(root, width=500, height=500, bg="black")
# canvas.pack()

# image = Image.open("Resources/Tails1.png")

# # Вырезка фона по цвету
# image.convert("RGBA")
# datas = image.getdata()
# newData = []

# for item in datas:
    # if item[0] == 255 and item[1] == 0 and item[2] == 255:
        # newData.append((255, 255, 255, 0))
    # else:
        # newData.append(item)
        
# image.putdata(newData)

# # Изменение размера картинки
# width, height = image.size

# image = image.resize((width*image_scale, height*image_scale), Image.NEAREST)

# #Вырезка области картинки*
# crop1 = image.crop((1*image_scale, 34*image_scale, 44*image_scale, 66*image_scale))
# crop2 = image.crop((46*image_scale, 34*image_scale, 87*image_scale, 66*image_scale))
# crop3 = image.crop((88*image_scale, 34*image_scale, 129*image_scale, 66*image_scale))
# crop4 = image.crop((130*image_scale, 34*image_scale, 164*image_scale, 66*image_scale))
# crop5 = image.crop((165*image_scale, 34*image_scale, 209*image_scale, 66*image_scale))
# crop6 = image.crop((210*image_scale, 34*image_scale, 249*image_scale, 66*image_scale))
# crop7 = image.crop((1*image_scale, 67*image_scale, 42*image_scale, 99*image_scale))
# crop8 = image.crop((43*image_scale, 67*image_scale, 77*image_scale, 99*image_scale))

# crops = [crop1,
         # crop2,
         # crop3,
         # crop4,
         # crop5,
         # crop6,
         # crop7,
         # crop8]

# cropped_photo1 = ImageTk.PhotoImage(crop1)
# cropped_photo2 = ImageTk.PhotoImage(crop2)
# cropped_photo3 = ImageTk.PhotoImage(crop3)
# cropped_photo4 = ImageTk.PhotoImage(crop4)
# cropped_photo5 = ImageTk.PhotoImage(crop5)
# cropped_photo6 = ImageTk.PhotoImage(crop6)
# cropped_photo7 = ImageTk.PhotoImage(crop7)
# cropped_photo8 = ImageTk.PhotoImage(crop8)

# photos = [cropped_photo1,
          # cropped_photo2,
          # cropped_photo3,
          # cropped_photo4,
          # cropped_photo5,
          # cropped_photo6,
          # cropped_photo7,
          # cropped_photo8]

# sprite = canvas.create_image(100, 100, image=cropped_photo1)
# canvas.create_rectangle(100-5*image_scale, 100-5*image_scale, 100+5*image_scale, 100+5*image_scale, fill="red")

# p = 0
 
# horizontalScale = ttk.Scale(orient="horizontal", length=200, from_=1.0, to=100.0, variable=50)
# horizontalScale.pack(anchor="nw")

# def button_click():
    # global p
    
    # if p < 7:
        # p+=1
    # elif p >= 7:
        # p = 0
    
    # # cropped_photo = ImageTk.PhotoImage(crops[p])
    
    # canvas.itemconfigure(sprite, image=photos[p])

# butt = tk.Button(root, text="next frame", command=button_click)
# butt.pack()

# #Вставка вырезанной картинки в PhotoImage

# root.mainloop()

# from PIL import Image, ImageTk
# import tkinter as tk

# root = tk.Tk()

# canvas = tk.Canvas(root, width=1000, height=1000, bg="black")
# canvas.pack()

# image = Image.open("Resources/Tails1.png")
# #Вырезка области картинки*
# cropped_image = image.crop((1, 1, 24, 32))

# #Вставка вырезанной картинки в PhotoImage
# cropped_photo = ImageTk.PhotoImage(cropped_image)

# canvas.create_image(100, 100, image=cropped_photo)
# canvas.create_rectangle(100-5, 100-5, 100+5, 100+5, fill="red")

# root.mainloop()


# import tkinter as tk

# root = tk.Tk()

# canvas = tk.Canvas(root, width=1000, height=1000, bg="black")
# canvas.pack()

# img = tk.PhotoImage(file="Resources/Tails1.png")
# canvas.create_image(200, 200, image=img)
# canvas.create_rectangle(200-5, 200-5, 200+5, 200+5)

# root.mainloop()

# import tkinter as tk

# def create_reflected_image(canvas, image):
    # # Получите размеры изображения
    # image_width = image.width()
    # image_height = image.height()
    
    # # Создайте отраженную копию изображения
    # reflected_image = image.copy()
    # reflected_image = reflected_image.transpose(method=tk.Transpose.ROTATE_180)

    # # Нарисуйте отраженную копию на Canvas
    # canvas.create_image(image_width // 2, image_height, image=reflected_image)

# # Создайте окно Tkinter
# root = tk.Tk()
# root.title("Отражение изображения")

# # Загрузите изображение (замените "your_image.png" на путь к вашему изображению)
# image = tk.PhotoImage(file="Resources/Tails1.png")

# # Создайте виджет Canvas и нарисуйте на нем изображение
# canvas = tk.Canvas(root, width=image.width(), height=image.height() * 2)
# canvas.create_image(image.width() // 2, image.height() // 2, image=image)

# # Создайте отраженную копию и нарисуйте ее на Canvas
# create_reflected_image(canvas, image)

# canvas.pack()

# root.mainloop()
