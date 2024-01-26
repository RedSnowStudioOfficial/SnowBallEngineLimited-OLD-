import os

from SBTK_CORE import *
from game_algorithms import *
import Settings as STT
import Conteiners.spisok as SP #Двойной список
import tkinter as tk
import characters_stats as cs
import math

class Sonic:

    def __init__(self, x_pos, y_pos, sprite, canva, input_tool, game_tool) -> None:

        '''
        Скрипт игрока
        '''
        
        self.canva = canva

        self.sprite = sprite
        
        self.sprite.set_transperent_color_rgb((255, 0, 255))
        
        self.sprite.scale(STT.RESIZE_SCALE)
        
        self.game_tool = game_tool
        
        #Слой игрового мира на котором сейчас находиться игрок*
        self.player_layer = "Bfloor"
        
        #Центр и первоначальная позиция игрока, статичная
        self.pos = [x_pos, y_pos]

        #Подключение беблиотеки для обработки ввода игрока
        self.get_input = input_tool
        
        #Вектор направления ввода игрока*
        self.input_dir : list = [0, 0]
        
        #Переменные параметров скорости
        self.X_SPD : float = 0
        self.Y_SPD : float = 0
        
        self.GROUND_SPD : float = 0
        
        #Состояние игрока* 
        self.player_state : str = "AIR"
        
        #Объект игрока собранный воедино, что бы передвигать все его состовляющие.
        #Список пополниться после отриовки игрока
        self.get_object : list = []

        #Динамичный центр объекта*
        self.ORIGIN : object = None
        
        #Очертания объекта, для обработки получения урона и прочего*
        self.HITBOX : object = None
        
        #Сенсоры Потолка
        self.LEFT_CILING_SENSOR : object = None
        self.RIGHT_CILING_SENSOR : object = None
        
        #Сенсоры Пола
        self.LEFT_FLOOR_SENSOR : object = None
        self.RIGHT_FLOOR_SENSOR : object = None
        
        self.BALANCE_CHECK_SENSOR : object = None
        
        #Сенсоры Стен
        self.LEFT_WALL_SENSOR : object = None
        self.RIGHT_WALL_SENSOR : object = None
        
        self.player_mode = None
        
        self.is_rolling : bool = False
        self.is_jumped : bool = False
        self.is_balancing : bool = False
        self.is_crouching : bool = False
        self.is_looking_up : bool = False
        
    def input_update(self):

        #Обработка нажатых клавиш
        if self.get_input.key == "Left" and self.get_input.PRESSED:
            self.input_dir[0] = -1
        if self.get_input.key == "Right" and self.get_input.PRESSED:
            self.input_dir[0] = 1
        if self.get_input.key == "Up" and self.get_input.PRESSED:
            self.input_dir[1] = -1
        if self.get_input.key == "Down" and self.get_input.PRESSED:
            self.input_dir[1] = 1
        if self.get_input.key == "a" and self.get_input.PRESSED:
            self.jump_hold = True

        #Обработка отпущенных клавиш
        if self.get_input.key == "Left" and self.get_input.RELEASED:
            self.input_dir[0] = 0
        if self.get_input.key == "Right" and self.get_input.RELEASED:
            self.input_dir[0] = 0
        if self.get_input.key == "Up" and self.get_input.RELEASED:
            self.input_dir[1] = 0
        if self.get_input.key == "Down" and self.get_input.RELEASED:
            self.input_dir[1] = 0
        if self.get_input.key == "a" and self.get_input.RELEASED:
            self.jump_hold = False

    def draw_in(self):
        
        self.player_mode = "floor"
        
        match STT.DEBUG:
            
            case 0:
                
                #ORIGIN
                self.ORIGIN = self.canva.create_oval(self.pos[0], self.pos[1],
                                                    self.pos[0], self.pos[1],
                                                    fill="")
                
                #HITBOX
                self.HITBOX = self.canva.create_rectangle(self.pos[0]-cs.WIDTHradius[0], self.pos[1]-cs.HEIGHTradius[0],
                                                        self.pos[0]+cs.WIDTHradius[0], self.pos[1]+cs.HEIGHTradius[0],
                                                        fill="")
                
                #WALL Sensors
                self.LEFT_WALL_SENSOR = self.canva.create_line(self.pos[0], self.pos[1],
                                                            self.pos[0]-cs.push_radius, self.pos[1],
                                                            fill="")

                self.RIGHT_WALL_SENSOR = self.canva.create_line(self.pos[0], self.pos[1],
                                                            self.pos[0]+cs.push_radius, self.pos[1],
                                                            fill="")

                #FLOOR Sensors
                self.LEFT_FLOOR_SENSOR = self.canva.create_line(self.pos[0]-cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]-cs.WIDTHradius[0], self.pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize, 
                                                            fill="")
                                                            
                self.RIGHT_FLOOR_SENSOR = self.canva.create_line(self.pos[0]+cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]+cs.WIDTHradius[0], self.pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize, 
                                                            fill="")
                
                self.BALANCE_CHECK_SENSOR = self.canva.create_line(self.pos[0], self.pos[1],
                                                                    self.pos[0], self.pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize,
                                                                    fill="")
                
                #CILING Sensor
                self.LEFT_CILING_SENSOR = self.canva.create_line(self.pos[0]-cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]-cs.WIDTHradius[0], self.pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize, 
                                                            fill="")

                self.RIGHT_CILING_SENSOR = self.canva.create_line(self.pos[0]+cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]+cs.WIDTHradius[0], self.pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize, 
                                                            fill="")
        
        
            case 1:
                
                #ORIGIN
                self.ORIGIN = self.canva.create_oval(self.pos[0], self.pos[1],
                                                    self.pos[0], self.pos[1],
                                                    fill="")
                
                #HITBOX
                self.HITBOX = self.canva.create_rectangle(self.pos[0]-cs.WIDTHradius[0], self.pos[1]-cs.HEIGHTradius[0],
                                                        self.pos[0]+cs.WIDTHradius[0], self.pos[1]+cs.HEIGHTradius[0],
                                                        fill="#ad2d9a")
                
                #WALL Sensors
                self.LEFT_WALL_SENSOR = self.canva.create_line(self.pos[0], self.pos[1],
                                                            self.pos[0]-cs.push_radius, self.pos[1],
                                                            fill="green")

                self.RIGHT_WALL_SENSOR = self.canva.create_line(self.pos[0], self.pos[1],
                                                            self.pos[0]+cs.push_radius, self.pos[1],
                                                            fill="green")

                #FLOOR Sensors
                self.LEFT_FLOOR_SENSOR = self.canva.create_line(self.pos[0]-cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]-cs.WIDTHradius[0], self.pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize, 
                                                            fill="red")
                                                            
                self.RIGHT_FLOOR_SENSOR = self.canva.create_line(self.pos[0]+cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]+cs.WIDTHradius[0], self.pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize, 
                                                            fill="blue")
                
                self.BALANCE_CHECK_SENSOR = self.canva.create_line(self.pos[0], self.pos[1],
                                                                    self.pos[0], self.pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize,
                                                                    fill="purple")
                
                #CILING Sensor
                self.LEFT_CILING_SENSOR = self.canva.create_line(self.pos[0]-cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]-cs.WIDTHradius[0], self.pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize, 
                                                            fill="orange")

                self.RIGHT_CILING_SENSOR = self.canva.create_line(self.pos[0]+cs.WIDTHradius[0], self.pos[1],
                                                            self.pos[0]+cs.WIDTHradius[0], self.pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize, 
                                                            fill="yellow")


        self.sprite.draw_in(self.pos[0], self.pos[1]+3)
        
        self.canva.addtag_withtag("hitbox", self.HITBOX)
            
        self.canva.addtag_withtag("origin", self.ORIGIN)

        self.canva.addtag_withtag("left_wall_sensor", self.LEFT_WALL_SENSOR)
        self.canva.addtag_withtag("right_wall_sensor", self.RIGHT_WALL_SENSOR)

        self.canva.addtag_withtag("left_floor_sensor", self.LEFT_FLOOR_SENSOR)
        self.canva.addtag_withtag("right_floor_sensor", self.RIGHT_FLOOR_SENSOR)

        self.canva.addtag_withtag("balance_check_sensor", self.BALANCE_CHECK_SENSOR)

        self.canva.addtag_withtag("left_ciling_sensor", self.LEFT_CILING_SENSOR)
        self.canva.addtag_withtag("right_ciling_sensor", self.RIGHT_CILING_SENSOR)
        
        self.canva.addtag_withtag("sprite", self.sprite.sprite_obj)

        self.get_floor_sensors = [self.LEFT_FLOOR_SENSOR, self.RIGHT_FLOOR_SENSOR]

        

        self.get_object = [self.ORIGIN, self.HITBOX,
                            self.LEFT_WALL_SENSOR, self.RIGHT_WALL_SENSOR, 
                            self.LEFT_FLOOR_SENSOR, self.RIGHT_FLOOR_SENSOR,
                            self.BALANCE_CHECK_SENSOR,
                            self.LEFT_CILING_SENSOR, self.RIGHT_CILING_SENSOR,
                            self.sprite.sprite_obj]

    def clear_out(self):
        for i in self.get_object:
            self.canva.delete(i)
    
    #Информация с датчиков
    def get_wall_info(self):
        
        left_wall_overlap = None
        right_wall_overlap = None
        
        left_wall_distance = None
        left_wall_tagid = None

        right_wall_distance = None
        right_wall_tagid = None

        left_wall_overlap = self.game_tool.get_overlap(self.LEFT_WALL_SENSOR)
        right_wall_overlap = self.game_tool.get_overlap(self.RIGHT_WALL_SENSOR)
        

        for index, links in enumerate(left_wall_overlap):
                    if self.game_tool.get_tag(links)[0] == self.player_layer or self.game_tool.get_tag(links)[0] == "Yfloor":
                        point_cross = self.game_tool.get_cross(self.LEFT_WALL_SENSOR, left_wall_overlap[index])
                            
                        if point_cross != None:
                            
                            left_wall_tagid = left_wall_overlap[index]
                            left_wall_distance = float(self.game_tool.get_distance(self.LEFT_WALL_SENSOR, point_cross)-cs.WIDTHradius[0]+self.GROUND_SPD)
            
        for index, links in enumerate(right_wall_overlap):
                    if self.game_tool.get_tag(links)[0] == self.player_layer or self.game_tool.get_tag(links)[0] == "Yfloor":
                        point_cross = self.game_tool.get_cross(self.RIGHT_WALL_SENSOR, right_wall_overlap[index])
                            
                        if point_cross != None:
                            
                            right_wall_tagid = right_wall_overlap[index]
                            right_wall_distance = float(self.game_tool.get_distance(self.RIGHT_WALL_SENSOR, point_cross)+cs.WIDTHradius[0]+self.GROUND_SPD)
                
        if left_wall_distance != None and right_wall_distance == None:
                    return left_wall_tagid, left_wall_distance, "l_wall"
                
        elif left_wall_distance == None and right_wall_distance != None:
                    return right_wall_tagid, right_wall_distance, "r_wall"
                
    def get_ciling_info(self):
        
        left_overlap = None
        right_overlap = None

        left_distance = None
        right_distance = None
            
        left_angle = None
        right_angle = None
            
        left_tagid = None
        right_tagid = None
        
        left_overlap = self.game_tool.get_overlap(self.LEFT_CILING_SENSOR)
        right_overlap = self.game_tool.get_overlap(self.RIGHT_CILING_SENSOR)
            
        for index, links in enumerate(left_overlap):
                if self.game_tool.get_tag(links)[0] == self.player_layer or self.game_tool.get_tag(links)[0] == "Yfloor":
                    point_cross = self.game_tool.get_cross(self.LEFT_CILING_SENSOR, left_overlap[index])
                    
                    if point_cross != None:
                    
                        left_tagid = left_overlap[index]
                        left_distance = int(self.game_tool.get_distance(self.LEFT_CILING_SENSOR, point_cross) + cs.sensor_resize) * -1
                        left_angle = int(self.game_tool.get_angle(left_overlap[index]))
                        
        for index, links in enumerate(right_overlap):
                if self.game_tool.get_tag(links)[0] == self.player_layer or self.game_tool.get_tag(links)[0] == "Yfloor":
                    point_cross = self.game_tool.get_cross(self.RIGHT_CILING_SENSOR, right_overlap[index])
                    
                    if point_cross != None:
                    
                        right_tagid = right_overlap[index]
                        right_distance = int(self.game_tool.get_distance(self.RIGHT_CILING_SENSOR, point_cross) + cs.sensor_resize) * -1
                        right_angle = int(self.game_tool.get_angle(right_overlap[index]))
        
        if left_distance != None and right_distance == None:
                    return left_tagid, left_distance, left_angle #, "l_floor"
                
        elif left_distance == None and right_distance != None:
                    return right_tagid, right_distance, right_angle #, "r_floor"
        
        elif left_distance != None and right_distance != None:
                if left_distance <= right_distance:
                    return left_tagid, left_distance, left_angle #, "l_floor"
                elif left_distance >= right_distance:
                    return right_tagid, right_distance, right_angle #, "r_floor"

    def get_floor_info(self):
        
        left_overlap = None
        right_overlap = None

        left_distance = None
        right_distance = None
            
        left_angle = None
        right_angle = None
            
        left_tagid = None
        right_tagid = None
        
        left_overlap = self.game_tool.get_overlap(self.LEFT_FLOOR_SENSOR)
        right_overlap = self.game_tool.get_overlap(self.RIGHT_FLOOR_SENSOR)
            
        for index, links in enumerate(left_overlap):
                if self.game_tool.get_tag(links)[0] == self.player_layer or self.game_tool.get_tag(links)[0] == "Yfloor":
                    point_cross = self.game_tool.get_cross(self.LEFT_FLOOR_SENSOR, left_overlap[index])
                    
                    if point_cross != None:
                    
                        left_tagid = left_overlap[index]
                        left_distance = int(self.game_tool.get_distance(self.LEFT_FLOOR_SENSOR, point_cross) - cs.sensor_resize)
                        left_angle = int(self.game_tool.get_angle(left_overlap[index]))
                        
        for index, links in enumerate(right_overlap):
                if self.game_tool.get_tag(links)[0] == self.player_layer or self.game_tool.get_tag(links)[0] == "Yfloor":
                    point_cross = self.game_tool.get_cross(self.RIGHT_FLOOR_SENSOR, right_overlap[index])
                    
                    if point_cross != None:
                    
                        right_tagid = right_overlap[index]
                        right_distance = int(self.game_tool.get_distance(self.RIGHT_FLOOR_SENSOR, point_cross) - cs.sensor_resize)
                        right_angle = int(self.game_tool.get_angle(right_overlap[index]))
        
        if left_distance != None and right_distance == None:
                    return left_tagid, left_distance, left_angle #, "l_floor"
                
        elif left_distance == None and right_distance != None:
                    return right_tagid, right_distance, right_angle #, "r_floor"
        
        if self.player_mode == "l_wall" or self.player_mode == "floor":
            if left_distance != None and right_distance != None:
                if left_distance <= right_distance:
                    return left_tagid, left_distance, left_angle #, "l_floor"
                elif left_distance >= right_distance:
                    return right_tagid, right_distance, right_angle #, "r_floor"
        
        elif self.player_mode == "r_wall" or self.player_mode == "ciling":
            if left_distance != None and right_distance != None:
                if left_distance >= right_distance:
                    return left_tagid, left_distance, left_angle #, "l_floor"
                elif left_distance <= right_distance:
                    return right_tagid, right_distance, right_angle #, "r_floor"

    def is_on_floor(self):
        if self.get_floor_info() == None:
                return False
        else:
            if self.get_floor_info()[1] <= 0:
                return True
    
    # def is_grounded(self):
        # if self.get_floor_info() == None:
            # return False
        # else:
            # if self.get_floor_info()[1] < -14:
                # return False
            # elif self.get_floor_info()[1] >= -14 and self.get_floor_info()[1] <= 0:
                # return True
            # elif self.get_floor_info()[1] > 14:
                # return False
            # elif self.get_floor_info()[1] <= 14 and self.get_floor_info()[1] >= 0:
                # return True
    
    def can_jump(self):
        if self.get_ciling_info() == None and self.is_jumped == False:
            return True
        else:
            if self.get_ciling_info()[1] < 6 or self.is_jumped == True:
                return False
                
    #Получение режима игрока из угла земли
    def update_player_mode(self):
        
        if self.get_floor_info() != None:
            
            if self.get_floor_info()[2] >= 226 and self.get_floor_info()[2] <= 314:
                
                ###RIGHT_WALL###

                self.player_mode = "l_wall"
                
            elif self.get_floor_info()[2] >= 135 and self.get_floor_info()[2] <= 225:
                
                ###CILING###
                
                self.player_mode = "ciling"
                   
            elif self.get_floor_info()[2] >= 46 and self.get_floor_info()[2] <= 134:
                
                ###LEFT_WALL###
                
                self.player_mode = "r_wall"
            
            elif self.get_floor_info()[2] >= 0 and self.get_floor_info()[2] <= 45 or self.get_floor_info()[2] >= 315 and self.get_floor_info()[2] <= 360:
    
                ###FLOOR###

                self.player_mode = "floor"
                
            elif self.is_on_floor() == False:
                
                self.player_mode = "air"

        else:
            return None
    
    #Режимы пола игрока
    def r_wall_mode(self):
    
                pos = self.game_tool.get_coords(self.ORIGIN)
    
                if self.is_rolling == False:
                
                    cs.sensor_resize = cs.sensor_resize_r_c
                    
                    self.canva.coords(self.HITBOX, pos[0]-cs.HEIGHTradius[0], pos[1]-cs.WIDTHradius[0],
                                                    pos[0]+cs.HEIGHTradius[0], pos[1]+cs.WIDTHradius[0])

                    self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]+cs.push_radius)

                    self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]-cs.push_radius)
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0], pos[1]+cs.WIDTHradius[0],
                                                                pos[0]+cs.HEIGHTradius[0] - cs.sensor_resize, pos[1]+cs.WIDTHradius[0])
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0], pos[1]-cs.WIDTHradius[0],
                                                                pos[0]+cs.HEIGHTradius[0] - cs.sensor_resize, pos[1]-cs.WIDTHradius[0])
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0], pos[1]+cs.WIDTHradius[0],
                                                                pos[0]-cs.HEIGHTradius[0] + cs.sensor_resize, pos[1]+cs.WIDTHradius[0])
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0], pos[1]-cs.WIDTHradius[0],
                                                                pos[0]-cs.HEIGHTradius[0] + cs.sensor_resize, pos[1]-cs.WIDTHradius[0])
                
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])
                
                else:
                    
                    cs.sensor_resize = cs.sensor_resize_r_c_roll
                    
                    self.canva.coords(self.HITBOX, pos[0]-cs.HEIGHTradius[1], pos[1]-cs.WIDTHradius[1],
                                                    pos[0]+cs.HEIGHTradius[1], pos[1]+cs.WIDTHradius[1])

                    self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]+cs.push_radius)

                    self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]-cs.push_radius)
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0], pos[1]+cs.WIDTHradius[1],
                                                                pos[0]+cs.HEIGHTradius[1] - cs.sensor_resize, pos[1]+cs.WIDTHradius[1])
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0], pos[1]-cs.WIDTHradius[1],
                                                                pos[0]+cs.HEIGHTradius[1] - cs.sensor_resize, pos[1]-cs.WIDTHradius[1])
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0], pos[1]+cs.WIDTHradius[1],
                                                                pos[0]-cs.HEIGHTradius[1] + cs.sensor_resize, pos[1]+cs.WIDTHradius[1])
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0], pos[1]-cs.WIDTHradius[1],
                                                                pos[0]-cs.HEIGHTradius[1] + cs.sensor_resize, pos[1]-cs.WIDTHradius[1])
    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])

    def l_wall_mode(self):
    
                pos = self.game_tool.get_coords(self.ORIGIN)
        
                if self.is_rolling == False:
                
                    cs.sensor_resize = cs.sensor_resize_l_f

                    self.canva.coords(self.HITBOX, pos[0]+cs.HEIGHTradius[0], pos[1]+cs.WIDTHradius[0],
                                                    pos[0]-cs.HEIGHTradius[0], pos[1]-cs.WIDTHradius[0])

                    self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]-cs.push_radius)

                    self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]+cs.push_radius)
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0], pos[1]-cs.WIDTHradius[0],
                                                                pos[0]-cs.HEIGHTradius[0] - cs.sensor_resize, pos[1]-cs.WIDTHradius[0])
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0], pos[1]+cs.WIDTHradius[0],
                                                                pos[0]-cs.HEIGHTradius[0] - cs.sensor_resize, pos[1]+cs.WIDTHradius[0])
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0], pos[1]-cs.WIDTHradius[0],
                                                                pos[0]+cs.HEIGHTradius[0] + cs.sensor_resize, pos[1]-cs.WIDTHradius[0])
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0], pos[1]+cs.WIDTHradius[0],
                                                                pos[0]+cs.HEIGHTradius[0] + cs.sensor_resize, pos[1]+cs.WIDTHradius[0])
                
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])
                                                                
                else:
                    
                    cs.sensor_resize = cs.sensor_resize_l_f_roll
                    
                    self.canva.coords(self.HITBOX, pos[0]+cs.HEIGHTradius[1], pos[1]+cs.WIDTHradius[1],
                                                    pos[0]-cs.HEIGHTradius[1], pos[1]-cs.WIDTHradius[1])

                    self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]-cs.push_radius)

                    self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0], pos[1]+cs.push_radius)
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0], pos[1]-cs.WIDTHradius[1],
                                                                pos[0]-cs.HEIGHTradius[1] - cs.sensor_resize, pos[1]-cs.WIDTHradius[1])
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0], pos[1]+cs.WIDTHradius[1],
                                                                pos[0]-cs.HEIGHTradius[1] - cs.sensor_resize, pos[1]+cs.WIDTHradius[1])
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0], pos[1]-cs.WIDTHradius[1],
                                                                pos[0]+cs.HEIGHTradius[1] + cs.sensor_resize, pos[1]-cs.WIDTHradius[1])
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0], pos[1]+cs.WIDTHradius[1],
                                                                pos[0]+cs.HEIGHTradius[1] + cs.sensor_resize, pos[1]+cs.WIDTHradius[1])
                    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])

    def floor_mode(self):
                
                pos = self.game_tool.get_coords(self.ORIGIN)
                
                if self.is_rolling == False:
                
                    cs.sensor_resize = cs.sensor_resize_l_f
                
                    self.canva.coords(self.HITBOX, pos[0]-cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0],
                                                    pos[0]+cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0])
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0]-cs.WIDTHradius[0], pos[1],
                                                                pos[0]-cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0]+cs.WIDTHradius[0], pos[1],
                                                                pos[0]+cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize)
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0]-cs.WIDTHradius[0], pos[1],
                                                                pos[0]-cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0]+cs.WIDTHradius[0], pos[1],
                                                                pos[0]+cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize)
                    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1]+cs.HEIGHTradius[0]+cs.sensor_resize)
                    
                else:
                
                    cs.sensor_resize = cs.sensor_resize_l_f_roll
                   
                    self.canva.coords(self.HITBOX, pos[0]-cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1],
                                                    pos[0]+cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1])
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0]-cs.WIDTHradius[1], pos[1],
                                                                pos[0]-cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1] + cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0]+cs.WIDTHradius[1], pos[1],
                                                                pos[0]+cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1] + cs.sensor_resize)
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0]-cs.WIDTHradius[1], pos[1],
                                                                pos[0]-cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1] - cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0]+cs.WIDTHradius[1], pos[1],
                                                                pos[0]+cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1] - cs.sensor_resize)

    def ciling_mode(self):
                
                pos = self.game_tool.get_coords(self.ORIGIN)
                
                if self.is_rolling == False:
                
                    cs.sensor_resize = cs.sensor_resize_r_c
                    
                    self.canva.coords(self.HITBOX, pos[0]-cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0],
                                                    pos[0]+cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0])

                    self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0]+cs.push_radius, pos[1])

                    self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0]-cs.push_radius, pos[1])
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0]+cs.WIDTHradius[0], pos[1],
                                                                pos[0]+cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0] + cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0]-cs.WIDTHradius[0], pos[1],
                                                                pos[0]-cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0] + cs.sensor_resize)
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0]+cs.WIDTHradius[0], pos[1],
                                                                pos[0]+cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0] - cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0]-cs.WIDTHradius[0], pos[1],
                                                                pos[0]-cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0] - cs.sensor_resize)
                    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])
                
                else:
                    
                    cs.sensor_resize = cs.sensor_resize_r_c_roll
                    
                    self.canva.coords(self.HITBOX, pos[0]-cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1],
                                                    pos[0]+cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1])

                    self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0]+cs.push_radius, pos[1])

                    self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                            pos[0]-cs.push_radius, pos[1])
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0]+cs.WIDTHradius[1], pos[1],
                                                                pos[0]+cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1] + cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0]-cs.WIDTHradius[1], pos[1],
                                                                pos[0]-cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1] + cs.sensor_resize)
                    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1]-cs.HEIGHTradius[1] - cs.sensor_resize)
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0]+cs.WIDTHradius[1], pos[1],
                                                                pos[0]+cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1] - cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0]-cs.WIDTHradius[1], pos[1],
                                                                pos[0]-cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1] - cs.sensor_resize)
                    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])

    def air_mode(self):
        
        pos = self.game_tool.get_coords(self.ORIGIN)
                
        if self.is_rolling == False:
                
                    cs.sensor_resize = cs.sensor_resize_l_f
                
                    self.canva.coords(self.HITBOX, pos[0]-cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0],
                                                    pos[0]+cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0])
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0]-cs.WIDTHradius[0], pos[1],
                                                                pos[0]-cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0]+cs.WIDTHradius[0], pos[1],
                                                                pos[0]+cs.WIDTHradius[0], pos[1]+cs.HEIGHTradius[0] + cs.sensor_resize)
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0]-cs.WIDTHradius[0], pos[1],
                                                                pos[0]-cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0]+cs.WIDTHradius[0], pos[1],
                                                                pos[0]+cs.WIDTHradius[0], pos[1]-cs.HEIGHTradius[0] - cs.sensor_resize)
                    
                    self.canva.coords(self.BALANCE_CHECK_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1]+cs.HEIGHTradius[0]+cs.sensor_resize)
                    
        else:
                
                    cs.sensor_resize = cs.sensor_resize_l_f_roll
                   
                    self.canva.coords(self.HITBOX, pos[0]-cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1],
                                                    pos[0]+cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1])
                    
                    self.canva.coords(self.LEFT_FLOOR_SENSOR, pos[0]-cs.WIDTHradius[1], pos[1],
                                                                pos[0]-cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1] + cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_FLOOR_SENSOR, pos[0]+cs.WIDTHradius[1], pos[1],
                                                                pos[0]+cs.WIDTHradius[1], pos[1]+cs.HEIGHTradius[1] + cs.sensor_resize)
                    
                    self.canva.coords(self.LEFT_CILING_SENSOR, pos[0]-cs.WIDTHradius[1], pos[1],
                                                                pos[0]-cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1] - cs.sensor_resize)
                    
                    self.canva.coords(self.RIGHT_CILING_SENSOR, pos[0]+cs.WIDTHradius[1], pos[1],
                                                                pos[0]+cs.WIDTHradius[1], pos[1]-cs.HEIGHTradius[1] - cs.sensor_resize)

    def handle_floor(self):
        #Обновление режима игрока
        
        match self.player_mode:
            case "l_wall":
                self.l_wall_mode()
            case "r_wall":
                self.r_wall_mode()
            case "ciling":
                self.ciling_mode()
            case "floor":
                self.floor_mode()

    def handle_wall(self):
    
        pos = self.game_tool.get_coords(self.ORIGIN)
                
        if self.get_floor_info() != None:
            
            if self.get_floor_info()[2] == 0:
                if self.X_SPD > 0:
                            self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1]+cs.wall_offcet,
                                                                pos[0], pos[1]+cs.wall_offcet)

                            self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1]+cs.wall_offcet,
                                                                pos[0]+cs.push_radius+self.X_SPD, pos[1]+cs.wall_offcet)
                        
                elif self.X_SPD < 0:
                            self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1]+cs.wall_offcet,
                                                                pos[0]-cs.push_radius+self.X_SPD, pos[1]+cs.wall_offcet)

                            self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1]+cs.wall_offcet,
                                                                pos[0], pos[1]+cs.wall_offcet)

                elif self.X_SPD == 0:
                            self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1]+cs.wall_offcet,
                                                                pos[0], pos[1]+cs.wall_offcet)

                            self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1]+cs.wall_offcet,
                                                                pos[0], pos[1]+cs.wall_offcet)

            else:
                if self.X_SPD > 0:

                            self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])

                            self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                                pos[0]+cs.push_radius+self.X_SPD, pos[1])
                elif self.X_SPD < 0:
                            self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                                pos[0]-cs.push_radius+self.X_SPD, pos[1])

                            self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])
                                                                
                elif self.X_SPD == 0:
                            self.canva.coords(self.LEFT_WALL_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])

                            self.canva.coords(self.RIGHT_WALL_SENSOR, pos[0], pos[1],
                                                                pos[0], pos[1])
    
        if self.get_wall_info() != None:
            if self.get_wall_info()[2] == "l_wall":
                if self.GROUND_SPD <= 0:
                    if self.get_wall_info()[1] < 0:
                                    self.GROUND_SPD = 0
                                    self.X_SPD = -self.get_wall_info()[1]
                            
            elif self.get_wall_info()[2] == "r_wall":
                if self.GROUND_SPD >= 0:
                    if self.get_wall_info()[1] > 0:
                                    self.GROUND_SPD = 0
                                    self.X_SPD = -self.get_wall_info()[1]
    
    def handle_airborn(self):
        self.air_mode()
    
        air_dir = self.game_tool.get_angle_spd(self.X_SPD, self.Y_SPD)
        
        if air_dir <= 45 and air_dir >= 0 or air_dir <= 360 and air_dir >= 316:
            return "RIGHT"
        elif air_dir <= 135 and air_dir >= 46:
            return "UP"
        elif air_dir <= 225 and air_dir >= 136:
            return "LEFT"
        elif air_dir <= 315 and air_dir >= 226:
            return "DOWN"
        
    #Состояния игрока
    def state_AIR(self):
        
        self.X_SPD = 0
        self.Y_SPD = 0.2 * STT.RESIZE_SCALE
        
        if self.is_on_floor() == True:
            self.player_state = "GROUND"
        
        if get_input.key == "a" or get_input.key == "A":
                self.Y_SPD = -2
        
        for i in self.get_object:
            self.canva.move(i,
                            self.X_SPD,
                            self.Y_SPD)

    def state_GROUND(self):
        #Не в самом начале но раньше чем передвижение персонажа должен обновляться и проверяться сенсор стен*

        if self.is_on_floor() == False:
            self.player_mode = "floor"
            self.player_state = "AIR"
        
        else:
            if get_input.key == "a" or get_input.key == "A":
                self.Y_SPD = -2
        
        self.handle_floor()
        
        #Обновление положения игрока относительно пола и режима
        #колличество пикселей на который надо сдвинуть игрока по Y или X координате что бы выровнять игрока относительно пола*
        amount = 0
        
        if self.get_floor_info() != None:    
            
            # self.X_SPD = self.GROUND_SPD * -math.cos(self.get_floor_info()[2])
            # self.Y_SPD = self.GROUND_SPD * math.sin(self.get_floor_info()[2])
            
            if self.get_floor_info()[1] == 0:
                amount = 0
            else:
                amount = self.get_floor_info()[1]
            
            if self.player_mode == "floor":
            
                            if self.get_floor_info()[2] == 0 or self.get_floor_info()[2] == 360:
                                self.X_SPD = self.GROUND_SPD
                                self.Y_SPD = amount
                            else:
                                if self.get_floor_info()[2] < 90:
                                    self.X_SPD = self.GROUND_SPD
                                    self.Y_SPD = -self.GROUND_SPD + amount
                                
                                elif self.get_floor_info()[2] > 270:
                                    self.X_SPD = self.GROUND_SPD
                                    self.Y_SPD = self.GROUND_SPD + amount
                                    
                            self.handle_wall()
                            
            elif self.player_mode == "r_wall":
            
                            if self.get_floor_info()[2] == 90:
                                self.X_SPD = -amount
                                self.Y_SPD = -self.GROUND_SPD
                            else:
                            
                                if self.get_floor_info()[2] < 90:
                                    self.X_SPD = self.GROUND_SPD + -amount
                                    self.Y_SPD = -self.GROUND_SPD
                                    
                                elif self.get_floor_info()[2] > 90:
                                    self.X_SPD = -self.GROUND_SPD + -amount
                                    self.Y_SPD = -self.GROUND_SPD
                            
            elif self.player_mode == "l_wall":
            
                            if self.get_floor_info()[2] == 270:
                                self.X_SPD = -amount
                                self.Y_SPD = self.GROUND_SPD
                            else:
                                if self.get_floor_info()[2] < 270:
                                    self.X_SPD = -self.GROUND_SPD + -amount
                                    self.Y_SPD = self.GROUND_SPD
                                elif self.get_floor_info()[2] > 270:
                                    self.X_SPD = self.GROUND_SPD + -amount
                                    self.Y_SPD = self.GROUND_SPD
                                    
            elif self.player_mode == "ciling":
                            
                            if self.get_floor_info()[2] == 180:
                                self.X_SPD = -self.GROUND_SPD
                                self.Y_SPD = amount
                            else:
                            
                                if self.get_floor_info()[2] > 180:
                                    self.X_SPD = -self.GROUND_SPD
                                    self.Y_SPD = self.GROUND_SPD + amount
                                    
                                elif self.get_floor_info()[2] < 180:
                                    self.X_SPD = -self.GROUND_SPD
                                    self.Y_SPD = -self.GROUND_SPD + amount

        self.GROUND_SPD += cs.SONIC_STATS[0] * self.input_dir[0]
        
        #Speed Cap for flat Ground
        
        # if INPUT is TRUE:
        
            # if self.GROUND_SPD != 0 and self.GROUND_SPD > 0:
                # if self.GROUND_SPD > cs.max_ground_spd:
                    # self.GROUND_SPD = cs.max_ground_spd
            
            # elif self.GROUND_SPD != 0 and self.GROUND_SPD < 0:
                # if self.GROUND_SPD < -cs.max_ground_spd:
                    # self.GROUND_SPD = -cs.max_ground_spd
        
        print(self.get_wall_info())
        
        #Обновеление положения игроока
        for i in self.get_object:
                self.canva.move(i,
                                self.X_SPD,
                                self.Y_SPD)
                
    def state_DEBUG(self):
        
        self.X_SPD = self.input_dir[0] * (0.5 * STT.RESIZE_SCALE)
        self.Y_SPD = self.input_dir[1] * (0.5 * STT.RESIZE_SCALE)
        
        for i in self.get_object:

            self.canva.move(i,
                            self.X_SPD,
                            self.Y_SPD)
    
    def update_player_layer(self):
        
        HITBOX_overlap = None
        
        HITBOX_overlap = self.game_tool.get_overlap(self.HITBOX)
                                        
        for index, links in enumerate(HITBOX_overlap):
                        match self.game_tool.get_tag(links)[0]:
                            case "Blayer":
                                self.player_layer = "Bfloor"
                            case "Rlayer":
                                self.player_layer = "Rfloor"
        
    #Обновления положения, анимации, обновление рутин игрока*

    def update(self):
        
        self.update_player_layer()

        self.update_player_mode()

        match self.player_state:
            case "GROUND":
                self.state_GROUND()
            case "AIR":
                self.state_AIR()
            case "DEBUG":
                self.state_DEBUG()
        
        self.input_update()

class Floor_line:
    
    def __init__(self, canva, x_pos1, y_pos1, x_pos2, y_pos2, layer:int) -> None:
        
        '''
        Будет Слой игрока личный что будет переключаться с помощью Переключателя и слой платформ,
        он будет статичен, и будет задаваться в начале игры*
        Синий - 0
        Красный - 1
        Жёлтый - 2 -> Детектиться на любом из двух режимов пола*
        '''
        
        self.canva = canva
            
        self.layer = layer
        
        self.pos = [x_pos1, y_pos1, x_pos2, y_pos2]

        self.ground_line : object = None

    def draw_in(self):
        
        if STT.DEBUG == True:
            match self.layer:
                case 0:
                    self.ground_line = self.canva.create_line(self.pos[0], self.pos[1],
                                                       self.pos[2], self.pos[3],
                                                       fill='blue')
                    
                    self.canva.addtag_withtag("Bfloor", self.ground_line)
                    
                case 1:
                    self.ground_line = self.canva.create_line(self.pos[0], self.pos[1],
                                                           self.pos[2], self.pos[3],
                                                           fill='red')
                
                    self.canva.addtag_withtag("Rfloor", self.ground_line)
                    
                case 2:
                    self.ground_line = self.canva.create_line(self.pos[0], self.pos[1],
                                                           self.pos[2], self.pos[3],
                                                           fill='yellow')
                
                    self.canva.addtag_withtag("Yfloor", self.ground_line)
            
        
        else:
            match self.layer:
                case 0:
                    self.ground_line = self.canva.create_line(self.pos[0], self.pos[1],
                                                       self.pos[2], self.pos[3],
                                                       fill='')
                    
                    self.canva.addtag_withtag("Bfloor", self.ground_line)
                    
                case 1:
                    self.ground_line = self.canva.create_line(self.pos[0], self.pos[1],
                                                           self.pos[2], self.pos[3],
                                                           fill='')
                
                    self.canva.addtag_withtag("Rfloor", self.ground_line)

                case 2:
                    self.ground_line = self.canva.create_line(self.pos[0], self.pos[1],
                                                           self.pos[2], self.pos[3],
                                                           fill='')
                
                    self.canva.addtag_withtag("Yfloor", self.ground_line)

    def clear_out(self):
        self.canva.delete(self.ground_chank) 

class Layer_Switcher:

    def __init__(self, canva, x_pos1, y_pos1, x_pos2, y_pos2, layer:int):
        self.canva = canva
        self.pos = [x_pos1, y_pos1, x_pos2, y_pos2]
        
        self.layer = layer
        
        self.collision = None
        
    def draw_in(self):
        if STT.DEBUG == True:
            match self.layer:
                case 0:
                    self.collision = self.canva.create_rectangle(self.pos[0], self.pos[1],
                                                            self.pos[2], self.pos[3], 
                                                            fill="blue")

                    self.canva.addtag_withtag("Blayer", self.collision)
                    
                case 1:
                    self.collision = self.canva.create_rectangle(self.pos[0], self.pos[1],
                                                            self.pos[2], self.pos[3], 
                                                            fill="red")

                    self.canva.addtag_withtag("Rlayer", self.collision)    
        else:
            match self.layer:
                case 0:
                    self.collision = self.canva.create_rectangle(self.pos[0], self.pos[1],
                                                            self.pos[2], self.pos[3], 
                                                            fill="")

                    self.canva.addtag_withtag("Blayer", self.collision)
                    
                case 1:
                    self.collision = self.canva.create_rectangle(self.pos[0], self.pos[1],
                                                            self.pos[2], self.pos[3], 
                                                            fill="")

                    self.canva.addtag_withtag("Rlayer", self.collision)

    def clear_out(self):
        self.canva.delete(self.collision)

if __name__ == "__main__":
    
    #Инициализация главных составляющих программы*
    root = GameWindow("Objects Test", STT.screen_size[0], STT.screen_size[1], STT.screen_resizable)

    canva = GameCanvas(root, width=STT.canva_size[0], height=STT.canva_size[1], bg="black")
    
    ATLAS1 = tk.PhotoImage(file="Resources/Tails1.png")
    
    get_input = InputTool(canva)
    get_input.UPDATE()
    
    fps_show = tk.Label(canva, background="black")
    fps_show.pack()
    
    # get_audio = AudioTool()
    # get_audio.load_sound("ppp.wav", loop=True)
    # get_audio.play_sound()

    #Инициализация объектов*
    #ПОДГРУЗКА .level файла
    #DOWN UP
    g1 = Floor_line(canva, (320/2 - 320/12), (240/2+240/3),
                            320/2 + 320/12, 240/2+240/3, 2)
                            
    g2 = Floor_line(canva, (320/2 + 320/12), (240/2-240/3),
                            320/2 - 320/12, 240/2-240/3, 2)
    #LEFT RIGHT
    g3 = Floor_line(canva, (320/2 - 240/3), (240/2 - 240/12),
                            (320/2 - 240/3), (240/2 + 240/12), 1)
    
    g4 = Floor_line(canva, (320/2 + 240/3), (240/2 + 240/12),
                            (320/2 + 240/3), (240/2 - 240/12), 0)
    
    #F->R
    g5 = Floor_line(canva, (320/2 + 320/12), (240/2+240/3),
                            (320/2 + 240/3)-20, (240/2 + 240/12)+40, 0)
    
    g6 = Floor_line(canva, (320/2 + 240/3)-20, (240/2 + 240/12)+40,
                            320/2 + 240/3, 240/2 + 240/12, 0)
    
    #R->C
    g7 = Floor_line(canva, 320/2 + 240/3, 240/2 - 240/12,
                            (320/2 + 320/12)+40, (240/2-240/3)+30, 2)
    
    g8 = Floor_line(canva, (320/2 + 320/12)+40, (240/2-240/3)+30,
                            320/2 + 320/12, 240/2-240/3, 2)
                            
    #C->L
    g9 = Floor_line(canva, 320/2 - 320/12, 240/2-240/3,
                            (320/2 - 240/3)+15, (240/2 - 240/12)-30, 2)
    
    g10 = Floor_line(canva, (320/2 - 240/3)+15, (240/2 - 240/12)-30,
                            320/2 - 240/3, 240/2 - 240/12, 2)
    
    #L->F
    g11 = Floor_line(canva, 320/2 - 240/3, 240/2 + 240/12,
                            (320/2 - 320/12)-40, (240/2+240/3)-30, 1)
                            
    g12 = Floor_line(canva, (320/2 - 320/12)-40, (240/2+240/3)-30,
                            320/2 - 320/12, 240/2+240/3, 1)
    
    #WALL_FLOOR
    g13 = Floor_line(canva, 4, (240/2+240/3),
                            4, 240/2+240/8, 2)
    
    #GROUND_LEFT
    g14 = Floor_line(canva, 0, (240/2+240/3),
                            (320/2 - 320/12), (240/2+240/3), 0)
    
    #GROUND_RIGHT
    g15 = Floor_line(canva, 320/2 + 320/12, 240/2+240/3,
                            320, 240/2+240/3, 1)
    
    #WALL RIGHT
    g16 = Floor_line(canva, 320, (240/2+240/3),
                            320, 240/2+240/8, 2)
    
    #LAYER SWITCH
    sw1 = Layer_Switcher(canva, (320/2), (240/8),
                                (135), 80,
                                1)
    
    sw2 = Layer_Switcher(canva, 320/2, 240/8,
                                185, 80,
                                0)
    
    #Рисование уровня из файла
    print("Уровень загружается...")
    
    #Объявление списка объектов
    level = SP.Spisok_Link()
    
    #Загрузка всех существующих объектов
    level.Add_in_end(g1)
    level.Add_in_end(g2)
    level.Add_in_end(g3)
    level.Add_in_end(g4)
    level.Add_in_end(g5)
    level.Add_in_end(g6)
    level.Add_in_end(g7)
    level.Add_in_end(g8)
    level.Add_in_end(g9)
    level.Add_in_end(g10)
    level.Add_in_end(g11)
    level.Add_in_end(g12)
    level.Add_in_end(g13)
    level.Add_in_end(g14)
    level.Add_in_end(g15)
    level.Add_in_end(g16)
    level.Add_in_end(sw1)
    level.Add_in_end(sw2)
    
    #Указатель на первый элемент списка
    p = level._Start
    
    for i in range(level.count_check()):
    
        p.elem.draw_in()
        print("Объект " + str(p.elem) + str(i) + " был создан.")
        
        p = p.nextNode
        
    IDLE = SpriteObject("idle", canva, ATLAS1, 1, 1, 24, 32)
    
    player = Sonic(20, 20, IDLE, canva, get_input, Game_Tool(canva))
    
    player.draw_in()

    cs.update()
    
    #Запуск главного цикла программы*
    def game_update():
        
        player.update()
        
        canva.update()
        
        canva.update_by_tick(1, game_update)
    
    game_update()
    
    root.game_mainloop(canva)

