from plugins.utils import *

class main:
    lvl = 0
    triggers = ['bosshp']
    need_bosses = True
    def execute(self, cmd):
        if state.get("boss"):
            vk_say(f"У босса {cmd.ab.name} осталось {cmd.ab.hp} ХП.", cmd.peer)
        else: vk_say("Нет активного босса.", cmd.peer)