from plugins.utils import *
import os

class main:
    lvl = 2
    triggers = ['restart', 'рестарт']
    def execute(self, cmd):
        vk_say("Перезагружаюсь..", cmd.peer)
        open("restart.txt", "w").write(str(cmd.peer))
        log("Рестарт <= ВК")
        os._exit(0)