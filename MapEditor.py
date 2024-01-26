from SBTK_CORE import *
from game_algorithms import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import tkinter as tk
import os
import math
import pickle
import Conteiners.spisok as SP #Двойной список
import Settings as STT

'''
Редактор работает как Hammer Editor разработанный Valve для игры Half-Life 2
Он позволяет наглядно редактировать геометрию уровня,
расставлять объекты из библиотеки игры,
моделировать маленькие сценки с помощью визуального программирования
и взаимодействия специальных обхектов игры*
Данный редактор НЕ ПОЗВОЛЯЕТ запускать сам игровой процесс внутри самого себя,
а лишь является инструментом который на выходе должен выдавать
зашифрованный текстовый файл с уникальным расширением* .SBmap .SBscript

###Масштабирование

Долгое время я думал как реализовать отдаление и приближение канвы для удобного редактирования карт
Всё оказалось довольно просто, нам нужно иметь при себе два значения канвы:
    -Реальный размер для игры
    -Динамичный размер для редактора

Реальный размер не изменчив, в угоду эффекта приблежения Динамичный же будет умножаться на диапозон от 0.1 до 2
Где 2 это сымое дальнее отдаление, а 0.1 самое близкое приблежение

Объекты в редакторе будут перерисованы, относительно своих позиций установленных на реальном размере
Так же они будут отмасштабированы по размеру канвы редактора, относительно Динамичного размера

Будет произведена попытка ввести возможность скриптинга карт! Не понимаю ещё как...
Но если вспомнить встроенный метод exec в питоне, возникает мысль дать пользователю
возможность писать на питоне. Проблема возникает одна, карты будут не безопасными!
Пользователю в таком режиме будет открыватся возможность подключать любые библиотеки и модули!
Он сможет по закрытию двери в игре, накрыть ваш ПК) 
Впрочем, есть ещё один вариант - Скриптовый Язык Сценариев! Да, питон сам по себе скриптовый язык...
Но нам нужен безопасный язык! Который будет позволять пользоваться только тем что предоставляет программа
А не то что вздумается пользователю.

'''

class Editor:

    def __init__(self):        

        self.zoom_amount = STT.RESIZE_SCALE #Число на которое будет умножатся канва в ту и другую сторону, в зависимости от того где она будет использоватся
        #По стандарту разрешение экрана зависит от размера экрана самого по себе что задаётся в настройках
        
        self.webx = None #Переменные сетки*
        self.weby = None
        
        self.selected_objects : list = [] #В список добавляются объекты что попали в область выделения(прямоугольника) инструмента выделения*
        
        self.object_list = [] #Список всех объектов ссылок или названий
        
        self.x1 = 0 #Переменные координат линий*
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
        
        self.scrollareaXYgame = 320 #Действительный размер канвы (записывается в файл проекта)*
        
        self.scrollareaXYeditor = 320 #Динамический размер канвы, нужен что бы увеличивать канву по мере приблежения
        
        self.line_count : int = 0

        self.step = 0
        
        self.root = GameWindow("MapEditor", 640, 480, 1)
        
        self.h = ttk.Scrollbar(self.root, orient="horizontal")
        self.v = ttk.Scrollbar(self.root, orient="vertical")
        
        self.canva = tk.Canvas(self.root, width=STT.canva_size[0], height=STT.canva_size[1], bg="#00000f", scrollregion=(0, 0, STT.canva_size[0], STT.canva_size[1]), yscrollcommand=self.v.set, xscrollcommand=self.h.set)
        
        self.pre_line = self.canva.create_line(self.x1, self.y1, self.x2, self.y2, fill="white", width=3, dash=2)
        
        self.tools_frame = tk.Frame(self.root, bg="#00000f")
        
        self.objects_frame = tk.Frame(self.root, bg="#00000f")
        
        self.object_list_var = tk.Variable(value=self.object_list)
        self.objects_listbox = tk.Listbox(self.objects_frame, listvariable=self.object_list_var)
        
        self.h["command"] = self.canva.xview
        self.v["command"] = self.canva.yview
        
        self.get_input = InputTool(self.canva)
        self.get_input.UPDATE()
        self.get_audio = AudioTool()
        
        self.root.option_add("*tearOff", False)
        
        self.main_menu = tk.Menu()
        self.file_menu = tk.Menu()
        self.settings_menu = tk.Menu()
        
        self.file_menu.add_command(label="Новый", command=self.create_new_map)
        self.file_menu.add_command(label="Открыть")
        self.file_menu.add_command(label="Сохранить")
        self.file_menu.add_command(label="Сохранить как...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Выход")
        
        self.main_menu.add_cascade(label="Файл", menu=self.file_menu)
        self.main_menu.add_cascade(label="Настройки", menu=self.settings_menu)
        self.main_menu.add_cascade(label="Автор", command=self.about_editor)
        
        self.settings_menu.add_cascade(label="Изменить шаг сетки", command=self.editor_settings_web_step)
        self.settings_menu.add_cascade(label="Изменить размер карты", command=self.editor_settings_map_size)
        
        self.mouse_pos = ttk.Label(master=self.canva)
        
        ##############################################################################################
        self.floor_types = [
        {"name": "Yfloor"},
        {"name": "Rfloor"},
        {"name": "Bfloor"}
        ]
        
        self.current_floor = self.floor_types[0]["name"]
        
        self.tool_list = [
        {"name": "Select", "img": tk.PhotoImage(file="Resources\Editor\Images\SelectG.png")},
        {"name": "Scale", "img": tk.PhotoImage(file="Resources\Editor\Images\ZoomG.png")}, 
        {"name": "Draw", "img": tk.PhotoImage(file="Resources\Editor\Images\DrawG.png")},
        {"name": "Move", "img": tk.PhotoImage(file="Resources\Editor\Images\PlusG.png")},
        {"name": "Entity", "img": tk.PhotoImage(file="Resources\Editor\Images\EntityG.png")},
        {"name": "Comment", "img": tk.PhotoImage(file="Resources\Editor\Images\CommentG.png")},
        {"name": "Delete", "img": tk.PhotoImage(file="Resources\Editor\Images\DeleteG.png")}
        ]

        self.current_tool = self.tool_list[0]["name"]    # по умолчанию будет выбран элемент с value=python
        ################################################################################################
        
        self.header = ttk.Label(master=self.tools_frame, textvariable=self.current_tool)
        self.header.pack(side="bottom", fill="x")
        
        tools_label = ttk.Label(self.tools_frame, text="Инструменты")
        objlist_label = ttk.Label(self.objects_frame, text="Объекты")
        
        #PACK's
        self.tools_frame.pack(fill="y", side="left")
        self.objects_frame.pack(fill="y", side="right")
        
        self.objects_listbox.pack(fill="y", expand=True)
        
        self.h.pack(side="bottom", fill="x")
        self.v.pack(side="right", fill="y")
        
        self.mouse_pos.pack()
        
        for t in self.tool_list:
            self.tool_btn = tk.Radiobutton(master=self.tools_frame, value=t["name"], text=t["name"], variable=self.current_tool, image=t["img"], compound="top", bg="#00000f", command=self.update_modes)
            self.tool_btn.pack( fill="y")
        
        self.root.config(menu=self.main_menu)

    def about_editor(self):
        showinfo("SB_ABOUT", "Редактор карт, часть большого проекта SnowBallEngine Pure Python")

    def create_new_map(self):
        self.create_win = tk.Tk()
        self.create_win.title("SB New Map")
        # self.create_win.geometry("240x480")
        self.create_win.resizable(0,0)
        
        name_label = ttk.Label(master=self.create_win,
                                text="Название новой карты",
                                font=("Arial", 16))
        
        size_label = ttk.Label(master=self.create_win, 
                                text="Задайте размер карты",
                                font=("Arial", 16))
        
        step_label = ttk.Label(master=self.create_win, 
                                text="Задайте размер сетки",
                                font=("Arial", 16))
        
        self.entry_name = ttk.Entry(master=self.create_win,
                                    font=("Arial", 16))
        
        self.entry_size = ttk.Entry(master=self.create_win,
                                    font=("Arial", 16))
        
        self.entry_step = ttk.Entry(master=self.create_win,
                                    font=("Arial", 16))
        
        # realsize_label = ttk.Label(master=self.create_win,
                                    # text="Реальный размер карты"+str(int(self.entry_size)))
        
        create_btn = ttk.Button(master=self.create_win,
                                text="Создать",
                                command=self.new_map_change)
        
        #PACK's
        name_label.pack(side="top")
        self.entry_name.pack(side="top", fill="x")
        size_label.pack(side="top")
        self.entry_size.pack(side="top", fill="x")
        step_label.pack(side="top")
        self.entry_step.pack(side="top", fill="x")
        
        create_btn.pack(side="bottom", fill="x")
        
    def editor_settings_map_size(self):
        self.create_win = tk.Tk()
        self.create_win.title("SB Map Size")
        # self.create_win.geometry("240x240")
        self.create_win.resizable(0,0)
        
        size_label = ttk.Label(master=self.create_win, 
                                text="Задайте размер карты",
                                font=("Arial", 16))
        
        self.entry_size = ttk.Entry(master=self.create_win,
                                    font=("Arial", 16))
        
        create_btn = ttk.Button(master=self.create_win,
                                text="Применить",
                                command=self.size_change)
        
        #PACK's
        size_label.pack(side="top")
        self.entry_size.pack(side="top", fill="x")
        
        create_btn.pack(side="bottom", fill="x")

    def editor_settings_web_step(self):
        self.create_win = tk.Tk()
        self.create_win.title("SB Web Step")
        # self.create_win.geometry("240x240")
        self.create_win.resizable(0,0)
        
        step_label = ttk.Label(master=self.create_win, 
                                text="Задайте размер сетки",
                                font=("Arial", 16))
                
        self.entry_step = ttk.Entry(master=self.create_win,
                                    font=("Arial", 16))
        
        create_btn = ttk.Button(master=self.create_win,
                                text="Применить",
                                command=self.step_change)
        
        #PACK's
        step_label.pack(side="top")
        self.entry_step.pack(side="top", fill="x")
        
        create_btn.pack(side="bottom", fill="x")

    def size_change(self):
        self.scrollareaXYgame = int(self.entry_size.get())
        
        old_scrollareaXYgame = int(self.scrollareaXY)
        
        try:
            self.create_win.destroy()
            self.canva.config(scrollregion=(0, 0, self.scrollareaXYgame, self.scrollareaXYgame))
            
        except tk.TclError:
            showerror(title="Ошибка", message="Пустое поле ввода, введено буквенное значение или не целое число, размер задаёться целыми числами!")
            self.create_win.destroy()
            
        except ValueError:
            showerror(title="Ошибка", message="Пустое поле ввода, введено буквенное значение или не целое число, размер задаёться целыми числами!")
            self.create_win.destroy()
    
    def step_change(self):
        self.step = int(self.entry_step.get())
        
        old_step = int(self.step)
        old_scrollareaXY = int(self.scrollareaXYgame)
        
        try:
            self.create_win.destroy()
            
            #Стираем старую сетку****
            for i in range(int(old_scrollareaXY)):
                self.canva.delete("webx"+str(i))
                self.canva.delete("weby"+str(i))
                
            # рисуем сетку
            for i in range(0, self.scrollareaXYgame, self.step):
                self.weby = self.canva.create_line(i, 0, i, self.scrollareaXYgame, fill="purple")
                self.webx = self.canva.create_line(0, i, self.scrollareaXYgame, i, fill="purple")
                self.canva.addtag_withtag("webx"+str(i), self.webx)
                self.canva.addtag_withtag("weby"+str(i), self.weby)
            
            for i in range(self.line_count):
                self.canva.lift("line"+str(i))
            
            #self.canva.lift(self.pre_line)
            
        except tk.TclError:
            showerror(title="Ошибка", message="Пустое поле ввода, введено буквенное значение или не целое число, размер задаёться целыми числами!")
            self.create_win.destroy()
            
        except ValueError:
            showerror(title="Ошибка", message="Пустое поле ввода, введено буквенное значение или не целое число, размер задаёться целыми числами!")
            self.create_win.destroy()
    
    def new_map_change(self):
        self.scrollareaXYgame = int(self.entry_size.get())
        self.step = int(self.entry_step.get())
        
        old_scrollareaXY = int(self.scrollareaXYgame)
        old_step = int(self.step)
        
        try:
            self.create_win.destroy()
            self.canva.config(scrollregion=(0, 0, self.scrollareaXYgame, self.scrollareaXYgame))
            
            #Стираем старую сетку****
            for i in range(int(old_scrollareaXY)):
                self.canva.delete("webx"+str(i))
                self.canva.delete("weby"+str(i))
                
            # рисуем сетку
            for i in range(0, self.scrollareaXYgame, self.step):
                self.weby = self.canva.create_line(i, 0, i, self.scrollareaXYgame, fill="purple")
                self.webx = self.canva.create_line(0, i, self.scrollareaXYgame, i, fill="purple")
                self.canva.addtag_withtag("webx"+str(i), self.webx)
                self.canva.addtag_withtag("weby"+str(i), self.weby)
            
            for i in range(self.line_count):
                self.canva.lift("line"+str(i))
            
            self.canva.lift(self.pre_line)
            
        except tk.TclError:
            showerror(title="Ошибка", message="Пустое поле ввода, введено буквенное значение или не целое число, размер задаёться целыми числами!")
            self.create_win.destroy()
            
        except ValueError:
            showerror(title="Ошибка", message="Пустое поле ввода, введено буквенное значение или не целое число, размер задаёться целыми числами!")
            self.create_win.destroy()

    def open_map_change(self):
        pass
    
    #Ивенты мыши
    
    #Обработчик передвижения мыши по холсту
    def update_motion(self, event):
    
        mouse_coords = [int(self.canva.canvasx(event.x)/self.zoom_amount), int(self.canva.canvasy(event.y)/self.zoom_amount)]
        
        self.mouse_pos.config(text=mouse_coords)
        
        match self.header.cget("text"):
            case "Select":
                self.canva.coords(self.pre_line, 0, 0, 0, 0)
            case "Draw":
                x = self.canva.canvasx(event.x)
                y = self.canva.canvasy(event.y)
                
                if self.line_count <= 0:
                    self.canva.coords(self.pre_line, 0, 0, 0, 0)
                elif self.line_count > 0:
                    self.canva.coords(self.pre_line, self.x1, self.y1, x, y)
            case "Entity":
                self.canva.coords(self.pre_line, 0, 0, 0, 0)
            case "Move":
                self.canva.coords(self.pre_line, 0, 0, 0, 0)
            case "Delete":
                self.canva.coords(self.pre_line, 0, 0, 0, 0)
            case "Comment":
                self.canva.coords(self.pre_line, 0, 0, 0, 0)

    #Обработчик события нажатия кнопки мыши на холсте
    def update_click(self, event):
        match self.header.cget("text"):
            case "Select":
                pass

            case "Scale":
                pass
            
            case "Draw":
                
                #Первая точка от которой будет рисоваться pre_line,
                #а так же все остальные линии
                #Будет рисоватся из координат мыши по нажатию*
                if self.line_count == 0:
                    self.x1 = self.canva.canvasx(event.x)
                    self.y1 = self.canva.canvasy(event.y)
                
                    self.x1 = int(round(self.x1 / self.step) * self.step)
                    self.y1 = int(round(self.y1 / self.step) * self.step)
                
                # получаем координаты клика мыши
                self.x2 = self.canva.canvasx(event.x)
                self.y2 = self.canva.canvasy(event.y)
                # округляем координаты до ближайшего кратного значения шага сетки
                self.x2 = int(round(self.x2 / self.step) * self.step)
                self.y2 = int(round(self.y2 / self.step) * self.step)
                # рисуем новую линию на холсте и присваиваем ей тег "auto"
                tag = "line{}".format(self.line_count)
                self.canva.create_line(self.x1, self.y1, self.x2, self.y2, fill="white", tags=tag)
                # увеличиваем счетчик линий на 1
                self.line_count += 1
                # сохраняем координаты конечной точки для следующей линии
                self.x1 = self.x2
                self.y1 = self.y2
                
            case "Entity":
                pass
                
            case "Move":
                pass
                
            case "Delete":
                pass
    
    #Обработчик удерживания кнопки мыши и передвижения по холсту*
    def update_B1_drag(self, event):
        print("DRAGING_STUFF")
    
    #Обработчик события прокрутки колёсика мыши
    def update_scroll(self, event):
        pass
    
    #обработчик смены режима* Переключает стили и в общем показывает что, что то произошло
    def update_modes(self):
        match self.header.cget("text"):
            case "Select":
                self.root.config(cursor="arrow")
            case "Scale":
                self.root.config(cursor="pencil")
            case "Draw":
                self.root.config(cursor="pencil")
            case "Entity":
                self.root.config(cursor="based_arrow_down")
            case "Move":
                self.root.config(cursor="cross_reverse")
            case "Comment":
                self.root.config(cursor="xterm")
            case "Delete":
                self.root.config(cursor="X_cursor")
    
    #обработчик нажатия кнопки Enter*
    def update_key_Enter(self, event):
        match self.header.cget("text"):
            case "Select":
                pass
            case "Scale":
                pass
            case "Draw":
                print("ENTER")
                self.line_count = 0
            case "Entity":
                pass
            case "Move":
                pass
            case "Comment":
                pass
            case "Delete":
                pass
    
    def update_key_Escape(self, event):
        match self.header.cget("text"):
            case "Select":
                pass
            case "Scale":
                pass
            case "Draw":
                print("Escape")
                
            case "Entity":
                pass
            case "Move":
                pass
            case "Comment":
                pass
            case "Delete":
                pass
    
    #Обработчик всеобщего обновления всех процессов*
    def UPDATE(self):
        self.canva.bind("<Return>", self.update_key_Enter)
        self.canva.bind("<Escape>", self.update_key_Escape)
        self.canva.bind("<Motion>", self.update_motion)
        self.canva.bind("<Button-1>", self.update_click)
        # self.canva.bind("<B2-Motion>", self.update_B2_drag)
        self.canva.bind("<B1-Motion>", self.update_B1_drag)
        
        self.root.game_mainloop(self.canva)
        
editor = Editor()

editor.UPDATE()
