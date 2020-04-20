import pygame
from Button import Button

def makefont(size):
    return pygame.font.Font(pygame.font.match_font("ubuntumono", bold=True), size)


def makebutton(pos,size,action):
    return Button([size,pos,action])
