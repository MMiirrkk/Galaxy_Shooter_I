from .player import Player1
from .enemy import (
Enemy1, Enemy2, Boss1, Boss2
)
from .asteroids import Asteroid1
from .background import (
Backgr_lev1, Backgr_lev1a, Backgr_lev2, Backgr_lev2a, Backgr_lev3, Backgr_lev3a,
Backgr_lev4, Backgr_lev4a, Backgr_lev5,
Backgr_lev5a
)
from .startboard import StartBoard
from .explosion import (
ExplBig, ExplSmall)
from .shootall import (
ShootPlayer, ShootEnemy)
from .staticobjects import (
Arrow_left, Arrow_right, Shoot_label)
from .labels import  (
    Label1, Label2, Label3, Label4, Label5)

class UnitFactory():
    
    units_dict = {
        'startboard': StartBoard,
        'player1':Player1,
        'asteroid1':Asteroid1,
        'enemy1':Enemy1,
        'enemy2':Enemy2,
        'boss1':Boss1,
        'boss2':Boss2,
        'asteroids':Asteroid1,
        'explbig':ExplBig,
        'explsmall':ExplSmall,
        'shootplayer':ShootPlayer,
        'shootenemy':ShootEnemy,
        'backgrlev1':Backgr_lev1,
        'backgrlev1a':Backgr_lev1a,
        'backgrlev2':Backgr_lev2,
        'backgrlev2a':Backgr_lev2a,
        'backgrlev3':Backgr_lev3,
        'backgrlev3a':Backgr_lev3a,
        'backgrlev4':Backgr_lev4,
        'backgrlev4a':Backgr_lev4a,
        'backgrlev5':Backgr_lev5,
        'backgrlev5a':Backgr_lev5a,
        'arrowleft':Arrow_left,
        'arrowright':Arrow_right,
        'shootlabel':Shoot_label,
        'label1':Label1,
        'label2':Label2,
        'label3':Label3,
        'label4':Label4,
        'label5':Label5
        }
        
    @classmethod
    def create_unit(cls, unit_type, *a, **kwa):
        return cls.units_dict.get(unit_type)(*a, **kwa)
    
    
class Units():
    
    factory = UnitFactory
    
    
    def build_unit(self, unit_type, *a, **kwa):
        
        unit = self.__class__.factory.create_unit(unit_type, *a, **kwa)
        #self.update_records(unit_type)
        return unit
    
    #def update_records(self,unit_type):
       #pass
    
    def cr_sources(self):
        sources = [
        'startboard',
        'player1',
        'asteroid1',
        'enemy1',
        'enemy2',
        'boss1',
        'boss2',
        'asteroids',
        'explbig',
        'explsmall',
        'shootplayer',
        'shootenemy',
        'backgrlev1',
        'backgrlev1a',
        'backgrlev2',
        'backgrlev2a',
        'backgrlev3',
        'backgrlev3a',
        'backgrlev4',
        'backgrlev4a',
        'backgrlev5',
        'backgrlev5a',
        'arrowleft',
        'arrowright',
        'shootlabel',
        'label1',
        'label2',
        'label3',
        'label4',
        'label5'
        ]
        
        for n in sources:
            self.build_unit(n)