import pygame
import functions
from window import Window
       
def run():
    pygame.init()
    window=Window()
    functions.init(window) #passes window class to functions
    window.execute("intro")
    
if __name__=="__main__":
    run()