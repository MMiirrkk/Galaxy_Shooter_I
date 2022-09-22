import random as rd
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from objects.gameutils import GameTimeScore
from objects.gameutils import KeepScale as ks
from objects.gameutils import Instances as inst
from objects.unitfactory import Units


class KivyGame(Widget):
    
    def __init__(self, *a, **kwa):
        super().__init__(*a, **kwa)
        
        self.units = Units()
        
        self.game_clock_on = 0
        self.score_on = 0
        self.game_clock = 0
        self.start_wait = 1
        self.game_delay = 0
        self.game_delay_code = 0
        self.score = 0
        self.best_score = 0
        self.game_level = 0
        self.pl_health = 5
        self.inst_list =[]
        
        #buttons scale factors [left, right
        #, height
        self.buttons = [4, 1.333, 50]
        
        self.units.cr_sources()
        self.start_board_on()
        self.set_frames = 100
        self.set_frames_2 = 60
        self.t_1 = time.time()
        #motion run
        Clock.schedule_interval(self.update, 1.0 / self.set_frames)
        '''
        #to handle:
        1. scaling and performance pronlem
        2. hard load problem - back to preload image on start?
        '''
       
    #====motion handler====
    def update(self, dt):
        #self.t_2 = time.time() - self.t_1
        #self.real_fps = 1 / self.t_2
        #self.tf = self.set_frames_2/self.real_fps
        #self.t_1 = time.time()
        self.tf = 1
        self.game_frame()
        
        
    def game_frame(self):
        
        #game clock update
        self.game_clock = GameTimeScore.gameclk_add(self.game_clock_on, self.game_clock)
        
        #score update
        self.score = GameTimeScore.score_add( self.score_on,  self.score, self.game_clock)
        
        #timeline update
        self.timeline()
        
        #time delay update
        self.game_time_delay()
        
        #moving all existing
        [n.moving(self.tf) for n in self.inst_list]
        
        #enemy shooting
        for n in self.inst_list:
            if n.shooting>0:
                n.shoot_aimed += 1
                n.shoot_random += 1
                
            if (n.shooting==2 and n.shoot_aimed>15) or (n.shooting==3 and n.shoot_aimed>15):
                self.aimed_shooting(n)
                n.shoot_aimed = 0
                
            if (n.shooting==1 and n.shoot_random>100) or (n.shooting==3 and n.shoot_random>100):
                self.cr_inst('shootenemy').shoot_start_param(n)
                n.shoot_random = 0
               
        #collision checking
        for n in self.inst_list:
            if n.coll_code==1:
                for m in self.inst_list:
                    if m.coll_code==2 or m.coll_code==4:
                        self.coll_check(n, m)
            if n.coll_code==2:
                for m in self.inst_list:
                    if m.coll_code==3:
                        self.coll_check(n, m)
                        
        self.check_health()
                
        #explosion expand
        if inst.is_in('Expl', self.inst_list):
            for n in self.inst_list:
                if 'Expl' in str(n):
                    n.expand_calc()
                              
        for n in self.inst_list:
            if 'Label1' in str(n):
                #n.tx(round(self.real_fps))
                n.tx(self.score)
            if 'Label3' in str(n):
                n.tx(self.best_score)
            if 'Label4' in str(n):
                n.tx(self.game_level)
            if 'Label5' in str(n):
                if inst.is_in('Player1', self.inst_list):
                    n.tx(inst.find_inst('Player1', self.inst_list).health)
        
        self.remove_off_screen()
   
    def game_start(self):
  
        self.game_clock_on = 0
        self.score_on = 0
        self.game_clock = 0
        self.rem_all_inst()
        self.game_clock_on = 1
        self.score_on = 1
        self.game_level += 1
        self.game_delay = 0
        self.game_delay_code = 0
        self.cr_inst(inst.backgr_name(0, self.game_level)).start()
        self.cr_inst(inst.backgr_name(1, self.game_level)).start()
        self.cr_inst('player1').health = self.pl_health
        self.cr_inst('label1')
        self.cr_inst('label3')
        self.cr_inst('label4')
        self.cr_inst('label5')
        self.cr_inst('arrowleft').setup(self.buttons)
        self.cr_inst('arrowright').setup(self.buttons)
        self.cr_inst('shootlabel').setup(self.buttons)
    
    
    def player_destroyed(self):
        if inst.is_in('Player1', self.inst_list):
            f = inst.find_inst('Player1', self.inst_list)
            if f.health<=0:
                self.cr_inst('label2').text = "GAME OVER"
                self.game_delay_code = 1
                self.game_delay = 1
                f.health = 0
                self.score_on = 0
                for n in self.inst_list:
                    if 'Label5' in str(n):
                        n.tx('0')
          
                
    def game_time_delay(self):

        if self.game_delay>0:
            self.game_delay += 1
            
            if self.game_delay_code==1 and self.game_delay>230/self.tf:
                self.game_delay = 0
                self.game_delay_code = 0
                self.player_loose()
                
            if self.game_delay_code==2 and self.game_delay>230/self.tf:
                self.game_delay = 0
                self.game_delay_code = 0
                self.level_finnish()
                
            if self.game_delay_code==3 and self.game_delay>230/self.tf:
                self.game_delay = 0
                self.game_delay_code = 0
                self.win_game()
            
            
    def level_finnish(self):
        
        self.rem_inst(inst.find_inst('Label2', self.inst_list))
        self.cr_inst('label2').text = "Tap to continue"
        self.score_on = 0
        self.score = self.score + 30
        self.start_wait =1
        self.pl_health = inst.find_inst('Player1', self.inst_list).health
        self.pl_health +=1
        
        
    def win_game(self):
        self.player_loose()
               
               
    def player_loose(self):
        
        self.score_on = 0
        self.game_level=0
        self.game_clock_on = 0
        self.game_clock = 0
        if self.best_score < self.score:
            self.best_score = self.score
        self.score = 0
        self.rem_all_inst()
        self.start_board_on()
        self.start_wait =1
        self.pl_health = 5
   
    
    def start_board_on(self):
        self.rem_all_inst()
        self.cr_inst('startboard')
        self.cr_inst('label2').text = "Tap to START"
        
  
    def remove_off_screen(self):
        for n in self.inst_list:
            if n.pos[1]>ks.multip_wh(1.1) or (n.pos[1]+n.size[1])<ks.multip_wh(-0.1):
                if n.end_screen_remove == 1:
                    self.rem_inst(n)
    
    
    def aster_deploy(self, smin, smax, vmin, vmax):
        #delete and create labels here***
        c = self.cr_inst('asteroids')
        random_size = ks.to_wh(rd.randint(smin, smax))
        c.size = [random_size, random_size]
        c.vel[1] = (-rd.randint(vmin, vmax))
    
    
           
    def cr_inst(self, name):
        #create instance
        instance = self.units.build_unit(name)
        self.add_widget(instance)
        self.inst_list.append(instance)
        return instance
    
    
    def rem_inst(self, instance):
        self.remove_widget(instance)
        self.inst_list.remove(instance)
        del instance
                
                
    def rem_all_inst(self):
        #remove all instances
        for n in self.inst_list:
            self.rem_inst(n)
        if len(self.inst_list)>0:
            self.rem_all_inst()
            
            
    def coll_check(self, obj1, obj2):
        if obj1.pos[1] < (obj2.pos[1] + obj2.size[1]) and obj1.pos[0] < (obj2.pos[0] + obj2.size[0]) and obj2.pos[1] < (obj1.pos[1] + obj1.size[1]) and obj2.pos[0] < (obj1.pos[0] + obj1.size[0]):
           
            obj1.health -= 1
            obj2.health -= 1
            w = self.cr_inst('explsmall')
            w.pos[0] = obj2.pos[0] + (obj2.size[0]//2) - (w.size[0]//2)
            if obj1.pos[1]>obj2.pos[1]:
                w.pos[1] = obj1.pos[1] - (w.size[1]//2)
            else: w.pos[1] = obj2.pos[1] - (w.size[1]//2)
            
    
    def aimed_shooting(self, shooter):
        if inst.is_in('Player1', self.inst_list):
            target = inst.find_inst('Player1', self.inst_list)
            if target.pos[0]+(target.size[0]*0.75)>(shooter.pos[0]+(shooter.size[0]//2))>target.pos[0] + target.size[0]*0.25:
                self.cr_inst('shootenemy').shoot_start_param(shooter)
                
                            
            
    def check_health(self):
        for n in self.inst_list:
            if n.health <= 0:
                if 'Player' in str(n):
                    self.player_destroyed()
                if 'Expl' not in str(n) and 'Shoot' not in str(n):
                    w = self.cr_inst('explbig')
                    w.pos = Vector(n.pos) + Vector(n.size)/2 - Vector(w.size)/2
                    self.score = self.score + n.score()
                self.rem_inst(n)
                     
                      
    #====Game controls====
    #buttons down
    def on_touch_down(self, touch):
     
        #screen touch vector
        self.v1 = Vector(touch.pos)
        
        #waiting for tap to start
        if self.start_wait == 1:
            self.start_wait = 0
            self.game_start()
              
        #left button
        if self.v1[0]<ks.partof_ww(self.buttons[0]):
            if inst.is_in('Player1', self.inst_list):
                inst.find_inst('Player1', self.inst_list).acc = Vector(-1, 0)
                     
        #shoot button
        if ks.partof_ww(self.buttons[1])>self.v1[0]>ks.partof_ww(self.buttons[0]):
           if inst.is_in('Player1', self.inst_list):
               self.cr_inst('shootplayer').shoot(inst.find_inst('Player1', self.inst_list))
            
       #right button
        if self.v1[0]>ks.partof_ww(self.buttons[1]):
            if inst.is_in('Player1', self.inst_list):
                inst.find_inst('Player1', self.inst_list).acc = Vector(1, 0)
                                            
    #buttons up
    def on_touch_up(self, touch):
        if inst.is_in('Player1', self.inst_list):
            inst.find_inst('Player1', self.inst_list).stop()
                   
                               
    def timeline(self):
        
        #__________level1__________
        if self.game_level==1:
            
            if 3800/self.tf>self.game_clock>100/self.tf:
                if self.game_clock%(50//self.tf)==1:
                    self.aster_deploy(50, 150, 6, 7)
                              
            if 7000/self.tf>self.game_clock>4000/self.tf:
                if self.game_clock%(40//self.tf)==1:
                    self.aster_deploy(50, 170, 6, 8)
                
            if self.game_clock==7200//self.tf:
                self.score_on = 0
                self.cr_inst('label2').text = "Level 1 complete!"
                
            if self.game_clock==7350/self.tf:
                self.level_finnish()
                
       #__________level2__________
        if self.game_level==2:
                 
            if 6800/self.tf>self.game_clock>20/self.tf:
                if self.game_clock%(500//self.tf)==1:
                    self.cr_inst('enemy1')
            
            if 6800/self.tf>self.game_clock>2000/self.tf:
                if self.game_clock%(800//self.tf)==1:
                    self.cr_inst('enemy2')
            
            if self.game_clock==6900/self.tf:
                for n in self.inst_list:
                    if 'Enemy1' in str(n) or 'Enemy2' in str(n):
                        n.vel = [0, 4]
            
            if self.game_clock==7100/self.tf:
                self.score_on = 0
                self.cr_inst('label2').text = "Level 2 complete!"
                
            if self.game_clock==7250/self.tf:
                self.level_finnish()
                
        #__________level3__________
        if self.game_level==3:
            
            if 3300/self.tf>self.game_clock>100/self.tf:
                if self.game_clock%(25//self.tf)==1:
                    self.aster_deploy(50, 150, 5, 7)
                
            if 6400/self.tf>self.game_clock>3400/self.tf:
                if self.game_clock%(500//self.tf)==1:
                    self.cr_inst('enemy1')
            
            if 6400/self.tf>self.game_clock>3400/self.tf:
                if self.game_clock%(800//self.tf)==1:
                    self.cr_inst('enemy2')
            
            if self.game_clock==6500/self.tf:
                for n in self.inst_list:
                    if 'Enemy1' in str(n) or 'Enemy2' in str(n):
                        n.vel = [0, 4]
               
            if self.game_clock==6800/self.tf:
                self.cr_inst('boss1')
                
            if self.game_clock>6800/self.tf and inst.is_in('Boss1', self.inst_list) is False:
                self.cr_inst('label2').text = "Level 3 complete!"
                self.game_clock = 0
                self.game_clock_on = 0
                self.game_delay = 1
                self.game_delay_code=2
                self.score_on = 0
                
        #__________level4__________
        if self.game_level==4:
            
            if 6000/self.tf>self.game_clock>100/self.tf:
                if self.game_clock%(90//self.tf)==1:
                    self.aster_deploy(50, 150, 5, 7)
            if 6800/self.tf>self.game_clock>20/self.tf:
                if self.game_clock%(400//self.tf)==1:
                    self.cr_inst('enemy1')
            
            if 6700/self.tf>self.game_clock>2000/self.tf:
                if self.game_clock%(600//self.tf)==1:
                    self.cr_inst('enemy2')
            
            if self.game_clock==6700/self.tf:
                for n in self.inst_list:
                    if 'Enemy1' in str(n) or 'Enemy2' in str(n):
                        n.vel = [0, 4]
                
            if self.game_clock==7100/self.tf:
                self.score_on = 0
                self.cr_inst('label2').text = "Level 4 complete!"
                
            if self.game_clock==7250/self.tf:
                self.level_finnish()
                
        #___________level 5__________
        if self.game_level==5:
            if self.game_clock==300/self.tf:
                self.cr_inst('boss2')
                
            if self.game_clock>300/self.tf and inst.is_in('Boss2', self.inst_list) is False:
                self.cr_inst('label2').text = "Congratulations!!! You win the game."
                self.game_clock = 0
                self.game_clock_on = 0
                self.game_delay = 1
                self.game_delay_code = 3
                self.score_on = 0


class KivyGameApp(App):
   pass
   
if __name__ == '__main__':
     
    KivyGameApp().run()
    