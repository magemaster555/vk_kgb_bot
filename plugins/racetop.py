from plugins.utils import *

class main:
    lvl = 2
    triggers = ['racetop']
    need_users = True
    racers = {}

    def sortmod(self, racer):
        return self.racers[racer]

    def execute(self, cmd):
        self.racers = {}
        tosay = "Топ заездов:\n"
        if len(races) > 0:
            for race in races:
                #tosay += f"Заезд {race[0].name.nom()} vs {race[1].name.nom()}.\nПобедитель - {race[2].name.nom()}\n================\n"
                if race[2].vk_id in self.racers:
                    self.racers[race[2].vk_id] += 1
                else:
                    self.racers[race[2].vk_id] = 1
            i = 1
            for racer in sorted(self.racers, reverse = True, key=self.sortmod):
                tosay += f"[{i}]{cmd.users[racer].name.nom()} -- {self.racers[racer]}\n"
                i += 1
            vk_say(tosay, cmd.peer)
        else: vk_say("Топ заездов пуст.", cmd.peer)
