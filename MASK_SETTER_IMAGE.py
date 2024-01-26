import tkinter as tk
from PIL import Image, ImageTk, ImageOps

root = tk.Tk()

canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

# загрузка изображения с помощью Pillow
pil_image = Image.open("Resources\Tails1.gif")

# удаление красного цвета
pil_image = ImageOps.invert(pil_image)
pil_image = ImageOps.colorize(pil_image, (0, 0, 0), (255, 255, 255))

# создание объекта ImageTk из измененного изображения
image = ImageTk.PhotoImage(pil_image)

canvas.create_image(100, 100, image=image)

root.mainloop()
