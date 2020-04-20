import configparser
import os

class World:

    def __init__(self):

        pass

    def load(self,save_name):
        config=configparser.ConfigParser()


        config.read("saves/"+save_name)

        self.__dict__.update(config["main"])

        self.items=[ self.itemload("saves/"+save_name.capitalize()+"/"+i) for i in os.listdir("saves/"+save_name.capitalize())]

    def itemload(self,save_name):
        config=configparser.ConfigParser()

        config.read(save_name)

        book=dict(config["main"])

        return World.MapItem(tuple(book["pos"].split(",")),book["name"],book["type"],book["tags"].split(","))

    class MapItem:

        def __init__(self,*args):


            self.pos=self.x,self.y=(int(i) for i in args[0])
            self.name=args[1]
            self.type=args[2]
            self.tags=list(args[2:])
            self.fontsize=18
            print(self.__dict__)


        def __repr__(self):
            return str(self.name)+". "+str(self.type)+" at "+str(self.pos)
