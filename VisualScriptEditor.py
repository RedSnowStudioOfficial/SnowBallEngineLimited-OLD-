from RSS_SDK import *
from game_objects import *
from PIL import Image, ImageTk
import Settings as STT
import math

"""
SnowBallVS - это язык визуального программирования преднозначенный
для взаимодействия с объектами и функционалом встроенным в проект SBEngineDirected
"""

class DragableBlock():
    """
    Объект контейнер который принимает в себя входные данные и изменяется
    в зависимости от того какого типа сам является
    К блоку можно подключится другим блокам что бы запустить вереницу событий
    """
    def __init__(self, name, inconnect:list, outconnect:list,
                                inputs:list, outputs:list):
        pass

class EmptyStaticNode(object, elem):
    """
    Нода - это виртуальный объект содержащий в себе информацию о его принадлежности
    Нода что не принимает входных данных,
    а так же не даёт ничего в выходных данных
    может быть использованна для блока коментария
    """
    
    def __init__(self, elem):
        self.elem = elem
        self.InputInfo = None
        self.OutputInfo = None

class VSeditor:
    def __init__(self):
        '''
        Окно редактора, в реализации почти ничем не отличается от MapEditor
        '''
        pass
