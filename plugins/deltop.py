from plugins.utils import *

class main:
    lvl = 2
    triggers = ['racedel', 'wardel']

    def execute(self, cmd):
        if 'race' in cmd.cmd:
            del races[:]
            vk_say("Статистика заездов сброшена", cmd.peer)
        if 'war' in cmd.cmd:
            del wars[:]
            vk_say("Статистика сражений сброшена", cmd.peer)