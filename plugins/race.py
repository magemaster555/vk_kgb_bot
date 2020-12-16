from plugins.utils import *
import random, re

class main:
    lvl = 0
    triggers = ['race', 'raceid']
    need_cars = True
    need_attach = True
    need_users = True
    need_bosses = True
    cars = {}
    activeboss = None
    def execute(self, cmd):
        self.cars = cmd.cars
        if state.get("boss"):
            self.activeboss = cmd.ab
        isid = "id" in cmd.cmd
        if isid and cmd.by.admin_level != 2:
            vk_say(NO_ACCESS_TO_COMMAND, cmd.peer)
            return None
        if state.get("race") or isid:
            if isid:
                attach_user = 0
                if len(cmd.params) > 2:
                    found_id = re.findall(r"\[id(\d+)\|[@,*].+\]", cmd.params[2])
                    if len(found_id) == 1:
                        attach_user = int(found_id[0])
                    else:
                        vk_say("подсказка: /raceid @упоминание @упоминание", cmd.peer)
                        return None
                else:
                    vk_say("подсказка: /raceid @упоминание @упоминание", cmd.peer)
                    return None

            race_str, data = self.race(cmd.attach, cmd.users[attach_user]) if isid else self.race(cmd.by, cmd.attach)
            if data:
                races.append(data)
            vk_say(race_str, cmd.peer)

        else: vk_say("В данный момент команда отключена.", cmd.peer)

    def race(self, st, nd):
        if not st is nd:
            maxint = self.cars[st.car_id].win_prob + self.cars[nd.car_id].win_prob
            r = random.randint(0, maxint-1)
            if r <= self.cars[st.car_id].win_prob:
                win = st
            else:
                win = nd
            toreturn = "В этом заеде победил "+win.name.nom()+" на своей "+self.cars[win.car_id].name+"!"
            if state.get("boss"):
                killed = self.activeboss.doDamage()
                if not killed:
                    toreturn += f"\n\nЭтот заезд нанес {self.activeboss.get_dmg} урона боссу {self.activeboss.name}. У него осталось {self.activeboss.hp} ХП."
                else:
                    toreturn += f"\n\nЭтот заезд нанес последний удар по боссу, уничтожив его.\n[так тут надо упоминние не забыть]"
                    self.activeboss.id = 0
                    state.switch("boss")
                    state.switch("race")
            return toreturn, [st, nd, win]
        else:
            return "Ошибка: Вы не можете устраивать заезд с самим с собой", None