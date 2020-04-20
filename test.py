from time import strftime
from subprocess import check_output as chk
from subprocess import Popen
from sys import argv

if len(argv)!=2:
    print("Clipnote only accepts 'new' or an integer as an argument.")

if argv[1]=="new":

    timestring = strftime(format("Clipnote_%A_%d._%B_%Y_%H:%M:%S"))

    with open("/home/jopeha/notes/"+timestring,"w") as file:
        file.writelines(i+"\n" for i in str(chk(["xclip","-o"]))[2:-1].split("\\n"))

    Popen(["gedit","/home/jopeha/notes/"+timestring])

else:
    note = int(argv[1])

    with open("/home/jopeha/notes/note{}.txt".format(note),"a") as file:
        file.writelines(i + "\n" for i in str(chk(["xclip", "-o"]))[2:-1].split("\\n"))

    Popen(["gedit","/home/jopeha/notes/note{}.txt".format(note)])
