import pygame
import functions
from bullet import Bullet
from enemies import Exploding,Flying,Laser,Tank
from particles import CircleParticle,DebrisParticle,ShellParticle,Rain,ShotParticle,LineParticle
from math import atan2,degrees
from defeated import DefeatedExploding,DefeatedFlying
from bomb import Bomb,Missile
from time import time

class Game():
    def __init__(self,window):
        self.window=window
        self.running=0
        self.reset=1 #reset variables
        self.lag_timer=0
        
    def update(self):         #Gameplay is calculated without scroll, then the scroll value is added when drawing
        self.window.camerax=self.window.x-self.window.w/2
        self.window.cameray=self.window.y-self.window.h/2
        
        if self.window.keys[pygame.K_SPACE]:
            self.window.player.hp=0
        
        self.window.camerax-=self.window.camerax*self.window.camera_center #camera offset
        self.window.cameray-=self.window.cameray*self.window.camera_center
        
        self.window.shakex*=-self.shake_cooldown
        self.window.shakey*=-self.shake_cooldown
        
        if self.intro==1 or self.outro==1:
            self.window.can_move=0
        else:
            self.window.can_move=1
        
        if self.intro==1: #-----------------------------------------INTRO--------------
            if round(self.window.player.y)==0:
                if self.fall_timer==0:
                    functions.play_sound("ground shake")
                if self.fall_timer==0:
                    self.window.shakex=10*functions.random_from((-1,1))
                    self.window.shakey=10*functions.random_from((-1,1))
                self.fall_timer+=1/60
                if self.fall_timer>3.5:
                    self.window.show_cursor=1
                    functions.play_sound("cock")
                    self.regen_timer=0
                    self.show_weapon=1
                    self.fire_timer=0
                    
                    self.shake_cooldown=0.8
                    self.intro=0
        elif self.outro==1: #-------------------------------------OUTRO--------------------
            self.border_height*=1.05
            if self.border_height>200:
                self.border_height=200
            self.window.camera_center*=1.05
            if self.window.camera_center>1:
                self.window.camera_center=1
            self.outro_timer+=1/60
            if self.outro_timer>3 and self.show_player==1:
                self.show_player=0
                self.window.shakex=100*functions.random_from((-1,1))
                self.window.shakey=100*functions.random_from((-1,1))
                functions.play_sound("dead explosion")
                for i in range(200):
                    self.particles.append(DebrisParticle(self.window.w/2+functions.random(-15,15),self.window.h*0.6+functions.random(-70,0),self.window,(-100.0,-80.0),(0.1,0.3),10,"blue",3))
            if self.outro_timer>8:
                self.running=0
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                self.window.playing=None
                self.window.execute("dead")
        else:
            self.border_height*=0.9
            self.window.camera_center*=0.95    
                
        self.window.player.update()
        
        if self.regen_timer>=255:
            self.window.player.hp+=1
            if self.window.player.hp>=255:
                self.window.player.hp=255
        else:
            self.regen_timer+=0.2
        
        if self.window.switch!="Never" and self.window.my_songs!=[]: #-------MUSIC--------------------
            self.song_timer+=1/60
            if self.song_timer>self.window.switch*60:
                self.playing+=1
                if self.playing>len(self.window.my_songs)-1:
                    self.playing=0
                functions.play_song(self.window.my_songs[self.playing])
                self.song_timer=0
        
        self.fire_timer+=1/60 #------------------------------------FIRING------------------
        if self.window.click==1 and self.fire_timer>0.15:
            self.fire_timer=0
            functions.play_sound("gunshot")
            self.window.bullets_shot+=1
            self.bullets.append(Bullet(self.window,self.enemies))
            if self.bullets[len(self.bullets)-1].can_hit==0: #Only way for can_hit to be 0 before updating is if it hit an enemy
                self.particles.append(CircleParticle(self.bullets[len(self.bullets)-1].x,self.bullets[len(self.bullets)-1].y,self.window,(5,10),(5,10)))
                for i in range(functions.random(10,15)):
                    if self.bullets[len(self.bullets)-1].enemy_hit.type=="exploding":
                        self.particles.append(DebrisParticle(self.bullets[len(self.bullets)-1].x,self.bullets[len(self.bullets)-1].y,self.window,(-210,30),(0.4,0.4),10,"red",2))
                    elif self.bullets[len(self.bullets)-1].enemy_hit.type=="flying":
                        self.particles.append(DebrisParticle(self.bullets[len(self.bullets)-1].x,self.bullets[len(self.bullets)-1].y,self.window,(-210,30),(0.4,0.4),10,"yellow",2))
                    elif self.bullets[len(self.bullets)-1].enemy_hit.type=="tank":
                        self.particles.append(DebrisParticle(self.bullets[len(self.bullets)-1].x,self.bullets[len(self.bullets)-1].y,self.window,(-210,30),(0.4,0.4),10,"purple",2))
                        self.particles.append(LineParticle(self.bullets[len(self.bullets)-1].x,self.bullets[len(self.bullets)-1].y,self.window,(0,360),(20,40),(5,15),"white",(5,15)))
                self.window.shakex=8*functions.random_from((-1,1))
                self.window.shakey=8*functions.random_from((-1,1))
                
            self.particles.append(ShellParticle(self.window))
            self.particles.append(ShotParticle(self.window))



        self.strength_timer+=1/60
        if self.strength_timer>6*(1+self.window.strength/4):
            self.strength_timer=0
            self.window.strength+=0.1
            if self.window.strength>1.5 and len(self.spawn_options)==1:
                self.spawn_options.append("flying")
            if self.window.strength>2 and len(self.spawn_options)==2:
                self.spawn_options.append("tank")
            if self.window.strength>2.5 and len(self.spawn_options)==3:
                self.spawn_options.append("laser")
            if self.window.strength>4:
                self.window.strength=4
            self.spawn_speed-=0.1
            if self.spawn_speed<0.4:
                self.spawn_speed=0.4
            
        self.enemy_timer+=1/60 #-----------------------------------SPAWNING----------------
        if self.enemy_timer>self.spawn_speed:
            spawn=functions.random_from(self.spawn_options)
            if spawn=="exploding":
                self.enemies.append(Exploding(self.window))
            elif spawn=="flying":
                self.enemies.append(Flying(self.window))
            elif spawn=="laser":
                self.enemies.append(Laser(self.window))
            elif spawn=="tank":
                self.enemies.append(Tank(self.window))
            self.enemy_timer=0
            #self.window.id+=1
            
        #for alpha in functions.init.alpha_surfaces:
            #functions.init.alpha_surfaces[alpha].fill(0)
            
        for number,enemy in enumerate(self.enemies): #------------ENEMIES-------------------
            enemy.update()
            if enemy.explode==1:
                del self.enemies[number]
                self.window.alpha=150
                self.window.shakex=100*functions.random_from((-1,1))
                self.window.shakey=100*functions.random_from((-1,1))
                self.regen_timer=0
                functions.play_sound("heavy explosion2")
                for i in range(10):
                    self.particles.append(DebrisParticle(enemy.x,enemy.y,self.window,(-100.0,-80.0),(0.1,0.3),10,"blue",3))
                self.window.player.hp-=enemy.explode_damage
                if self.window.player.hp<0:
                    self.window.player.hp=0
            if enemy.type=="flying":
                if enemy.fire_timer>2.5:
                    self.enemy_bombs.append(Bomb(enemy.x,enemy.y,self.window))
                    enemy.fire_timer=0
            if enemy.hp<=0:
                del self.enemies[number]
                if enemy.type=="exploding":
                    self.window.red_shot+=1
                    self.defeated_enemies.append(DefeatedExploding(enemy.x,enemy.y,self.window))
                elif enemy.type=="flying":
                    self.window.yellow_shot+=1
                    self.defeated_enemies.append(DefeatedFlying(enemy.x,enemy.y,self.window))
                elif enemy.type=="laser":
                    self.window.laser_shot+=1
                    self.enemy_bombs.append(Missile(enemy.x,enemy.y,self.window))
                    self.enemy_bombs[len(self.enemy_bombs)-1].direction="left"
                    self.enemy_bombs.append(Missile(enemy.x,enemy.y,self.window))
                    self.enemy_bombs[len(self.enemy_bombs)-1].direction="right"
                    self.defeated_enemies.append(DefeatedExploding(enemy.x,enemy.y,self.window,"laser"))
                    functions.play_sound("laser explosion")
                elif enemy.type=="tank":
                    self.window.tank_shot+=1
                    self.defeated_enemies.append(DefeatedExploding(enemy.x,enemy.y,self.window,"tank"))
            
        for number,bullet in enumerate(self.bullets): #-----------BULLETS-------------------
            bullet.update()
            if bullet.alpha<0:
                del self.bullets[number]
            if bullet.can_hit==1:
                if bullet.y>self.window.h*0.6:
                    self.particles.append(CircleParticle(bullet.x,bullet.y,self.window,(10,20),(10,20)))
                    for i in range(functions.random(5,10)):
                        self.particles.append(DebrisParticle(bullet.x,bullet.y,self.window,(-210,30),(0.4,0.4),10,"white",3))
                    self.window.shakex=8*functions.random_from((-1,1))
                    self.window.shakey=8*functions.random_from((-1,1))
                    bullet.can_hit=0
                    for i in range(functions.random(1,3)):
                        self.particles.append(DebrisParticle(bullet.x,bullet.y,self.window,(-120,-60),(0.2,0.2),10,"gray",5))
                        
        self.firing=0 #For muzzle flash
        for number,particle in enumerate(self.particles): #----------PARTICLES--------------
            particle.update()
            if particle.type=="circle":
                if particle.stroke_size==1:
                    del self.particles[number]
            elif particle.type=="debris" or particle.type=="shell":
                if particle.y>self.window.h*2:
                    del self.particles[number]
            elif particle.type=="shot":
                self.firing=1
                if particle.life_time==0:
                    del self.particles[number]
            elif particle.type=="line":
                if particle.thickness<=0 or particle.length<=0:
                    del self.particles[number]
                     #------------------------OTHER----------------
                    
        for i in self.rain:
            i.update()
            
        for i,o in enumerate(self.defeated_enemies):
            o.update()
            if o.x<self.window.w*-2 or o.x>self.window.w*2 or o.y>self.window.h*2 or o.y<self.window.h*-2:
                del self.defeated_enemies[i]
                
        for i,o in enumerate(self.enemy_bombs): #----------------------BOMBS-----------------
            o.update()
            if o.rect.colliderect(self.window.player.rect):
                del self.enemy_bombs[i]
                if o.type=="bomb":
                    for i in range(3):
                        self.particles.append(CircleParticle(o.x,o.y,self.window,(15,30),(10,20)))
                    self.window.shakex=100*functions.random_from((-1,1))
                    self.window.shakey=100*functions.random_from((-1,1))
                    functions.play_sound("heavy explosion")
                    self.window.alpha=150
                    self.regen_timer=0
                    for i in range(10):
                        self.particles.append(DebrisParticle(enemy.x,enemy.y,self.window,(-100.0,-80.0),(0.1,0.3),10,"blue",3))
                    self.window.player.hp-=functions.random(40,60)
                    if self.window.player.hp<0:
                        self.window.player.hp=0
                elif o.type=="missile":
                    self.window.shakex=100*functions.random_from((-1,1))
                    self.window.shakey=100*functions.random_from((-1,1))
                    self.window.alpha=150
                    for i in range(10):
                        self.particles.append(DebrisParticle(o.x,o.y,self.window,(-100.0,-80.0),(0.1,0.3),10,"blue",3))
                    self.window.player.hp-=functions.random(50,70)
                    if self.window.player.hp<0:
                        self.window.player.hp=0
            if o.type=="bomb":
                if o.y>self.window.h*0.6:
                    del self.enemy_bombs[i]
                    for i in range(3):
                        self.particles.append(CircleParticle(o.x,o.y,self.window,(15,30),(10,20)))
                    for i in range(functions.random(15,20)):
                        self.particles.append(DebrisParticle(o.x,o.y,self.window,(-210,30),(0.4,0.4),10,"white",3))
                    self.window.shakex=100*functions.random_from((-1,1))
                    self.window.shakey=100*functions.random_from((-1,1))
                    functions.play_sound("heavy explosion")
            elif o.type=="missile":
                if o.x<self.window.w*-2 or o.x>self.window.w*2:
                    del self.enemy_bombs[i]
        
        self.right_ar_direction=degrees(atan2(self.window.h*0.6-70-self.window.player.y-self.window.y,self.window.x-self.window.w/2))
        self.left_ar_direction=degrees(atan2(self.window.h*0.6-70-self.window.player.y-self.window.y,self.window.x-self.window.w/2))+180
        if self.window.x>self.window.w/2:
            self.ar_sprite="ar right{}".format(self.firing)
            self.direction=self.right_ar_direction
        else:
            self.ar_sprite="ar left{}".format(self.firing)
            self.direction=self.left_ar_direction
            
        if self.window.player.hp==0 and self.outro==0:
            self.outro=1
            self.window.camera_center=0.01
            self.border_height=10
            self.bullets=[]
            self.particles=[]
            self.enemies=[]
            self.defeated_enemies=[]
            self.enemy_bombs=[]
            self.fire_timer=-100
            self.enemy_timer=-100
            self.window.show_cursor=0
            self.show_weapon=0
            
        if round(self.window.clock.get_fps())<=40:
            self.lag_timer=2
        self.lag_timer-=1/60
        
        self.thunder_timer+=1/60
        if self.thunder_timer>25:
            functions.play_sound(functions.random_from(("thunder","thunder2")))
            self.thunder_timer=0
            
    def draw(self):
        self.window.surface.fill((0,51,102))
        for i in self.stars:
            pygame.draw.rect(self.window.surface,pygame.Color("white"),(i[0]-self.window.camerax+self.window.shakex,i[1]-self.window.cameray+self.window.shakey,5,5))
        
        functions.parallax(self.window.h*0.25,800,4,self.window.player.x,"trees")
                    
        pygame.draw.rect(self.window.surface,(102,102,102),(0,self.window.h*0.6-self.window.cameray+self.window.shakey,self.window.w,self.window.h)) #Ground
        if self.show_player==1:
            self.window.player.draw()
            
        functions.parallax(self.window.h*0.7,800,2,self.window.player.x,"rocks")
        functions.parallax(self.window.h,800,1,self.window.player.x,"gray rocks")
            
        functions.draw_all((self.bullets,self.enemy_bombs,self.enemies))    
            
        if self.show_weapon==1:
            functions.draw(self.ar_sprite,self.window.w/2-self.window.camerax+self.window.shakex,self.window.h*0.6-70-self.window.cameray+self.window.shakey-self.window.player.y,angle=self.direction)

        functions.draw_all((self.defeated_enemies,self.particles,self.rain))
        
        if self.window.player.hp>0:
            functions.rounded_rectangle(self.window.w/2-510,50,1020,40,25,colour="gray")
            functions.rounded_rectangle(self.window.w/2-510,50,self.window.player.hp*4,40,25,colour=(0,0,self.window.player.hp))
            
            #functions.rounded_rectangle(self.window.w/2-510,110,1020,20,10,colour="black")
            #functions.rounded_rectangle(self.window.w/2-510,110,self.regen_timer*4,20,10,colour="yellow")
            
            pygame.draw.rect(self.window.surface,pygame.Color("black"),(self.window.w/2-510,110,1020,20))
            pygame.draw.rect(self.window.surface,pygame.Color("yellow"),(self.window.w/2-510,110,self.regen_timer*4,20))
            
        dimensions=functions.write(round(self.window.score*10),self.window.w*0.05,self.window.h-self.window.w*0.1,60,font="font2",return_info=1) #score
        pygame.draw.rect(self.window.surface,pygame.Color("white"),(self.window.w*0.05-10,self.window.h-self.window.w*0.1-5,dimensions[0]+15,dimensions[1]+10),3)
        
        pygame.draw.rect(self.window.surface,pygame.Color("black"),(0,0,self.window.w,self.border_height))  #cutscene borders
        pygame.draw.rect(self.window.surface,pygame.Color("black"),(0,self.window.h-self.border_height,self.window.w,self.border_height))
        
        if self.lag_timer>0:
            functions.write("Experiencing lag? Try configuring the settings.",0,self.window.h*0.85,40,center="x")
                    
        if self.window.show_fps==1:
            functions.write(round(self.window.clock.get_fps()),0,0,40,font="font1")

    def run(self):
        self.running=1
        self.window.cursor_image="crosshair"
        if self.reset==1:
            self.reset_var()
        self.reset=1
        pygame.mixer.unpause()
        if self.intro==1 or self.outro==1:
            self.window.show_cursor=0
        
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.running=0
                self.window.cursor_image="cursor"
                pygame.mixer.pause()
                self.window.execute("pause")
                
            self.update()
            self.draw()
            
            self.window.update_screen()
            
    def reset_var(self):
        #self.window.id=1
        self.window.score=0
        self.window.bullets_shot=0
        self.window.red_shot=0
        self.window.yellow_shot=0
        self.window.tank_shot=0
        self.window.laser_shot=0
        self.bullets=[]
        self.particles=[]
        self.stars=[]
        self.rain=[]
        self.regen_timer=0
        self.enemies=[]
        self.window.start_time=time()
        self.strength_timer=0
        self.spawn_options=["exploding"]
        self.spawn_speed=2.5
        self.window.strength=1
        self.window.player.hp=255
        self.defeated_enemies=[]
        self.enemy_bombs=[]
        self.playing=0 #playing [0] index from soundtracks
        self.fire_timer=-5 #Controls fire rate
        self.enemy_timer=-5 #Controls enemy spawn
        self.intro=1
        self.outro=0
        self.fall_timer=0
        self.outro_timer=0
        self.thunder_timer=0
        self.shake_cooldown=0.95
        self.show_weapon=0
        self.window.show_cursor=0
        self.show_player=1
        self.window.player.y=self.window.h
        self.window.player.y_vel=-10
        self.border_height=200 #Black borders top and bottom during intro
        self.window.camera_center=1 #1 fully centred 0 freestyle
        self.rain_channel=pygame.mixer.Channel(0)
        if self.window.sounds==1:
            self.rain_channel.play(pygame.mixer.Sound("sound effects/rain.wav"),loops=-1)
        self.song_timer=0
        
        self.y_change=functions.random(5,15)
        self.x_change=functions.random(-10,10)
        
        for i in range(500):
            self.rain.append(Rain(self.window,self.x_change,self.y_change))

            
        for i in range(80):
            self.stars.append((functions.random(self.window.w*-0.5,self.window.w*1.5),functions.random(self.window.h*-0.5,self.window.h*0.5)))
        if self.window.my_songs!=[]:
            functions.play_song(self.window.my_songs[self.playing])
        else:
            pygame.mixer.music.stop()
            self.window.playing=None