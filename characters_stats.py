import Settings as STT

#Вспомогательные переменные отвечающие за изменения размеров проверки пола
sensor_resize = 19

sensor_resize_l_f : float = 19
sensor_resize_r_c : float = -19

#При сворачивании в клубок
sensor_resize_l_f_roll : float = 14
sensor_resize_r_c_roll : float = -14

#Значения вычета скорости при уклоне земли*
slope_factor : float = 0

#Sonic Stats:
#                    0 STAND,   1 ROLL,  2 HITBOX
HEIGHTradius : list = [19,         14,        6]
WIDTHradius : list =  [9,           7,        8]
#                        0 ACCELERATION  1 DECELERATION   2 FRICTION     3 TOP_SPD   4 GRAVITY    5 slope_factor_normal	  6 slope_factor_rollup    7 slope_factor_rolldown
SONIC_STATS : list = [     0.046875,           0.5,        0.046875,             6,       0.21875,           0.125,                  0.078125,                  0.3125]

max_ground_spd = 6

#Длина датчика стен*
push_radius : int = 10

#Сдвиг датчиков стен если угол пола равен нулю* 
wall_offcet : int = 8

#Сделать проверку на развершение экрана*
#Относительно разрешения будут меняться показатели персонажей*

def update():
    
    global SONIC_STATS, HEIGHTradius, WIDTHradius, sensor_resize, sensor_resize_l_f, sensor_resize_r_c, sensor_resize_l_f_roll, sensor_resize_r_c_roll, wall_offcet, push_radius, max_ground_spd
    
    sensor_resize = 19 * STT.RESIZE_SCALE
        
    sensor_resize_l_f = 19 * STT.RESIZE_SCALE
    sensor_resize_r_c = -19 * STT.RESIZE_SCALE
        
    sensor_resize_l_f_roll = 14 * STT.RESIZE_SCALE
    sensor_resize_r_c_roll = -14 * STT.RESIZE_SCALE
        
    wall_offcet = 8 * STT.RESIZE_SCALE
        
    push_radius = 10 * STT.RESIZE_SCALE
        
    HEIGHTradius = [19*STT.RESIZE_SCALE,      14*STT.RESIZE_SCALE,       6*STT.RESIZE_SCALE]
    WIDTHradius =  [9*STT.RESIZE_SCALE,        7*STT.RESIZE_SCALE,       8*STT.RESIZE_SCALE]

    SONIC_STATS = [ (0.046875/2) * STT.RESIZE_SCALE,        (0.5/2) * STT.RESIZE_SCALE,       (0.046875/2) * STT.RESIZE_SCALE,       (6/2) * STT.RESIZE_SCALE,      (0.21875/2) * STT.RESIZE_SCALE]
    
    max_ground_spd = max_ground_spd * STT.RESIZE_SCALE

