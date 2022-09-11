import pygame
from os import listdir
from math import ceil,floor
from random import randint,choice,uniform

def init(window):
    init.window=window

    file=open("sizes.txt","r")
    sizes=[]
    init.images={}
    for line in file:
        sizes.append(tuple(line.split(" ")))
    file.close()
        
    for image in listdir("graphics"):
        if image[-4:]==".png":
            image_object=pygame.image.load("graphics/{}".format(image)).convert_alpha()
            found_size=0
            for size in sizes:
                image_name=size[0]   #Adds the elements before the last two (sizes) together to form the name
                for i in range(len(size)-3):
                    image_name+=" {}".format(size[i+1])
                
                if image_name==image[:-4]:  #If the name matches an image listed, it will try to assign it the given size
                    try:                    #If failed it will assume w or h is listed
                        init.images[image[:-4]]=pygame.transform.scale(image_object,(int(size[len(size)-2]),int(size[len(size)-1])))
                    except:
                        try:
                            init.images[image[:-4]]=pygame.transform.scale(image_object,(int(size[len(size)-2]),int(init.window.h)))  #Assumes that there is only 1 w or h
                        except:
                            init.images[image[:-4]]=pygame.transform.scale(image_object,(int(init.window.w),int(init.window.h)))
                    found_size=1
            if found_size==0:
                init.images[image[:-4]]=image_object   #If no sizes are found no resizings happen
            
    init.sounds={}
    for sound in listdir("sound effects"):
        init.sounds[sound[:-4]]=pygame.mixer.Sound("sound effects/{}".format(sound))

    init.font1_sizes=[]
    for i in range(100):
        init.font1_sizes.append(pygame.font.Font("font1.otf",(i+1)*5))
        
    init.font2_sizes=[]
    for i in range(100):
        init.font2_sizes.append(pygame.font.Font("font2.ttf",(i+1)*5))

    init.intro_font=pygame.font.Font("font3.ttf",80)
        
    init.alpha_surfaces={}                #test for bullet trails
    for i in range(ceil(255/20)):
        init.alpha_surfaces[str(255-i*20)]=pygame.Surface((init.window.w,init.window.h),pygame.SRCALPHA)
        init.alpha_surfaces[str(255-i*20)].set_alpha(255-i*20)
        
    init.test=pygame.Surface((init.window.w,init.window.h),pygame.SRCALPHA)

def rounded_rectangle(x,y,w,h,r,colour="black",center=0,rect=0,return_info=0):
    colour=pygame.Color(colour)
    if isinstance(rect,pygame.Rect):
        x=rect[0]
        y=rect[1]
        w=rect[2]
        h=rect[3]
    if center=="x":
        x=init.window.w/2-w/2+x
    elif center=="y":
        y=init.window.h/2-h/2+y
    elif center=="middle":
        x=init.window.w/2-w/2+x
        y=init.window.h/2-h/2+y
    elif center=="right":
        x=init.window.w-w+x
    elif isinstance(center,pygame.Rect):
        x=center[0]+center[2]/2-w/2+x
        y=center[1]+center[3]/2-h/2+y

    pygame.draw.ellipse(init.window.surface,colour,(x,y,r,r))
    pygame.draw.ellipse(init.window.surface,colour,(x+w-r,y,r,r))
    pygame.draw.ellipse(init.window.surface,colour,(x,y+h-r,r,r))
    pygame.draw.ellipse(init.window.surface,colour,(x+w-r,y+h-r,r,r))

    pygame.draw.rect(init.window.surface,colour,(x+r/2,y,w-r,r))
    pygame.draw.rect(init.window.surface,colour,(x+r/2,y+h-r/2-r/2,w-r,r))
    pygame.draw.rect(init.window.surface,colour,(x,y+r/2,r,h-r))
    pygame.draw.rect(init.window.surface,colour,(x+w-r,y+r/2,r,h-r))

    pygame.draw.rect(init.window.surface,colour,(x+r/2,y+r/2,w-r,h-r))

    if return_info==1:
        return (x,y,w,h)

def write(string,x,y,size,colour=pygame.Color("white"),center=0,return_info=0,alpha=255,font="font1",write=1):
    if font=="font1":
        text=init.font1_sizes[int(size/5)-1].render(str(string),False,colour)
    elif font=="font2":
        text=init.font2_sizes[int(size/5)-1].render(str(string),False,colour)
    else:
        text=init.intro_font.render(str(string),False,colour)
    text.set_alpha(alpha)
    if isinstance(center,pygame.Rect):
        x=center[0]+center[2]/2-text.get_width()/2+x
        y=center[1]+center[3]/2-text.get_height()/2+y
    elif center=="middle":
        x=init.window.w/2-text.get_width()/2+x
        y=init.window.h/2-text.get_height()/2+y
    elif center=="x":
        x=init.window.w/2-text.get_width()/2+x
    elif center=="y":
        y=init.window.h/2-text.get_height()/2+y
    elif center=="right":
        x=init.window.w-text.get_width()+x
        
    if write==1:
        init.window.surface.blit(text,(x,y))
    if return_info==1:
        return (text.get_width(),text.get_height())

def draw(picture,x,y,center=0,angle=None,size=None):
    image=init.images[picture]
    if size!=None:
        image=pygame.transform.scale(image,(floor(size[0]),floor(size[1])))
    if isinstance(center,pygame.Rect):
        x,y=(center[0]+center[2]/2-image.get_width()/2+x,center[1]+center[3]/2-image.get_height()/2+y)
    elif center=="middle":
        x=init.window.w/2-image.get_width()/2
        y=init.window.h/2-image.get_height()/2

    if angle==None:
        init.window.surface.blit(image,(x,y))
    else:
        rotated=pygame.transform.rotate(image,angle)
        rect=rotated.get_rect(center=(x,y))
        init.window.surface.blit(rotated,(rect.x,rect.y))

def play_song(song,loop=-1):
    init.window.playing=song
    pygame.mixer.music.load("music\{}.wav".format(song))
    pygame.mixer.music.play(loop)

def play_sound(sound):
    if init.window.sounds==1:
        init.sounds[sound].play()
'''
class Button():
    def __init__(self,x,y,w,h,r,text,colour="black",display="text"):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text
        self.r=r
        self.colour=colour
        self.display=display
        self.click=0

    def draw(self):
        if self.hover==1:
            rounded_rectangle(0,0,0,0,self.r,rect=self.rect,colour=pygame.Color("yellow green"))
        else:
            rounded_rectangle(0,0,0,0,self.r,rect=self.rect,colour=pygame.Color(self.colour))
        if self.display=="text":
            write(self.text,0,0,40,center=self.rect)
        else:
            draw(self.text,0,0,center=self.rect)
        
    def update(self):
        if self.rect.colliderect(init.window.cursor_rect):
            self.hover=1
            if init.window.click==1 and init.window.can_click==1:
                self.click=1
            else:
                self.click=0
        else:
            self.hover=0'''
            
            
class Button():
    def __init__(self,x,y,w,h,r,text,colour="black",display="text"):
        self.rect=pygame.Rect(x,y,w,h)
        self.text=text
        self.r=r
        self.original_colour=colour
        self.colourr=self.original_colour
        self.display=display
        self.select=0
        self.text_colour="white"

    def update(self):
        if init.window.click==1 and init.window.can_click==1 and self.rect.colliderect(init.window.cursor_rect):
            self.click=1
        else:
            self.click=0
        
        if self.rect.colliderect(init.window.cursor_rect):
            self.colourr=pygame.Color("yellow green")
            if self.select==0:
                play_sound("select")
            self.select=1
        else:
            self.colourr=pygame.Color(self.original_colour)
            self.select=0
        
    def draw(self):
        rounded_rectangle(0,0,0,0,self.r,rect=self.rect,colour=pygame.Color(self.colourr))
        if self.display=="text":
            write(self.text,0,0,40,center=self.rect,colour=pygame.Color(self.text_colour))
        else:
            draw(self.text,0,0,center=self.rect)
            
def parallax(y,w,speed,scroll,picture):
    for i in range(abs(floor(scroll/w))+4):
        draw(picture,scroll/speed+i*w-init.window.camerax+init.window.shakex,y-init.window.cameray+init.window.shakey)
    for i in range(abs(floor(scroll/w))+4):
        draw(picture,scroll/speed-i*w-init.window.camerax+init.window.shakex,y-init.window.cameray+init.window.shakey)
        
def random(a,b):
    if isinstance(a,float):
        return uniform(a,b)
    else:
        return randint(round(a),round(b))
    
def contains(element,list):
    for i in list:
        if i==element:
            return 1
    return 0
    
def toggle(variable,toggle1=1,toggle2=0):
    if variable==toggle1:
        return toggle2
    elif variable==toggle2:
        return toggle1
        
def draw_all(tuple):
    for list in tuple:
        for element in list:
            element.draw()
            
def random_from(random_values):
    list=[]
    for value in random_values:
        list.append(value)
    return choice(list)