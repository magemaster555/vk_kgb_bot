from plugins.utils import *
import psutil, random, time

class main:
    triggers = ['status']
    lvl = 2
    def execute(self, cmd):
        stat = "[СТАТИСТИКА]:\n"
        stat += "Бот активен "+str(int(time.time()-starttime))+" сек.\n"
        stat += "Процессор: "+str(int(psutil.cpu_percent()))+"%\n"
        stat += "Память: "+str(int(psutil.virtual_memory()[2]))+"%"
        vk_say(stat,cmd.peer)