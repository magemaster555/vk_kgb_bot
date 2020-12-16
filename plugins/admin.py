from plugins.utils import *

class main:
    lvl = 1
    triggers = ['adm', 'admin', 'setadmin']
    need_users = True
    def execute(self, cmd):
        if cmd.cmd != "setadmin":
            say = "Вы вошли в админ режим." if cmd.by.admin_level == 1 else "Вы вышли из админ режима."
            if cmd.by.admin_level == 1: cmd.by.admin_level = 2
            elif cmd.by.admin_level == 2: cmd.by.admin_level = 1
            cmd.by.updateAdmin()
            vk_say(say, cmd.peer)
        else:
            if len(cmd.params) > 1 and cmd.params[1].isdigit() and int(cmd.params[1]) in cmd.users:
                cmd.users[int(cmd.params[1])].admin_level = 2
                cmd.users[int(cmd.params[1])].updateAdmin()
                vk_say("+", cmd.peer)