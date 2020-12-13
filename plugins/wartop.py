from plugins.utils import *

class main:
    lvl = 2
    triggers = ['wartop']
    need_users = True
    racers = {}

    def sortmod(self, racer):
        return self.racers[racer]

    def execute(self, cmd):
        self.racers = {}
        tosay = "Топ сражений:\n"
        if len(wars) > 0:
            for race in wars:
                if race[2].vk_id in self.racers:
                    self.racers[race[2].vk_id] += 1
                else:
                    self.racers[race[2].vk_id] = 1
            i = 1
            for racer in sorted(self.racers, reverse = True, key=self.sortmod):
                tosay += f"[{i}]{cmd.users[racer].name.nom()} -- {self.racers[racer]}\n"
                i += 1
            vk_say(tosay, cmd.peer)
        else: vk_say("Топ сражений пуст.", cmd.peer)
