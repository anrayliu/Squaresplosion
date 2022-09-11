import pygame
import functions
from songs import SongButton
from visualizer import Visualizer
from random import shuffle
from math import ceil,sin
from chest import Chest
from sys import exit

class MainMenu():
    def __init__(self,window):
        self.window=window
        self.play_button=functions.Button(self.window.w/2-100,self.window.h*0.55,200,100,50,"Play")
        self.settings_button=functions.Button(self.window.w/2-100,self.window.h*0.7,200,100,50,"Settings")
        self.quit_button=functions.Button(self.window.w/2-100,self.window.h*0.85,200,100,50,"Quit")
        buttons(self.window)
        self.running=0
        #self.chest=Chest(self.window)
        self.timer=0 #for update popup
        self.show_updates=0
        self.update_popup=self.window.h
        self.close_button=functions.Button(430,self.update_popup+20,50,50,0,"close","red","draw")

    def update(self):
        self.play_button.update()
        if self.play_button.click==1:
            self.running=0
            self.show_updates=0
            self.window.execute("game")
            
        self.settings_button.update()
        if self.settings_button.click==1:
            self.show_updates=0
            self.window.transition("settings","menu")
            
        self.quit_button.update()
        if self.quit_button.click==1:
            self.window.quit()
        
        if self.show_updates==1:
            self.timer+=1/60
            if self.timer>1:
                self.update_popup-=10
                if self.update_popup<self.window.h*0.6:
                    self.update_popup=self.window.h*0.6
                    
            self.close_button.rect.y=self.update_popup+20
            self.close_button.update()
            if self.close_button.click==1:
                self.show_updates=0
                        
        #self.chest.update()
        self.popup_rect=pygame.Rect(0,self.update_popup,500,self.window.h*0.4)
        
    def draw(self):
        self.window.surface.fill(pygame.Color("black"))
        functions.draw("menu art",0,0)
        self.play_button.draw()
        self.settings_button.draw()
        self.quit_button.draw()
        self.text=functions.write("Square",self.window.w*0.5,self.window.h*0.1,120,colour=pygame.Color("blue"),return_info=1)
        self.text2=functions.write("splosion",self.window.w*0.5+self.text[0]+10,self.window.h*0.1,120,colour=pygame.Color("red"),return_info=1)
        for i in range(4):
            pygame.draw.rect(self.window.surface,pygame.Color("white"),(self.window.w*0.5+i*200,self.window.h*0.1+self.text[1]+20+i*20,self.text[0]+self.text2[0]-i*200,10))

        #self.chest.draw()
        
        if self.show_updates==1:
            pygame.draw.rect(self.window.surface,pygame.Color("gray"),self.popup_rect)
            pygame.draw.rect(self.window.surface,pygame.Color("black"),self.popup_rect,5)
            
            self.close_button.draw()
            
            if self.window.new_update=="update":
                if self.window.VERSION=="v1.0.0":
                    functions.write("Welcome to Squaresplosion!",0,-self.window.h*0.15,30,center=self.popup_rect)
                else:
                    functions.write("Here's what's new in {}!".format(self.window.VERSION),0,-self.window.h*0.15,30,center=self.popup_rect)
            else:
                functions.write("Welcome back!".format(self.window.VERSION),0,-self.window.h*0.15,30,center=self.popup_rect)
                functions.write("You're playing the first version".format(self.window.VERSION),0,-self.window.h*0.05,30,center=self.popup_rect)
                functions.write("of Squaresplosion, but stay".format(self.window.VERSION),0,0,30,center=self.popup_rect)
                functions.write("tuned for future updates!".format(self.window.VERSION),0,self.window.h*0.05,30,center=self.popup_rect)
        
    def run(self):
        self.running=1
        self.window.show_cursor=1
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.running=0
                self.show_updates=0
                self.window.execute("quit")
            self.update()
            self.draw()
            self.window.update_screen()
            
class SettingsMenu():
    def __init__(self,window):
        self.window=window
        self.music_button=functions.Button(self.window.w*0.1,self.window.h*0.4,200,100,50,"Playlist")
        self.fps_button=functions.Button(self.window.w*0.4,self.window.h*0.4,200,100,50,"FPS")
        self.sounds_button=functions.Button(self.window.w*0.7,self.window.h*0.4,200,100,50,"Sounds")
        self.reset_button=functions.Button(self.window.w*0.1,self.window.h*0.6,200,100,50,"Reset")
        self.keyboard_button=functions.Button(self.window.w*0.4,self.window.h*0.6,200,100,50,"QWERTY")
        self.running=0
        
    def update(self):
        self.music_button.update()
        if self.music_button.click==1:
            pygame.mixer.music.stop()
            self.window.playing=None
            self.window.transition("music","settings")
        
        self.fps_button.update()
        if self.window.show_fps==1:
            self.fps_button.text_colour="yellow"
        else:
            self.fps_button.text_colour="white"
        if self.fps_button.click==1:
            self.window.show_fps=functions.toggle(self.window.show_fps)
            
        self.sounds_button.update()
        if self.window.sounds==1:
            self.sounds_button.text_colour="yellow"
        else:
            self.sounds_button.text_colour="white"
        if self.sounds_button.click==1:
            self.window.sounds=functions.toggle(self.window.sounds)   
            
        self.reset_button.update()
        if self.reset_button.click==1:
            self.running=0
            self.window.execute("reset")
            
        self.keyboard_button.update()
        self.keyboard_button.text=self.window.keyboard
        if self.keyboard_button.click==1:
            self.window.keyboard=functions.toggle(self.window.keyboard,"WASD","Arrows")
        
        buttons.back_button.update()
        if buttons.back_button.click==1:
            self.window.transition("menu","settings")
        
    def draw(self):
        self.window.surface.fill(pygame.Color("gray"))
        self.music_button.draw()
        self.sounds_button.draw()
        self.fps_button.draw()
        self.reset_button.draw()
        self.keyboard_button.draw()
        buttons.back_button.draw()
    
    def run(self):
        self.running=1
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.running=0
                self.window.execute("menu")
            self.update()
            self.draw()
            self.window.update_screen()
            
class MusicMenu():
    def __init__(self,window):
        self.window=window
        self.timer=0
        self.running=0
        
        self.SONGS=["chill1","chill2","chill3","chill4","chill5","dubstep1","dubstep2","dubstep3","hiphop1","hiphop2"]
        
        self.add_button=functions.Button(self.window.w*0.25,self.window.h*0.9-100,200,100,50,"Add")
        self.remove_button=functions.Button(self.window.w*0.25,self.window.h*0.9-100,200,100,50,"Remove")
        self.play_button=functions.Button(self.window.w*0.45,self.window.h*0.9-100,200,100,50,"Play")
        self.stop_button=functions.Button(self.window.w*0.45,self.window.h*0.9-100,200,100,50,"Stop")
        self.clear_button=functions.Button(self.window.w*0.65,self.window.h*0.9-100,200,100,50,"Clear")
        self.random_button=functions.Button(self.window.w*0.65,self.window.h*0.4,200,100,50,"Randomize")
        self.add_all_button=functions.Button(self.window.w*0.65,self.window.h*0.6,200,100,50,"Add All")
        self.switch_button=functions.Button(self.window.w*0.65,self.window.h*0.2,200,100,50,self.window.switch)
                
        #self.song_buttons holds all buttons, and the list attribute differentiates them from my_songs and SONGS 
        #self.window.selected_song=(song,list)
        
        self.visualizer=Visualizer(self.window)
        
    def update(self):
        for number,button in enumerate(self.my_sb):
            button.y=self.window.h*0.1+number*50
            button.update()
        for button in self.all_sb: #sb=song buttons
            button.update()
            
        if self.window.selected_song!=None:
            if self.window.playing==self.window.selected_song[0]:
                self.stop_button.update()
                if self.stop_button.click==1:
                    pygame.mixer.music.stop()
                    self.window.playing=None
            else:
                self.play_button.update()
                if self.play_button.click==1:
                    functions.play_song(self.window.selected_song[0])
                    self.visualizer.read(self.window.selected_song[0])
                    self.visualizer.update() #updates once to load variables
                    self.timer=0
                    
            if self.window.selected_song[1]=="SONGS":
                self.add_button.update()
                if self.add_button.click==1:
                    if functions.contains(self.window.selected_song[0],self.window.my_songs)==0:
                        self.window.my_songs.append(self.window.selected_song[0])
                        self.my_sb.append(SongButton(self.window.selected_song[0],self.window.w*0.45,self.window.h*0.1+(len(self.window.my_songs)-1)*50,self.window,"my_songs"))
            else:
                self.remove_button.update()
                if self.remove_button.click==1:
                    self.window.my_songs.remove(self.window.selected_song[0])
                    for number,button in enumerate(self.my_sb):
                        if button.list=="my_songs" and button.song==self.window.selected_song[0]:
                            del self.my_sb[number]
                        
                            
        if len(self.window.my_songs)!=len(self.SONGS):
            self.add_all_button.update()
            if self.add_all_button.click==1:
                for song in self.SONGS:
                    if functions.contains(song,self.window.my_songs)==0:
                        self.window.my_songs.append(song)
                        self.my_sb.append(SongButton(song,self.window.w*0.45,self.window.h*0.1+(len(self.window.my_songs)-1)*50,self.window,"my_songs"))
                    
        if self.window.my_songs!=[]:
            self.clear_button.update()
            if self.clear_button.click==1:
                if self.window.selected_song!=None:
                    if self.window.selected_song[1]=="my_songs":
                        if self.window.selected_song[0]==self.window.playing:
                            self.window.playing=None
                            pygame.mixer.music.stop()
                        self.window.selected_song=None
                self.window.my_songs=[]
                self.my_sb=[]
            
            if self.window.switch=="Never":
                self.switch_button.text=self.window.switch
            else:
                self.switch_button.text="{}mins".format(self.window.switch)
                
            self.switch_button.update()
            if self.switch_button.click==1:
                if self.window.switch==10:
                    self.window.switch="Never"
                elif self.window.switch=="Never":
                    self.window.switch=1
                else:
                    self.window.switch+=1
            
            self.random_button.update()
            if self.random_button.click==1:
                shuffle(self.window.my_songs)
                self.my_sb=[]
                for song in self.window.my_songs:
                    self.my_sb.append(SongButton(song,self.window.w*0.45,self.window.h*0.1+(len(self.window.my_songs)-1)*50,self.window,"my_songs"))
                    
        buttons.back_button.update()
        if buttons.back_button.click==1:
            self.window.playing=None
            pygame.mixer.music.stop()
            self.window.transition("menu","music")
            
        self.slide_rect=pygame.Rect(self.window.w*0.15,self.window.h*0.3+4.5*self.window.volume,50,50)
        if self.window.click==1 and self.window.can_click==1 and self.window.cursor_rect.colliderect(self.slide_rect):
            self.difference=self.window.y-self.slide_rect.y
        if self.difference!=None:
            self.slide_rect.y=self.window.y-self.difference
            if self.slide_rect.y<self.window.h*0.3:
                self.slide_rect.y=self.window.h*0.3
            elif self.slide_rect.y>self.window.h*0.3+450:
                self.slide_rect.y=self.window.h*0.3+450
            self.window.volume=(self.slide_rect.y-self.window.h*0.3)/4.5
            pygame.mixer.music.set_volume(ceil(self.window.volume)/100)
            if self.window.click==0:
                self.difference=None
                    
    def draw(self):
        self.window.surface.fill(pygame.Color("green"))
        
        if self.window.playing!=None and self.window.playing!="menu music1":
            self.timer+=1
            if self.timer==6:
                self.visualizer.update()
                self.timer=0
            else:
                self.visualizer.draw()
        
        for button in self.my_sb:
            button.draw()
        for button in self.all_sb:
            button.draw()
            
        if self.window.selected_song!=None:
            if self.window.playing==self.window.selected_song[0]:
                self.stop_button.draw()
            else:
                self.play_button.draw()

            if self.window.selected_song[1]=="SONGS":
                self.add_button.draw()
            else:
                self.remove_button.draw()
                
        if self.window.my_songs!=[]:
            self.clear_button.draw()
            self.switch_button.draw()
            functions.write("Switch song every:",0,-100,40,center=self.switch_button.rect,colour="black")
            self.random_button.draw()
        
        if len(self.window.my_songs)!=len(self.SONGS):
            self.add_all_button.draw()
            
        buttons.back_button.draw()
        
        pygame.draw.rect(self.window.surface,pygame.Color("black"),(self.window.w*0.15,self.window.h*0.3,50,500))
        pygame.draw.rect(self.window.surface,pygame.Color("gray"),self.slide_rect)
        functions.write("{}%".format(ceil(self.window.volume)),self.window.w*0.05,self.window.h*0.3,40,font="font1")
                                        
    def run(self):
        self.running=1
        self.reset_songs()
        self.difference=None
        
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.window.playing=None
                self.running=0
                pygame.mixer.music.stop()
                self.window.execute("settings")
            self.update()
            self.draw()
            self.window.update_screen()
            
    def reset_songs(self):
        self.my_sb=[]  #my song buttons
        self.all_sb=[]  #options song buttons
        for number,song in enumerate(self.SONGS):
            self.all_sb.append(SongButton(song,self.window.w*0.25,self.window.h*0.1+number*50,self.window,"SONGS"))
        for song in self.window.my_songs:
            self.my_sb.append(SongButton(song,self.window.w*0.45,self.window.h*0.1+(len(self.window.my_songs)-1)*50,self.window,"my_songs"))

class ConfirmQuit():
    def __init__(self,window):
        self.window=window
        self.running=0
        self.yes_button=functions.Button(self.window.w/2+200,self.window.h*0.5,200,100,50,"Yes")
        self.no_button=functions.Button(self.window.w/2-400,self.window.h*0.5,200,100,50,"No")
        
        self.cover=pygame.Surface((self.window.w,self.window.h),pygame.SRCALPHA)
        self.cover.fill(pygame.Color("black"))
        self.cover.set_alpha(200)
        
    def update(self):
        self.yes_button.update()
        if self.yes_button.click==1:
            self.window.quit()
        
        self.no_button.update()
        if self.no_button.click==1:
            self.running=0
            self.window.execute("menu")
        
    def draw(self):
        self.window.locations["menu"].draw()
        self.window.surface.blit(self.cover,(0,0))
        functions.write("Are you sure you want to quit?",0,self.window.h*0.2,100,center="x")
        
        self.yes_button.draw()
        self.no_button.draw()
    
    def run(self):
        self.running=1
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.window.quit()
            self.update()
            self.draw()
            self.window.update_screen()
            
class ConfirmReset():
    def __init__(self,window):
        self.window=window
        self.running=0
        self.yes_button=functions.Button(self.window.w/2+200,self.window.h*0.5,200,100,50,"Yes")
        self.no_button=functions.Button(self.window.w/2-400,self.window.h*0.5,200,100,50,"No")
        
        self.cover=pygame.Surface((self.window.w,self.window.h),pygame.SRCALPHA)
        self.cover.fill(pygame.Color("black"))
        self.cover.set_alpha(150)
        
    def update(self):
        self.yes_button.update()
        if self.yes_button.click==1:
            self.window.reset_save()
            exit()
        
        self.no_button.update()
        if self.no_button.click==1:
            self.running=0
            self.window.execute("settings")
        
    def draw(self):
        self.window.locations["settings"].draw()
        self.window.surface.blit(self.cover,(0,0))
        functions.write("Are you sure you want to reset?",0,self.window.h*0.2,100,center="x")
        functions.write("This will close the game.",0,self.window.h*0.35,60,center="x")
        
        self.yes_button.draw()
        self.no_button.draw()
    
    def run(self):
        self.running=1
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.running=0
                self.window.execute("settings")
            self.update()
            self.draw()
            self.window.update_screen()

class Pause():
    def __init__(self,window):
        self.window=window
        self.running=0
        self.quit_button=functions.Button(self.window.w/2+200,self.window.h*0.5,200,100,50,"Quit")
        self.resume_button=functions.Button(self.window.w/2-400,self.window.h*0.5,200,100,50,"Resume")
        
        self.cover=pygame.Surface((self.window.w,self.window.h),pygame.SRCALPHA)
        self.cover.fill(pygame.Color("black"))
        self.cover.set_alpha(100)
        
    def update(self):
        self.quit_button.update()
        if self.quit_button.click==1:
            self.running=0
            pygame.mixer.stop()
            self.window.playing=None
            pygame.mixer.music.stop()
            self.window.cursor_image="cursor"
            self.window.execute("menu")
        
        self.resume_button.update()
        if self.resume_button.click==1:
            self.running=0
            self.window.locations["game"].reset=0
            self.window.execute("game")
        
    def draw(self):
        self.window.locations["game"].draw()
        self.window.surface.blit(self.cover,(0,0))
        functions.write("Paused",0,self.window.h*0.2,100,center="x")
        
        self.quit_button.draw()
        self.resume_button.draw()
    
    def run(self):
        self.running=1
        self.window.cursor_image="cursor"
        self.window.show_cursor=1
        while (self.running):
            self.window.get_events()
            if self.window.escape_pressed==1 and self.window.can_escape==1:
                self.running=0
                pygame.mixer.stop()
                self.window.playing=None
                pygame.mixer.music.stop()
                self.window.cursor_image="cursor"
                self.window.execute("menu")
            self.update()
            self.draw()
            self.window.update_screen()
            

            
def buttons(window):
    buttons.back_button=functions.Button(window.w*0.1,window.h*0.1,200,100,50,"Back")