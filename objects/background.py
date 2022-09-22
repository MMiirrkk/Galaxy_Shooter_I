from .gameunit import GameUnit


class Background(GameUnit):
    
    def __init__(self):       
        super().__init__()
        self.size = [self.ww, self.wh+5]
        self.end_screen_remove = 0
    
    def moving(self, factor):
        self.pos_reload()
        super().moving(factor)
        
    def start(self):
        self.vel[1] = -4
          
    def pos_reload(self):
        if self.pos[1]<-self.wh:
            self.pos[1] = self.wh
            
            
class Backgr_lev1(Background):
        
    pass
        
        
class Backgr_lev1a(Background):
    
    def __init__(self):
        super().__init__()
        self.pos = [0, self.wh]
        
        
class Backgr_lev2(Background):
    
    pass
    
        
class Backgr_lev2a(Background):
    
    def __init__(self):
        super().__init__()
        self.pos = [0, self.wh]
        

class Backgr_lev3(Background):
    
    pass
        
        
class Backgr_lev3a(Background):
    
    def __init__(self):
        super().__init__()
        self.pos = [0, self.wh]
        
        
class Backgr_lev4(Background):
    
    pass
        
        
class Backgr_lev4a(Background):
    
    def __init__(self):
        super().__init__()
        self.pos = [0, self.wh]
    
    
class Backgr_lev5(Background):
    
    pass
        
        
class Backgr_lev5a(Background):
    
    def __init__(self):
        super().__init__()
        self.pos = [0, self.wh]
        
        