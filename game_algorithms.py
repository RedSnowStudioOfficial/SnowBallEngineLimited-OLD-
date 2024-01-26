from SBTK_CORE import *
from game_objects import *
import Settings as STT
import math

#Game help

class Game_Tool:
    
    def __init__(self, canva) -> None:
        
        self.canva = canva

    def get_sign(self, x):
        if x >= 0: 
            return 1
        else:
            return -1

    def get_coords(self, obj):
        return self.canva.coords(obj)
    
    def get_tag(self, obj):
        return self.canva.gettags(obj)
    
    def get_overlap(self, obj):
        '''
        Возвращает пересечения и объект проверок
        '''
        x1, y1, x2, y2 = self.canva.coords(obj)
    
        return self.canva.find_overlapping(x1, y1, x2, y2)

    def get_cross(self, obj1, obj2): #Получение точки пересечения (ТОЛЬКО ДЛЯ ЛИНИЙ!)
        
        x1, y1, x2, y2 = self.get_coords(obj1)
        x3, y3, x4, y4 = self.get_coords(obj2)

        den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if den == 0:
            return None  # отрезки параллельны

        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

        if 0 <= ua <= 1 and 0 <= ub <= 1:
            # точка пересечения лежит на отрезках AB и CD
            x = x1 + ua * (x2 - x1)
            y = y1 + ua * (y2 - y1)
            return x, y
        else:
            return None  # отрезки не пересекаются

    def get_distance(self, origin, point_cross):
        if point_cross != None:
            x1, y1, x2, y2 = self.get_coords(origin)
            x3, y3 = point_cross

            return (x1 - x3)-(y1 - y3)
        else:
            return None

    def get_angle(self, obj):
        #Получаем координаты объекта
        x1, y1, x2, y2 = self.canva.coords(obj)

        #Преобразуем отрезок в вектор направления
        dx = x2 - x1
        dy = y2 - y1

        #Узнаём угол вектора направления отнросительно того что направлен вперёд горизонтально
        v1 = [0, 1]
        v2 = [dy, dx]

        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])

        r = (v2_theta - v1_theta) * (180.0 / math.pi)

        if r < 0:
            r += 360.0

        return r

    def get_angle_spd(self, xspd, yspd):
        
        x1, y1, x2, y2 = 0, 0, xspd, yspd
        
        #Преобразуем отрезок в вектор направления
        dx = x2 - x1
        dy = y2 - y1

        #Узнаём угол вектора направления отнросительно того что направлен вперёд горизонтально
        v1 = [0, 1]
        v2 = [dy, dx]

        v1_theta = math.atan2(v1[1], v1[0])
        v2_theta = math.atan2(v2[1], v2[0])

        r = (v2_theta - v1_theta) * (180.0 / math.pi)

        if r < 0:
            r += 360.0

        return r
    
    def rgb_to_alpha(self, image, r, g, b):
        image.convert('RGBA') # конвертируем в формат с альфа-каналом
        data = image.getdata() # получаем пиксели
        new_data = [] # создаем новый список пикселей
        for item in data:
            if item[:3] == (r, g, b): # если цвет такой то, такой то, ТО
                new_data.append((255, 255, 255, 0)) # заменяем на прозрачность
            else:
                new_data.append(item) # оставляем без изменения
            image.putdata(new_data) # устанавливаем новые пиксели
            image.save('new_image.png') # сохраняем результат
        
        