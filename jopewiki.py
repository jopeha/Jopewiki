import pygame
from PIL import Image
import configparser
from Applet import Navbar,Box,Viewer
from World import World



class App:

    def __init__(self,window_size,savename):
        """Take window size as an argument."""

        self.world=World()
        self.world.load(savename)

        self.size=self.w,self.h=self.width,self.height=window_size

        # initialise pygame, display surface and all the applets

        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.nav=Navbar(self)
        self.box=Box(self)
        self.viewer=Viewer(self)
        self.sub_apps=[self.nav,self.box,self.viewer]

        # If running is false, the game stops. Lastpage stores the last page. Clock is initialised

        self.running=True
        self.clock=pygame.time.Clock()
        self.lastpage=None
        self.focus=self.box
        self.menus=[]

    def event(self):

        # Gathers events and calls the appropriate functions


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            for app in self.menus:
                if app.x<pygame.mouse.get_pos()[0]<app.x+app.w and app.y<pygame.mouse.get_pos()[1]<app.y+app.h:
                    self.focus=app
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button==1:
                            app.click(event.pos)

                        elif event.button==3:
                            app.click2(event.pos)
                    break


            else:
                for app in self.sub_apps:
                    if app.x<pygame.mouse.get_pos()[0]<app.x+app.w and app.y<pygame.mouse.get_pos()[1]<app.y+app.h:
                        self.focus=app
                        if event.type == pygame.MOUSEBUTTONUP:
                            if event.button==1:
                                app.click(event.pos)
                                break
                            elif event.button==3:
                                app.click2(event.pos)
                                break

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    self.focus.scroll("up")
                elif event.key==pygame.K_DOWN:
                    self.focus.scroll("down")
                elif event.key == pygame.K_LEFT:
                    self.focus.scroll("left")
                elif event.key == pygame.K_RIGHT:
                    self.focus.scroll("right")

                elif event.key==pygame.K_PLUS:
                    self.viewer.zoom("+")
                elif  event.key==pygame.K_MINUS:
                    self.viewer.zoom("-")

    def update(self):

        # Gets called every loop. Ticks, calls applets' updates and flips

        self.clock.tick(12)
        for app in self.sub_apps+self.menus:
            app.update()

        pygame.display.flip()

    def navigate(self,button):

        # Gets called when a button is pressed

        if button=="<<" and self.lastpage!=None:
            pass
        elif button=="X":
            self.quit()
        elif button=="menu":
            self.menu()

        elif button=="+":
            self.focus.zoom("+")
        elif button=="-":
            self.focus.zoom("-")

        elif button=="Create new stationary item":
            pass


    def quit(self):
        self.running=False


app=App((1920,1080),"goty")
while app.running:
    app.event()
    app.update()



pygame.quit()