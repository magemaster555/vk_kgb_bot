from plugins.utils import *

class main:
    lvl = 0
    triggers = ['mydiv']
    need_divs = True
    need_users = True
    def execute(self, cmd):
        if cmd.by.div_id > 0:
            tosay = "Состав подразделения "+cmd.divs[cmd.by.div_id].name+":\n\n"
            mydivusers = []

            for id in cmd.users:
                if cmd.users[id]:
                    if cmd.users[id].div_id == cmd.by.div_id:
                        mydivusers.append(cmd.users[id])

            for user in sorted(mydivusers, reverse=True, key=byRank_key):
                tosay += cmd.divs[cmd.by.div_id].getFullRankStr(user.rank) + " -- "
                tosay += user.name.nom()
                prom = cmd.divs[cmd.by.div_id].getPromote(user.rank, user.invdate)
                if prom != "": tosay += "\n"+prom
                tosay += "\n==================================\n"

            vk_say(tosay, cmd.peer)
        else:
            vk_say("Вы не состоите в подразделении.", cmd.peer)