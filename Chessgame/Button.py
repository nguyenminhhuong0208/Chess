import pygame as p
import webbrowser
import os as os

current_dir = os.path.dirname(__file__)
class Button:
    def __init__(self, name, position, size):
        self.name = name
        self.position = position
        self.size = size

    # load, transform and display button on the screen
    def displayButton(self, screen):  
        image = p.image.load(os.path.join(current_dir,"images", self.name+".png"))
        image = p.transform.scale(image,self.size)
        screen.blit(image, self.position)
    
    # check if mouse on button 
    def isMouseOnText(self):
        (x, y) = p.mouse.get_pos()
        if (self.position[0] <= x <= self.position[0] + self.size[0]) and (self.position[1] <= y <= self.position[1] + self.size[1]):
             return True
        else:
             return False
        
    # big image when the mouse is hovering on 
    def handleHover(self, screen):
        if self.isMouseOnText() == True:
            image = p.image.load(os.path.join(current_dir,"images", self.name+".png"))
            bigSize = (self.size[0] * 1.1, self.size[1] * 1.1)
            image = p.transform.scale(image,bigSize)
            screen.blit(image, self.position)
        
    # check if click 
    def handleClick(self, events):
        for event in events:
            if event.type == p.MOUSEBUTTONUP:
                return True
        return False

    # open link when button is clicked
    def open(self, link):
        webbrowser.open(link)