import pygame


class Button:

    def __init__(self,info):
        self.size = self.w, self.h = self.weight, self.height = info[0]
        self.pos = self.x,self.y = [int(i) for i in info[1]]
        self.action=info[2]
        self.rect=pygame.Rect(self.pos,self.size)

    def getmidx(self):
        return self.x+(self.w/2)

    def setmidx(self,value):
        self.x=value-(self.w/2)

    def getmidy(self):
        return self.y + (self.h / 2)

    def setmidy(self, value):
        self.y = value - (self.h / 2)

    centery = property(getmidy, setmidy)
    centerx = property(getmidx, setmidx)


class Newbutton:

    def __init__(self,*args):
        self.rect,self.kind,self.text,self.textimage=None,None,None,None
        keys=["rect","kind","text","textimage","color"]

        self.__dict__.update(dict(zip(keys,args)))



