from .gameunit import GameUnit
import random as rd

class Asteroid1(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.size = [100, 100]
        self.pos = [(rd.randint(0, self.ww - self.size[0])), (self.wh)]
        self.health = 3
        self.vel = [0, 0]
        self.coll_code = 2
        
    def score(self):
        return 5
        
            