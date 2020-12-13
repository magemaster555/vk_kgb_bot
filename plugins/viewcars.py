from plugins.utils import *

class main:
    triggers = ['vc', 'viewcars']
    lvl = 2
    need_cars = True
    need_warcars = True

    cars = {}

    def execute(self, cmd):
        if len(cmd.params) >= 2:
            if cmd.params[1].lower() in ["w", "d"]:
                tosay =  "Автомобили "+cmd.params[1]+"\n"

                if cmd.params[1].lower() == "w":
                    for id in cmd.warcars:
                        if cmd.warcars[id]:
                            tosay += f"{cmd.warcars[id].name}[{id}] -- dmg: {cmd.warcars[id].dmg}, hp: {cmd.warcars[id].hp}, exp_to: {cmd.warcars[id].exp_to_reach}\n"
                else:
                     for id in cmd.cars:
                        if cmd.cars[id]:
                            tosay += f"{cmd.cars[id].name}[{id}] -- win_prob: {cmd.cars[id].win_prob}, exp_to: {cmd.cars[id].exp_to_reach}\n"
                vk_say(tosay, cmd.peer)

            else: vk_say(f"Подсказка: /{cmd.cmd} [W - боевые | D - обычные]", cmd.peer)
        else: vk_say(f"Подсказка: /{cmd.cmd} [W - боевые | D - обычные]", cmd.peer)