from plugins.utils import *

class main:
    lvl = 1
    triggers = ['adm', 'admin']
    def execute(self, cmd):
        say = "Вы вошли в админ режим." if cmd.by.admin_level == 1 else "Вы вышли из админ режима."
        if cmd.by.admin_level == 1: cmd.by.admin_level = 2
        elif cmd.by.admin_level == 2: cmd.by.admin_level = 1
        cmd.by.updateAdmin()
        vk_say(say, cmd.peer)