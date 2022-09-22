from .gameunit import GameUnit


class Arrow_left(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.size = [100, 100]
        self.pos = [0, 0]
        
    def setup(self, buttons):
        self.size = [self.ww//buttons[0], self.wh//buttons[2]]
        self.pos = [0, 0]
        
        
class Arrow_right(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.size = [100, 100]
        self.pos = [0, 0]
        
    def setup(self, buttons):
        self.size = [self.ww//(buttons[0]), self.wh//buttons[2]]
        self.pos = [self.ww//buttons[1], 0]
        

class Shoot_label(GameUnit):
    
    def __init__(self):
        super().__init__()
        self.size = [100, 100]
        self.pos = [0, 0]
        
    def setup(self, buttons):
        self.size = [(self.ww-(2*self.ww//buttons[0])), self.wh//buttons[2]]
        self.pos = [self.ww//buttons[0], 0]
    