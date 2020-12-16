from plugins.utils import *

class main:
    lvl = 2
    triggers = ['boss']
    need_bosses = True
    def execute(self, cmd):
        if state.get("boss") and len(cmd.params) == 1:
            vk_say("Активный босс удален", cmd.peer)
            cmd.ab.id = 0
            state.switch("boss")
        else:
            if len(cmd.params) >=2 and cmd.params[1].isdigit():
                if int(cmd.params[1]) in cmd.add and cmd.add[int(cmd.params[1])]:
                    addr = cmd.add[int(cmd.params[1])]
                    cmd.ab.id       = addr[0]
                    cmd.ab.name     = addr[1]
                    cmd.ab.hp       = addr[2]
                    cmd.ab.get_dmg  = addr[3]
                    vk_say(f"Активирован босс {cmd.ab.name}.", cmd.peer)
                    if not state.get("boss"): state.switch("boss")
                else:vk_say("Ошибка: Не найдено босса с ID "+cmd.params[1], cmd.peer)
            else: vk_say("Подсказка: /boss [id босса]", cmd.peer)
        
