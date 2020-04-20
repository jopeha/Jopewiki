import pygame
from tools import makefont
from Button import Button
from Menu import Mousemenu
import configparser


class Applet:

    """base class for all applets"""

    def __init__(self,size,pos):

        # essentially takes in a rect of the applet

        self.rect=pygame.Rect(pos,size)

        self.size = self.w, self.h = self.weight, self.height = self.rect.size
        self.pos = self.x,self.y = self.rect.x,self.rect.y
        self.centery,self.centerx=self.rect.centery,self.rect.centerx


    def click(self,pos):

        """Sees if a click is on a button and calls navigate with the button"""

        for button in self.buttons:
            if not button==None:
                if button.x<pos[0]<button.x+button.w and button.y<pos[1]<button.y+button.h:

                    return self.app.navigate(button.action)

    def click2(self,pos):
        pass

    def scroll(self,dir):
        pass

    def zoom(self,dir):
        pass

class Navbar(Applet):

    """Acts as a navigation bar in the bottom of the screen"""

    def __init__(self,app):

        # A relative size is set, meaning what part of the screen it will take. Other applets will scale with the height
        # of navbar rel_h=10 would mean it takes a tenth of the screens height. The entire width is always taken.

        self.app=app
        self.rel_h=rel_h=15
        size=self.app.w,self.app.h/rel_h
        pos=0,self.app.h-size[1]


        # Makes the buttons. DOES NOT WORK WITH DIFFERENT BUTTON AMOUNTS

        buttons=["<<",">>","menu","X",]
        self.buttons = [Button(((self.app.w/(len(buttons)+1),self.app.h/rel_h),(((self.app.w/4)*pos)+(1/40*self.app.w),self.app.h*((rel_h-1)/rel_h)),i)) for pos, i in enumerate(buttons)]
        Applet.__init__(self,size,pos)




    def update(self):

        """Draws a rectangle as the bacground of the bar and then buttons with text on top"""

        rect=pygame.Rect(self.pos,self.size)
        color=pygame.Color("gray")
        buttoncolor=pygame.Color("dimgray")
        pygame.draw.rect(self.app._display_surf,color,rect)

        for button in self.buttons:
            pygame.draw.rect(self.app._display_surf,buttoncolor,pygame.Rect(button.x,button.y,button.w,button.h))
            font = makefont(18)
            text_image = font.render(button.action, True, pygame.Color("black"))
            textrect = text_image.get_rect()
            textrect.centerx=button.centerx
            textrect.centery=button.centery
            self.app._display_surf.blit(text_image,textrect)

class Box(Applet):

    def __init__(self,app):

        # Sets the relative size. 4 will fill a quarter of the screen

        self.rel_w=rel_w=4


        self.config=configparser.ConfigParser()
        self.config.read("conf/none.info")
        Applet.__init__(self,(app.w/rel_w,app.h-app.nav.h),(app.w*((rel_w-1)/rel_w),0))
        self.main_image=pygame.image.load("skull2.jpg")




        self.app=app
        self.shelf=pygame.Rect(self.pos,(self.w,self.h*3))
        self.buttons=[None]



    def update(self):

        color = pygame.Color("gray")

        self.app._display_surf.set_clip(self.rect)



        pygame.draw.rect(self.app._display_surf, color, self.shelf)
        self.picrect=self.main_image.get_rect()
        self.picrect.centerx,self.picrect.centery=self.rect.centerx,self.y+self.rect.w/2
        self.app._display_surf.blit(self.main_image,self.picrect)

        self.updateitems()

        self.app._display_surf.set_clip()

    def updateitems(self):

        color = pygame.Color("slategray")
        rect= pygame.Rect(0,0,self.w*0.9,30)
        rect.centerx,rect.y=self.rect.centerx,self.picrect.bottom+20
        pygame.draw.rect(self.app._display_surf,color,rect)

        font = makefont(18)
        text_image = font.render(self.config["main"]["title"], True, pygame.Color("black"))
        textrect = text_image.get_rect()
        textrect.centerx = rect.centerx
        textrect.centery = rect.centery
        self.app._display_surf.blit(text_image, textrect)

        for section in self.config["resources"]:
            pass


        for section in self.config["text"]:
            text_image= font.render(section, True, pygame.Color("black"))
            textrect = text_image.get_rect()
            textrect.centerx = rect.centerx
            textrect.centery = rect.centery+30
            self.app._display_surf.blit(text_image, textrect)
            rows=[]
            text=""

            for word in self.config["text"][section].split(" "):
                if len(text+word+" ")>(self.w*0.9)/9:
                    rows.append(text)
                    text=word+" "
                else:
                    text+=word+" "
            rows.append(text)

            rect=pygame.Rect(rect.x,textrect.y+25,self.w*0.9,(len(rows)*14)+10)
            pygame.draw.rect(self.app._display_surf,color,rect)
            for row in rows:

                self.app._display_surf.blit(font.render(row, True, pygame.Color("black")),rect)
                rect.y+=14
    def open(self,boxname):

        self.config=configparser.ConfigParser()
        self.config.read("saves/"+self.app.world.name.capitalize()+"/"+boxname)




    def scroll(self,dir):
        if dir=="up":
            if self.y<0:self.y+=10
        elif dir=="down":
            self.y -= 10

class Viewer(Applet):

    def __init__(self, app):

        self.config = configparser.ConfigParser()
        self.config.read("boxes/none.box")
        Applet.__init__(self, (app.w-app.box.w, app.h - app.nav.h), (0,0))
        self.app = app

        self.buttons = [ Button([(40, 40),(self.w - 50, 10), "+"]), Button([(40, 40),(self.w - 50, 60), "-"])]
        self.image=pygame.image.load("map_borders.png")
        self.scale=self.w/self.image.get_rect().w
        self.pany,self.panx=0,0
        self.world=self.app.world
        self.visible=["city"]

    def update(self):

        self.app._display_surf.set_clip(self.rect)
        self.app._display_surf.fill(pygame.Color("#13305c"))
        self.app._display_surf.blit(pygame.transform.scale(self.image,self.scaled().size),self.scaled())


        for button in self.buttons:
            pygame.draw.rect(self.app._display_surf,pygame.Color("gray"),button.rect)

            font = makefont(36)
            text_image = font.render(button.action, True, pygame.Color("black"))
            textrect = text_image.get_rect()
            textrect.centerx = button.centerx
            textrect.centery = button.centery
            self.app._display_surf.blit(text_image, textrect)



        for item in self.world.items:
            if any(i in item.tags for i in self.visible):
                x,y=(item.x+self.scaled().x),(item.y+self.scaled().y)
                pygame.draw.polygon(self.app._display_surf,pygame.Color("gray"),
                                    [(x-5,y-10),(x+5,y-10),(x,y)])
                font=makefont(item.fontsize)

                w=len(item.name)*item.fontsize/2
                rect=pygame.Rect(0,0,w+6,item.fontsize+6)
                rect.centerx=x
                rect.bottom=y-10
                text_image=font.render(item.name,True,pygame.Color("black"))
                textrect=text_image.get_rect()
                textrect.center=rect.center

                pygame.draw.rect(self.app._display_surf,pygame.Color("gray"),rect)
                self.app._display_surf.blit(text_image,textrect)



        self.app._display_surf.set_clip()


    def zoom(self,dir):
        if dir=="+" and self.scale<12:
            self.scale*=1.1
        elif dir=="-" and self.scale>1:
            self.scale/=1.1

    def scaled(self):
        rect= pygame.Rect(0,0,self.image.get_rect().w*self.scale,self.image.get_rect().h*self.scale)
        rect.centerx,rect.centery=self.rect.centerx+self.panx, self.rect.centery+self.pany
        return rect

    def scroll(self,dir):
        pan=(self.w + self.h) / 40
        if dir=="left":
            self.panx-=pan
        elif dir=="right":
            self.panx+=pan
        elif dir=="down":
            self.pany+=pan
        elif dir=="up":
            self.pany-=pan
    def click2(self,pos):
        self.app.menus.append(Mousemenu(self.app,pos))
        self.app.focus=self.app.menus[-1]

    def click(self,pos):
        for item in self.world.items:
            if any(i in item.tags for i in self.visible):
                w,h = (len(item.name)*item.fontsize)+6,item.fontsize+6
                x, y = (item.x + self.scaled().x-(w/2)), (item.y + self.scaled().y-10-h)
                if x<pos[0]<x+w and y<pos[1]<y+h:
                    return self.app.box.open(item.name)
        super().click(pos)
