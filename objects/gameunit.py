from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.core.window import Window

class GameUnit(Widget):
    
    def __init__(self):
        super().__init__()
        self.ww, self.wh = Window.size
        self.factor = 0
        self.size = [0, 0]
        self.pos = [0, 0]
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.health = 1
        self.end_screen_remove = 1
        self.coll_code = 0
        self.shooting = 0
     
    
    def moving(self, factor):
        self.vel = Vector(self.vel) + Vector(self.acc)
        self.pos = Vector(self.pos) + Vector(self.vel)*factor
            
    def stop(self):
        self.vel = [0, 0]
        self.acc = [0, 0]
        
    def hit_1(self):
        self.health -=1
        
    def hit_2(self):
        self.health -= 1
 