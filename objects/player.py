from .gameunit import GameUnit
from .gameutils import KeepScale as ks

class Player1(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.factor = 6
        self.size = [ks.partof_ww(self.factor+2), ks.partof_ww(self.factor)]
        self.pos = [ks.partof_ww(2) -self.size[0]//2, ks.partof_wh(6)]
        self.health = 5
        self.coll_code = 1
    
    def moving(self, factor):
        super().moving(factor)
       
        if self.health>0:
            if self.pos[0]<=-self.vel[0] and self.vel[0]<0:
                self.pos[0] = 0
                self.vel[0] = 0
                self.acc[0] = 0
                
            if self.pos[0]>=ks.multip_ww(1)-(self.size[0]+self.vel[0]) and self.vel[0]>0:
                self.pos[0] = ks.multip_ww(1) - self.size[0]
                self.vel[0] = 0
                self.acc[0] = 0
        
    def score(self):
        return 0
        