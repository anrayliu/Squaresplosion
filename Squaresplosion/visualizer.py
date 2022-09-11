import pygame 
import functions
from scipy.fftpack import dct
from math import ceil 
from wave import open
from numpy import fromstring,short

class Visualizer():
    def __init__(self,window):
        self.window=window
        
    def draw(self):
        self.bars=[]
        for i in self.h:
            self.bars.append((self.window.w-i*20*ceil(self.window.volume)/100,len(self.bars)*30,i*20*ceil(self.window.volume)/100,30))
        for i in self.bars:
            pygame.draw.rect(self.window.surface,pygame.Color("white"),i)

    def read(self,song):
        self.song=open("music/{}.wav".format(song))
        self.params=self.song.getparams()
        self.nchannels,self.sampwidth,self.framerate,self.frames=self.params[:4]
        self.str_data=self.song.readframes(self.frames)
        self.song.close()
        self.wave_data=fromstring(self.str_data, dtype =short)
        self.wave_data.shape=-1,2
        self.wave_data=self.wave_data.T
        self.num=self.frames
        
    def update(self):
        self.num-=self.framerate/10
        if self.num>0:
            self.num=int(self.num)
            self.h=abs(dct(self.wave_data[0][self.frames-self.num:self.frames-self.num+ceil(self.window.h/30)]))
            self.h=[min(30,int(i**(1 / 2.5)*30/100)) for i in self.h]
            self.draw()
        else:
            self.num=self.frames
