import random as rd
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from objects.asteroids import Asteroid1
from objects.unitfactory import Units
from objects.gameutils import GameTimeScore
from objects.gameutils import KeepScale as ks


class KivyGame(Widget):
    '''
    main program
    '''
    
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
        self.aster_reload = 1
        self.player1_health = 3
        self.info1 = ''
        self.aster_list = []
        
        #buttons scale factors [left, right
        #, height
        self.buttons = [4, 1.333, 50]
        
        #initiate all widgets and start board
        self.initiate_widgets()
        self.start_board_on()
        
        #motion run
        Clock.schedule_interval(self.update, 1.0 / 100)
       
       
    #====motion handler====
    def update(self, dt):
        
        #check player destroyed
        self.player_destroyed()
        
        #labels update state
        self.lb1.text = '{0}{1}'.format('Score: ', self.score)
        self.lb2.text = self.info1
        self.lb3.text = '{0}{1}'.format('Best score: ', self.best_score)
        self.lb4.text = '{0}{1}'.format('Level: ', self.game_level)
        self.lb5.text = '{0}{1}'.format('Energy: ', self.player1.health)
        
        #game clock update
        self.game_clock = GameTimeScore.gameclk_add(self.game_clock_on, self.game_clock)
        
        #score update
        self.score = GameTimeScore.score_add( self.score_on,  self.score, self.game_clock)
        
        #timeline update
        self.timeline(self.game_clock, self.game_level)
        
        #time delay update
        self.game_time_delay()
       
        #moving
        self.lev_backgr1.moving(self.lev_backgr1a.pos[1])
        self.lev_backgr1a.moving(self.lev_backgr1.pos[1])
        
        [globals()[n].moving(self.aster_reload) for n in self.aster_list]
        
        to_move = [
        self.player1, self.enemy1,
        self.enemy2, self.boss1,
        self.boss2, self.shoot1,
        self.shoot2, self.shoot3
        ]
        [n.moving() for n in to_move]
        
        #enemy shooting
        self.shoot2.aimed_shooting(self.player1, self.enemy1)
        self.shoot3.random_shooting(self.enemy2, self.game_clock)
        self.shoot2.random_shooting(self.boss1, self.game_clock)
        self.shoot3.random_shooting(self.boss1, (self.game_clock + ks.mov_sc(50)))
        self.shoot2.aimed_shooting(self.player1, self.boss2)
        self.shoot3.random_shooting(self.boss2, (self.game_clock))
               
        #collision checking
        for n in self.aster_list:
            self.expl2.object_collision(self.player1, globals()[n])
            self.expl2.object_collision(globals()[n], self.shoot1)
            
        obj_coll = [
            (self.player1, self.shoot2),
            (self.player1, self.shoot3),
            (self.enemy1, self.shoot1),
            (self.enemy2, self.shoot1),
            (self.boss1, self.shoot1),
            (self.boss2, self.shoot1)
            ]
        [self.expl2.object_collision(n[0],n[1]) for n in obj_coll]
        
        #health check
        checkheal_list = [
             self.player1, self.enemy1,
             self.enemy2, self.boss1,
             self.boss2
             ]
             
        for m in checkheal_list:
            self.score = self.expl1.check_health(m, self.score)
    
        for n in self.aster_list:
            self.score = self.expl1.check_health(globals()[n], self.score)
        
        #explosion expand
        self.expl2.small_explosion_expand()
        self.expl1.big_explosion_expand()
                   
                   
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
            self.player1.acc = Vector(-1, 0)
                     
        #shoot button
        if ks.partof_ww(self.buttons[1]) > self.v1[0] > ks.partof_ww(self.buttons[0]) and self.shoot1.pos[1] > ks.multip_wh(1.2):
            self.shoot1.shoot(self.player1)
            
       #right button
        if self.v1[0]>ks.partof_ww(self.buttons[1]):
             self.player1.acc = Vector(1, 0)
                                            
    #buttons up
    def on_touch_up(self, touch):
        self.player1.stop()
    
    
    def game_start(self):
        '''
        delay
        '''
        self.game_clock_on = 0
        self.score_on = 0
        self.game_clock = 0
        self.remove_start_board()
        self.player1_health = self.player1.health
        self.remove_widgets()
        self.initiate_widgets()
        self.game_clock_on = 1
        self.score_on = 1
        self.game_level += 1
        self.game_delay = 0
        self.game_delay_code = 0
        
        for_stop = [
            self.player1, self.enemy1,
            self.enemy2, self.boss1,
            self.boss2, self.shoot1,
            self.shoot2, self.shoot3
                ]
        [n.stop() for n in for_stop]
        
        self.lev_backgr1.start()
        self.lev_backgr1a.start()
    
    
    def player_destroyed(self):
        if self.player1.health<=0 and self.game_delay==0:
            self.info1 = "GAME OVER"
            self.lb2.set_pos('center1')
            self.game_delay_code = 1
            self.game_delay = 1
            self.player1.health = 0
            self.score_on = 0
                
                
    def game_time_delay(self):

        if self.game_delay>0:
            self.game_delay += 1
            
            if self.game_delay_code==1 and self.game_delay>ks.mov_sc(230):
                
                self.game_delay = 0
                self.game_delay_code = 0
                self.player_loose()
                
            if self.game_delay_code==2 and self.game_delay>ks.mov_sc(230):
                
                self.game_delay = 0
                self.game_delay_code = 0
                self.level_finnish()
                
            if self.game_delay_code==3 and self.game_delay>ks.mov_sc(230):
                
                self.game_delay = 0
                self.game_delay_code = 0
                self.win_game()
            
            
    def level_finnish(self):
        '''
        lev
        '''
        self.info1 = "Tap to continue."
        self.score_on = 0
        self.score = self.score + 30
        self.start_wait =1
        self.player1.health +=1
        
        
    def win_game(self):
        self.player_loose()
               
               
    def player_loose(self):
        '''
        loose
        '''
        self.score_on = 0
        self.game_level=0
        self.game_clock_on = 0
        self.game_clock = 0
        if self.best_score < self.score:
            self.best_score = self.score
        self.score = 0
        self.lb2.park()
        self.ship_health = 3
        self.player1.health = 3
        self.start_board_on()
        self.start_wait =1
   
    
    def start_board_on(self):
        
        self.remove_widget(self.lb2)
        self.start_board1 = self.units.build_unit('startboard')
        self.add_widget(self.start_board1)
        self.add_widget(self.lb2)
        self.info1 = "Tap to START"
        self.lb2.set_pos('center1')
                
                
    def remove_start_board(self):
         self.remove_widget(self.start_board1)
         self.lb2.park()
    
    
    def aster_generator(self, num, min_size, max_size):
        self.aster_list = []
        for n in range(num):
            globals()['aster%s' % n] = Asteroid1(ks.to_wh(min_size), ks.to_wh(max_size))
            name = ('aster%s' % n)
            self.aster_list.append(name)
    
    
    def aster_vel_upd(self, v_min, v_max):
        
        for n in self.aster_list:
            globals()[n].vel[1] = -rd.randint(ks.mov_sc(v_min), ks.mov_sc(v_max))
    
    
    def aster_impl(self, num, v_min, v_max, min_size, max_size):
        
        [self.remove_widget(globals()[n]) for n in self.aster_list]
            
        add_remove = [ self.expl1, self.expl2, self.lb1, self.lb2, self.lb3, self.lb4, self.lb5]
        [self.remove_widget(w) for w in add_remove]
        
        self.aster_generator(num, min_size, max_size)
        [self.add_widget(globals()[n]) for n in self.aster_list]
            
        self.aster_vel_upd(v_min, v_max)
        self.aster_reload = 1
        [self.add_widget(w) for w in add_remove]
                          
                
    #===timeline===
    def timeline(self, t, gl):
        
        #level1
        if gl==1:
            
            if t==ks.mov_sc(100):
                self.aster_impl(
                    7, 6, 7, 7, 15
                    )
                
            if t==ks.mov_sc(1800):
                self.aster_reload = 0
                     
            if t==ks.mov_sc(2400):
                self.aster_impl(
                    9, 6, 7, 7, 16
                    )
                              
            if t==ks.mov_sc(4000):
                self.aster_vel_upd(7, 8)
                               
            if t==ks.mov_sc(6000):
                self.aster_reload = 0
                
            if t==ks.mov_sc(6400):
                self.score_on = 0
                self.lb2.set_pos('center1')
                self.info1 = "Level 1 complete!"
                
            if t==ks.mov_sc(6630):
                self.level_finnish()
                
       #level2
        if gl==2:
                 
            if t==ks.mov_sc(100):
               self.enemy1.start_move(ks.mov_sc(2),0)
               
            if t==ks.mov_sc(1000):
               self.enemy2.start_move(ks.mov_sc(-4),0)
               
            if t==ks.mov_sc(5200):
               self.enemy1.start_move(0,ks.mov_sc(4))
               self.enemy2.start_move(0,ks.mov_sc(4))
               self.enemy1.reload = 0
               self.enemy2.reload = 0
                         
            if t==ks.mov_sc(5600) and self.player1.health > 0:
                self.score_on = 0
                self.lb2.set_pos('center1')
                self.info1 = "Level 2 complete!"
                
            if t==ks.mov_sc(5830) and self.player1.health > 0:
                self.level_finnish()
                
        #level3 
        if gl==3:
            
            if t==ks.mov_sc(100):
                self.aster_impl(
                    9, 7, 9, 9, 20
                    )
                
            if t==ks.mov_sc(3300):
                self.aster_reload = 0
                
            if t==ks.mov_sc(3500):
                self.enemy1.reload = 1
                self.enemy2.reload = 1
                self.enemy1.start_move(ks.mov_sc(3), 0)
                self.enemy2.start_move(ks.mov_sc(-5),0)
                
            if t==ks.mov_sc(4600):
               self.enemy1.start_move(0, ks.mov_sc(4))
               self.enemy2.start_move(0, ks.mov_sc(4))
               self.enemy1.reload = 0
               self.enemy2.reload = 0
               
            if t==ks.mov_sc(5200):
                self.boss1.start_move(ks.mov_sc(-4),0)
            
            if t>ks.mov_sc(5200) and self.boss1.health <=0:
                self.lb2.set_pos('center1')
                self.info1 = "Level 3 complete!"
                self.game_delay_code = 2
                self.game_delay = 1
                self.boss1.health = 1
                
        #level4
        if gl==4:
            
            if t==ks.mov_sc(100):
                self.aster_impl(
                    4, 6, 8, 7, 22
                    )
                
            if t==ks.mov_sc(200):
                self.enemy1.reload = 1
                self.enemy2.reload = 1
                self.enemy1.start_move(ks.mov_sc(3),0)
                self.enemy2.start_move(ks.mov_sc(-5),0)
                
            if t==ks.mov_sc(6400):
                self.enemy1.start_move(0, ks.mov_sc(4))
                self.enemy2.start_move(0, ks.mov_sc(4))
                self.enemy1.reload = 0
                self.enemy2.reload = 0
            
            if t==ks.mov_sc(6600):
                self.aster_reload = 0
                
            if t==ks.mov_sc(6800):
                self.score_on = 0
                self.lb2.set_pos('center1')
                self.info1 = "Level 4 complete!"
                
            if t==ks.mov_sc(7100):
                self.level_finnish()
        
        #level 5
        if gl==5:
            
            if t==ks.mov_sc(100):
                
                self.boss2.start_move(ks.mov_sc(6),0)
                
            if t>ks.mov_sc(100) and self.boss2.health<=0:
                self.lb2.set_pos('center1')
                self.info1 = "Congratulations!!! You win the game."
                self.game_delay_code = 3
                self.game_delay = 1
                self.boss2.health = 1
                                   
                                   
    #====all widgets linitiate====
    def initiate_widgets(self):
        
        #background initiate
        back = 'backgrlev'
        gl = self.game_level + 1
        name_1 = '{0}{1}'.format(back, gl)
        name_2 = '{0}{1}{2}'.format(back, gl, 'a')
        self.lev_backgr1 = self.units.build_unit(name_1)
        self.lev_backgr1a = self.units.build_unit(name_2)

        #shoots initiate
        self.shoot1 = self.units.build_unit('shootplayer')
        self.shoot2 = self.units.build_unit('shootenemy')
        self.shoot3 = self.units.build_unit('shootenemy')
        
        #units initiate                
        self.player1 = self.units.build_unit('player1')
        self.player1.health = self.player1_health
        self.enemy1 = self.units.build_unit('enemy1')
        self.enemy2 = self.units.build_unit('enemy2')
        self.boss1 = self.units.build_unit('boss1')
        self.boss2 = self.units.build_unit('boss2')
        
        #asteroids initiate
        self.aster_generator(7, 7, 17)
        
        #explosions initiate
        self.expl1 = self.units.build_unit('explosion1', 1)
        self.expl2 = self.units.build_unit('explosion1', 2)
        
        #static elements initiate
        self.arr_left = self.units.build_unit('arrowleft', self.buttons)
        self.arr_right = self.units.build_unit('arrowright', self.buttons)
        self.sh_label = self.units.build_unit('shootlabel', self.buttons)
                       
        #Labels initiate
        self.lb1 = self.units.build_unit('lb')
        self.lb1.set_pos('lefttop4')
        self.lb2 = self.units.build_unit('lb')
        self.lb2.font_2()
        self.lb2.text_size[1] = 130
        self.lb3 = self.units.build_unit('lb')
        self.lb3.set_pos('lefttop1')
        self.lb4 = self.units.build_unit('lb')
        self.lb4.set_pos('lefttop2')
        self.lb5 = self.units.build_unit('lb')
        self.lb5.set_pos('lefttop3')
        
        #add all widgets
        widgets_to_add1 = [
            self.lev_backgr1,
            self.lev_backgr1a,
            ]
        [self.add_widget(n) for n in widgets_to_add1]
        
        [self.add_widget(globals()[n]) for n in self.aster_list]
        
        widgets_to_add2 = [
            self.shoot1,
            self.shoot2, self.shoot3,
            self.player1,self.enemy1,
            self.enemy2, self.boss1,
            self.boss2, self.expl2,
            self.expl1,
            self.arr_right, self.sh_label,
            self.arr_left,
            self.lb1, self.lb2, self.lb3,
            self.lb4, self.lb5
            ]
        [self.add_widget(n) for n in widgets_to_add2]
        
    
    def remove_widgets(self):
        
        widgets_to_remove = [
            self.lev_backgr1,
            self.lev_backgr1a,
            self.shoot1, self.shoot2,
            self.shoot3, self.player1,
            self.enemy1, self.enemy2,
            self.boss1, self.boss2,
            self.expl1, self.expl2,
            self.arr_right, self.sh_label,
            self.arr_left,
            self.lb1, self.lb2, self.lb3,
            self.lb4, self.lb5, [m for m in self.aster_list]
            ]
        [self.remove_widget(n) for n in widgets_to_remove]
        

class KivyGameApp(App):
   pass
   
if __name__ == '__main__':
     
    KivyGameApp().run()
    