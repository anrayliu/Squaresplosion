import pygame
import functions
from sys import exit
from player import Player
from pickle import dump,load
from game import Game 
from intro import Intro 
from menus import MainMenu,SettingsMenu,MusicMenu,ConfirmQuit,Pause,ConfirmReset
from time import time
from dead import Dead
from math import ceil

class Window(): #Pygame display and holds event data, as well as handling game states
    def __init__(self):
        #self.id=1
        self.surface=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.w=self.surface.get_width()
        self.h=self.surface.get_height()
        self.clock=pygame.time.Clock()
        self.VERSION="v1.0.0"
        pygame.display.set_caption("Squaresplosion")
        self.icon_surface=pygame.image.load("graphics/icon.png")
        pygame.display.set_icon(self.icon_surface)
                
        self.selected_song=None #Music variables
        self.playing=None
        self.my_songs=load(open("save1.p","rb"))[0]
        self.volume=load(open("save1.p","rb"))[4]
        pygame.mixer.music.set_volume(ceil(self.volume)/100)
        pygame.mixer.set_num_channels(20)
        self.switch=load(open("save1.p","rb"))[7]
        
        self.new_update=load(open("save1.p","rb"))[6] #Menu variables
        
        self.sounds=load(open("save1.p","rb"))[3] #Settings variables
        self.show_fps=load(open("save1.p","rb"))[2]
        self.keyboard=load(open("save1.p","rb"))[8]
        if self.keyboard=="WASD":
            self.up=pygame.K_w
            self.right=pygame.K_d
            self.left=pygame.K_a
        else:
            self.up=pygame.K_UP
            self.right=pygame.K_RIGHT
            self.left=pygame.K_LEFT
        
        self.show_cursor=0 #Intro variables
        
        self.chest_time=load(open("save1.p","rb"))[5] #Chest variables
        
        self.camerax=0 #Game variables
        self.cameray=0
        self.camera_center=1
        self.cursor_image="cursor"
        self.highscore=load(open("save1.p","rb"))[1]
        self.shakex=0
        self.shakey=0
        self.explosion=pygame.Surface((self.w,self.h),pygame.SRCALPHA)
        self.explosion.fill(pygame.Color("white"))
        self.alpha=0
        self.can_move=1
        
        self.player=Player(self)
        self.locations={"game":Game(self),
                        "intro":Intro(self),
                        "menu":MainMenu(self),
                        "settings":SettingsMenu(self),
                        "quit":ConfirmQuit(self), 
                        "reset":ConfirmReset(self), 
                        "pause":Pause(self), 
                        "dead":Dead(self), 
                        "music":MusicMenu(self)}                        
        self.can_escape=1
        self.transitionx=self.w
        self.close=None
        self.run=None

    def get_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.quit()
                
        pygame.mouse.set_visible(False)
        self.x,self.y=pygame.mouse.get_pos()
        self.cursor_rect=pygame.Rect(self.x,self.y,5,5)
        self.click=pygame.mouse.get_pressed()[0]
        self.keys=pygame.key.get_pressed()
        
        if self.keyboard=="WASD":
            self.up=pygame.K_w
            self.right=pygame.K_d
            self.left=pygame.K_a
        else:
            self.up=pygame.K_UP
            self.right=pygame.K_RIGHT
            self.left=pygame.K_LEFT
            
        if self.keys[pygame.K_ESCAPE]:
            self.escape_pressed=1
        else:
            self.escape_pressed=0
        self.clock.tick(60)
        
        if self.click==0:
            self.can_click=1
        if self.escape_pressed==0:
            self.can_escape=1
            
        if self.locations["music"].running==0 and self.locations["game"].running==0 and self.locations["intro"].running==0 and self.locations["pause"].running==0:
            if self.playing==None and self.run!="music":
                functions.play_song("menu music1")
            
    def update_screen(self):
        if self.click==1:
            self.can_click=0
            
        if self.alpha>0:
            self.explosion.set_alpha(self.alpha)
            self.surface.blit(self.explosion,(0,0))
            self.alpha-=5
            
        self.transitionx+=200
        pygame.draw.rect(self.surface,pygame.Color("black"),(self.transitionx,0,self.w,self.h))
        if self.transitionx>=0 and self.transitionx<=400:
            self.locations[self.close].running=0
            self.locations[self.run].run()

        if self.show_cursor==1:
            functions.draw(self.cursor_image,self.x,self.y)

        pygame.display.update()
        
    def quit(self):
        self.save()
        exit()
        
    def execute(self,location):
        self.save()
        self.can_escape=0
        self.locations[location].run()
        
    def save(self):
        dump([self.my_songs,self.highscore,self.show_fps,self.sounds,self.volume,self.chest_time,"null",self.switch,self.keyboard],open("save1.p","wb"))
    
    def reset_save(self):
        dump([[],0,0,1,100,time()+30,"update",3,"WASD"],open("save1.p","wb"))
        
    def transition(self,location,current_location):
        self.transitionx=-self.w
        self.close=current_location
        self.run=location
        if self.can_escape==1:
            functions.play_sound("transition")
'''
pygame.init()
object=Window()
object.reset_save()'''