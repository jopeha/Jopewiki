import pygame
import configparser
from tools import makefont,makebutton
from Button import Newbutton


class Mousemenu:

    def __init__(self,app,pos):

        self.app=app

        pos=pos[0]-3,pos[1]-3

        config=configparser.ConfigParser()
        config.read("conf/mousemenus")

        self.buttons=[ config[self.app.focus.__class__.__name__][button] for button in  config[self.app.focus.__class__.__name__]]

        width=(max(len(i) for i in self.buttons)*16)+10
        height=len(self.buttons)*40
        self.rect = pygame.Rect(pos, (width, height))
        self.pos=self.x,self.y=self.rect.topleft
        self.size=self.w,self.h=self.rect.size

        for pos,button in enumerate(self.buttons):
            self.buttons[pos]=makebutton((0,self.y+(40*pos)),(width,40),button)
            self.buttons[pos].rect.centerx=self.rect.centerx


        print("Instance of "+self.__class__.__name__+" created.")

    def update(self):

        if not self== self.app.focus:
            self.app.menus.remove(self)
            return self.close()


        pygame.draw.rect(self.app._display_surf,pygame.Color("gray"),self.rect)
        font=makefont(30)
        for button in self.buttons:
            self.app._display_surf.blit(font.render(button.action,True,pygame.Color("black")),button.rect)


    def click(self,pos):
        if self.buttons[int((pos[1]-self.y+1)/40)].action == "Create new stationary item":
            self.app.menus.append(ItemMenu(self.app,pos=pos))
            self.app.menus.remove(self)


    def close(self):
        self.__dict__={}

class ItemMenu:

    def __init__(self,app,pos=None):

        self.app=app
        self.rect=self.app.viewer.rect
        self.x,self.y=self.size=self.rect.topleft
        self.w,self.h=self.size=self.rect.size


        self.name=""
        self.tags=[]
        self.type=""
        self.resources={"population":"","none":""}
        self.text={"population":"","none":""}
        self.pos=pos
        self.unit=self.app.viewer.w / 24

        self.buttons=self.makeelements()
        self.writing=False


    def makeelements(self):


        font=makefont(18)
        fontb=makefont(36)
        unit = self.unit
        display=self.app._display_surf

        buttons=[]

        rect=pygame.Rect(unit,-24,unit,unit)

        for pos,i in enumerate(self.resources):


            rect=pygame.Rect(unit,unit+(unit+24)*pos,unit*2,unit/2)
            textimage=font.render(i,True,pygame.Color("Black"))
            textrect=textimage.get_rect()
            textrect.centerx=rect.centerx
            textrect.bottom=rect.top
            buttons.append(Newbutton(rect,"resource",i,textimage))

        rect = pygame.Rect((rect.x, rect.bottom + 24), (unit,unit))
        rect.centerx=buttons[-1].rect.centerx
        buttons.append(Newbutton(rect, "add", "resource",fontb.render("+", True, pygame.Color("Black"))))

        rect = pygame.Rect(unit*4, -24, unit, unit)

        for pos, i in enumerate(self.text):
            rect = pygame.Rect((unit*4), unit + (unit*2 + 24) * pos, unit*4, unit*2)
            textimage = font.render(i, True, pygame.Color("Black"))
            textrect = textimage.get_rect()
            textrect.centerx = rect.centerx
            textrect.bottom = rect.top
            buttons.append(Newbutton(rect, "text", i,textimage))

        rect = pygame.Rect((rect.x, rect.bottom + 24), (unit,unit))
        rect.centerx=buttons[-1].rect.centerx
        buttons.append(Newbutton(rect, "add", "text",fontb.render("+", True, pygame.Color("Black"))))

        return buttons



    def update(self):




        pygame.draw.rect(self.app._display_surf,pygame.Color("Gray"),self.rect)

        unit=self.unit
        font=makefont(18)

        display = self.app._display_surf
        color2=pygame.Color("dimgray")

        for i in self.buttons:
            if i.kind=="resource":
                pygame.draw.rect(display,color2,i.rect)
                textrect=i.textimage.get_rect()
                textrect.centerx=i.rect.centerx
                textrect.bottom=i.rect.top-3
                display.blit(i.textimage,textrect)
            if i.kind=="text":
                pygame.draw.rect(display, color2, i.rect)
                textrect = i.textimage.get_rect()
                textrect.centerx = i.rect.centerx
                textrect.bottom = i.rect.top - 3
                display.blit(i.textimage, textrect)
        for i in self.buttons:
            if i.kind=="add":
                pygame.draw.rect(display,color2,i.rect)
                textrect = i.textimage.get_rect()
                textrect.center = i.rect.center
                display.blit(i.textimage, textrect)


        if self.writing:
            rect=pygame.Rect(0,0,self.app.w/3,self.app.w/4)
            self.rect.center=self.app.center
            pygame.draw.rect(display,color2,rect)


    def click(self,pos):

        for i in self.buttons:
            if i.rect.x<pos[0]<i.rect.right and i.rect.y<pos[1]<i.rect.bottom:
                pass


