from .gameunit import GameUnit


class Explosion(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.health = 1
    
    def expand_calc(self):
        factor = 1 + 0.01*(self.factor - self.health)
        self.size[0] = int((self.origin_size[0])*factor)
        self.size[1] = int((self.origin_size[1])*factor)
        self.pos[0] = int(self.pos[0] - (self.size[0]*(factor-1)//2))
        self.pos[1] = int(self.pos[1] - (self.size[1]*(factor-1)//2))
        self.health -= 1
    

class ExplBig(Explosion):
    
    def __init__(self):
        super().__init__()
        self.size = [self.ww//4, self.ww//4]
        self.origin_size = self.size
        self.health = 10
        self.factor = self.health
        
    
class ExplSmall(Explosion):
    
    def __init__(self):
        super().__init__()
        self.size = [self.ww//10, self.ww//10]
        self.origin_size = self.size
        self.health = 5
        self.factor = self.health
    