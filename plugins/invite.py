from plugins.utils import *

class main:
    lvl = 0
    triggers = ['invite', 'uninvite', 'ainvite']
    need_divs = True
    need_attach = True
    def execute(self, cmd):
        if (cmd.by.div_id != 0 and cmd.by.rank > 7) or cmd.by.admin_level == 2:
            if "un" in cmd.cmd:
                if cmd.by.div_id == cmd.attach.div_id and cmd.by.div_id > 0:
                    if cmd.attach.div_id != 0:
                        vk_say(f"{cmd.attach.name.nom()} кикнут из подразделения {cmd.divs[cmd.by.div_id].name}.", cmd.peer)
                        cmd.attach.div_id = 0
                        cmd.attach.rank = 0
                        cmd.attach.updateDiv()
                    else: vk_say(f"Ошибка: {cmd.attach.name.nom()} не состоит в подразделении.", cmd.peer)
                else: vk_say(NO_ACCESS_TO_COMMAND, cmd.peer)
            elif "a" in cmd.cmd:
                if cmd.by.admin_level == 2:
                    if len(cmd.divs) >= 3 and cmd.divs[int(cmd.params[2])] and cmd.params[2].isdigit():
                        cmd.attach.div_id = int(cmd.params[2])
                        cmd.attach.rank = 1
                        cmd.attach.updateDiv()
                        vk_say(f"{cmd.attach.name.nom()} принят в подражделение {cmd.divs[cmd.by.div_id].name}.", cmd.peer)
                    else: vk_say("Подсказка: /ainvite @упоминание код_подразделения")
                else: vk_say(NO_ACCESS_TO_COMMAND, cmd.peer)
            else:
                if cmd.attach.div_id == 0:
                    cmd.attach.div_id = cmd.by.div_id
                    cmd.attach.rank = 1
                    cmd.attach.updateDiv()
                    vk_say(f"{cmd.attach.name.nom()} принят в подражделение {cmd.divs[cmd.by.div_id].name}.", cmd.peer)
                else: vk_say(f"Ошибка: {cmd.attach.name.nom()} уже состоит в подразделении.", cmd.peer)
            
        else: vk_say(NO_ACCESS_TO_COMMAND, cmd.peer)