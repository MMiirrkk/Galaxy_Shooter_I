from kivy.core.window import Window
from kivy.vector import Vector
from kivy.uix.widget import Widget
        

class GameTimeScore:

    @staticmethod
    def gameclk_add(game_clock_on, game_clock):
        '''
        time score func
        '''
        if game_clock_on ==1:
            game_clock+=1
        
        return game_clock
    
    @staticmethod
    def score_add(score_on, score, game_clock):
       
        if score_on ==1:
            if game_clock%100==0:
                score += 1
        return score
        
   
class KeepScale():
    
 
    @staticmethod
    def to_wh(value):
        _, wh = Window.size
        return round(value*(wh/2400))

    @staticmethod
    def to_ww(value):
        ww, _ = Window.size
        return round(value*(ww/1080))
        
    @staticmethod
    def partof_wh(value):
        _, wh = Window.size
        return wh//value
        
    @staticmethod
    def partof_ww(value):
        ww, _ = Window.size
        return ww//value
        
    @staticmethod
    def mov_sc(value):
        _, wh = Window.size
        return round(value*(wh/2400))
    
    @staticmethod
    def multip_ww(value):
        ww, _ = Window.size
        return round(value*ww)
       
    @staticmethod
    def multip_wh(value):
        _, wh = Window.size
        return round(value*wh)


class Instances():
    
    
    @staticmethod
    def find_inst(name, inst_list):
        for n in inst_list:
            if name in str(n):
                return n
                
    @staticmethod
    def is_in(name, inst_list):
        finded = False
        for n in inst_list:
            if name in str(n):
                finded = True
        return finded
    
    @staticmethod
    def backgr_name(seq, game_level):
        if seq==1:
            pref = 'a'
        else: pref = ''
        back = 'backgrlev'
        return '{0}{1}{2}'.format(back, game_level, pref)
    
