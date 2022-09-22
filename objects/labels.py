from kivy.uix.label import Label
from .gameutils import KeepScale as ks

class GameLabel(Label):
    
    def __init__(self):
        
        super().__init__()
        self.text = ''
        self.font_size = ks.to_wh(35)
        self.text_size = [ks.to_wh(450), ks.to_wh(40)]
        self.halign = 'left'
        self.valign = 'center'
        self.coll_code = 0
        self.health = 1
        self.shooting = 0
        
    def moving(self, factor):
        pass
        
    def score(self):
        return 0


class Label1(GameLabel):
    
    def __init__(self):
        
        super().__init__()
        self.pos = [ks.to_ww(170), ks.to_wh(2095)]
        
    def tx(self, add_text):
        self.text = '{0}{1}'.format('Score: ', add_text)
    
    
class Label2(GameLabel):
    
    def __init__(self):
        
        super().__init__()
        self.pos = [ks.multip_ww(0.45), ks.to_wh(1200)]
        self.font_size = ks.to_ww(45)
        self.text_size = [ks.multip_ww(1), ks.to_ww(45)]
        self.halign = 'center'
        self.valign = 'center'
    
    def tx(self, add_text):
        self.text = ''
    
class Label3(GameLabel):
    
    def __init__(self):
        
        super().__init__()
        self.pos = [ks.to_ww(170), ks.to_wh(2200)]
        
    def tx(self, add_text):
        self.text = '{0}{1}'.format('Best score: ', add_text)


class Label4(GameLabel):
    
    def __init__(self):
        
        super().__init__()
        self.pos = [ks.to_ww(170), ks.to_wh(2165)]
        
    def tx(self, add_text):
        self.text = '{0}{1}'.format('Level: ', add_text)


class Label5(GameLabel):
    
    def __init__(self):
        
        super().__init__()
        self.pos = [ks.to_ww(170), ks.to_wh(2130)]
        
    def tx(self, add_text):
        self.text = '{0}{1}'.format('Energy: ', add_text)
        
        
       
