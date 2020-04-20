import pygame
import itertools

class App:

    size=w,h=int(1920/2),int(1080/2)

    with open("letter keys", "r") as file:
        letters = file.read().split(":")

    letters = [i.split("\n") for i in letters]
    keys=[i[0] for i in letters]
    keycodes=[i[1] for i in letters]
    letters=[i[2:] for i in letters]
    keybook=dict(zip(keys,letters))
    keytocode=dict(zip(keys,keycodes))
    consonants=["sh","s","w","t","d","w","m","n","r","b","s","z","l","p","h","k","'","thw","j","wh","st","f"]

    vowels=["a","u","o","i","e","y","ao","ua"]

    both=["an","al","at","ab","an","ak","ar","al","om","ek"]

    consonants+=both
    vowels+=both

    def __init__(self,text):

        pygame.init()
        self.display=pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self.running=True
        self.clock=pygame.time.Clock()
        self.tick=self.clock.tick
        self.image=self.build(text)

    def run(self):
        while self.running:
            self.tick(6)
            self.event()

    def event(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
#            elif event.type == pygame.KEYUP:
#                if event.key == pygame.K_
                

    def build(self,text):
        self.length=len(text)

        self.totalw = 5
        self.tw = (self.w * 0.8) / self.length
        self.th = self.tw * 2

        font=makefont(self.tw)
        self.display.blit(font.render(text,True,pygame.Color("blue")),(0,0))

        for key in self.keys:
            while True:
                if key in text:
                    text=text.replace(key,self.keycodes[self.keys.index(key)]+"|",1)
                else:
                    break

        rect=self.display.get_rect()

        drawtext=text.split("|")[:-1]


        image=pygame.Surface((self.tw*len(drawtext)*1.1,self.th))

        vowels = [self.keytocode[i] for i in self.vowels]
        consonants = [self.keytocode[i] for i in self.consonants]



        for pos,code in enumerate(drawtext):
            self.adjh=0

            if pos>0:
                if drawtext[pos-1]=="?":
                    if code in vowels:
                        self.totalw-=self.tw
                        self.draw("3",image)
                        self.totalw+=self.tw
                elif drawtext[pos-1] in consonants and code in vowels:
                    self.totalw-=self.tw*0.2
                elif drawtext[pos-1]==code:
                    self.totalw-=self.tw
                    self.totalw -= self.tw * 0.2
                    self.adjh=self.th/3

            self.draw(code,self.display)
            self.totalw+=self.tw+self.tw*0.2

        pygame.display.flip()

    def draw(self,letter,image):

        pointlist=[]

        for i in range(10):
            for y_pos, row in enumerate(self.letters[self.keycodes.index(letter)]):
                for x_pos, point in enumerate(row):
                    try:
                        if int(point) == i:
                            pointlist.append([self.totalw + self.w * 0.025 + x_pos * (self.tw / 2), self.display.get_rect().centery + self.adjh - (self.th / 2) + y_pos * (self.th / 6)])
                    except Exception:
                        pass
        if len(pointlist)>1:
            pygame.draw.aalines(image, pygame.Color("red"), False, pointlist)


#    def splittit(self,input):

#        for string in input:




def makefont(size):
    return pygame.font.Font(pygame.font.match_font("ubuntumono", bold=True), int(size))

word="hello i am a meme"


app=App(word.replace(" ","-").lower().replace(".","-"))

app.run()




