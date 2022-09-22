from .gameunit import GameUnit
from kivy.vector import Vector

class ShootAll(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.size = [self.ww//40, self.ww//10]
        
        
class ShootPlayer(ShootAll):
    
    def __init__(self):
        super().__init__()
        self.pos = [-500, self.ww*3]
        self.speed_scale = self.wh/2400
        self.coll_code = 3
        
    def shoot(self, shooter):
        self.pos[0] = shooter.pos[0] + (shooter.size[0]//2) - (self.size[0]//2)
        self.pos[1] = shooter.pos[1] + shooter.size[1]
        self.vel = Vector(0, 50*self.speed_scale)
        
        
class ShootEnemy(ShootAll):
    
    def __init__(self):
        super().__init__()
        self.pos =  [-500, -self.wh]
        self.speed_scale = self.wh/2400
        self.coll_code = 4
        
    def shoot_start_param(self, shooter):
        self.pos[0] = shooter.pos[0] + (shooter.size[0]//2) - (self.size[0]//2)
        self.pos[1] = shooter.pos[1] - self.size[1]
        self.vel = Vector(0, -20)
 