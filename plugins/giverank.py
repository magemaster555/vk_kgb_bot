from plugins.utils import *

class main:
    lvl = 0
    triggers = ['giverank']
    need_divs = True
    need_users = True
    need_attach = True

    def execute(self, cmd):
        if cmd.by.rank > 7 or cmd.by.admin_level == 2:
            if len(cmd.params) >= 3 and cmd.params[2].isdigit():
                if not (cmd.by is cmd.attach) or cmd.by.admin_level == 2:
                    if (cmd.attach.div_id == cmd.attach.div_id and cmd.by.rank < cmd.attach.rank) or cmd.by.admin_level == 2:
                        if (int(cmd.params[2]) < cmd.by.rank or cmd.by.admin_level == 2) and int(cmd.params[2]) < 10:
                            act = "повышен" if  cmd.attach.rank > int(cmd.params[2]) else "понижен"
                            cmd.attach.rank = int(cmd.params[2])
                            cmd.attach.updateDiv()
                            vk_say(f"{cmd.attach.name.nom()} был {act} в ранге до {cmd.divs[cmd.attach.div_id].getRankName(cmd.attach.rank)}", cmd.peer)
                        else: vk_say("Вы не можете выдать ранг больше вашего.", cmd.peer)
                    else: vk_say("Вы не можете выдать ранг этому пользователю", cmd.peer)
                else: vk_say("Вы не можете выдавать ранг самому себе", cmd.peer)
            else: vk_say("Подсказка: /giverank [@упоминание] [ранг]", cmd.peer)
        else: vk_say(NO_ACCESS_TO_COMMAND, cmd.peer)