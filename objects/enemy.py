from .gameunit import GameUnit
from kivy.vector import Vector
import random as rd
from .gameutils import KeepScale as ks


class Enemy(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.coll_code = 2
        self.pos = [0, 0]
        self.shoot_aimed = 0
        self.shoot_random = 0
        
    def screen_end_dir_change(self):
        if self.pos[0]>self.ww - self.size[0]*0.55 and self.vel[0] > 0:
            self.vel[0] = -self.vel[0]
            
        if self.pos[0]<-self.size[0]*0.25 and self.vel[0] < 0:
            self.vel[0] = -self.vel[0]
                  
    def random_loc_m(self, v_min, v_max):
        
        loc = [-self.size[0], self.size[0] + self.ww]
        sel = rd.choice(loc)
        self.pos = [sel, rd.randint(self.wh//1.33, self.wh//1.05)]
        if sel>0:
            self.vel = Vector(-rd.randint(v_min, v_max), 0)
        elif sel<0:
            self.vel = Vector(rd.randint(v_min, v_max), 0)
        
        
class Enemy1(Enemy):
   
    def __init__(self):
        super().__init__()
        self.factor = 6
        self.shooting = 2
        self.size = [self.ww//self.factor, self.ww//(self.factor*1.5)]
        self.health = 4
        self.random_loc()
         
    def moving(self, factor):
        super().moving(factor)
        super().screen_end_dir_change()
        
    def random_loc(self):
        super().random_loc_m(2, 3)
        
    def score(self):
        return 20
        
        
class Enemy2(Enemy):

    def __init__(self):
        super().__init__()
        self.factor = 6
        self.shooting = 1
        self.size = [self.ww//self.factor, self.ww//(self.factor*1.5)]
        self.health = 2
        self.random_loc()
        
    def moving(self, factor):
        super().moving(factor)
        super().screen_end_dir_change()
       
    def random_loc(self):
        super().random_loc_m(3, 4)
        
    def score(self):
        return 10
        
        
class Boss1(Enemy):

    def __init__(self):
        super().__init__()
        self.factor = 2
        self.shooting = 3
        self.size = [self.ww//self.factor, self.ww//(self.factor*1.5)]
        self.pos = [self.ww + self.size[0], self.wh-self.size[1]*2]
        self.vel = [-5, 0]
        self.health = 30
   
    def moving(self, factor):
        super().moving(factor)
        super().screen_end_dir_change()
        
    def score(self):
        return 100
   
   
class Boss2(Enemy):

    def __init__(self):
        super().__init__()
        self.factor = 1.4
        self.shooting = 3
        self.size = [self.ww//self.factor, self.ww//(self.factor*1.5)]
        self.pos = [self.ww + self.size[0]*1.2, self.wh-self.size[1]*1.5]
        self.vel = [-4, 0]
        self.health = 100
       
    def moving(self, factor):
        super().moving(factor)
        super().screen_end_dir_change()
        
    def score(self):
        return 1000
    