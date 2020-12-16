from plugins.utils import *

class main:
    lvl = 0
    triggers = ['mm', 'cmds']
    need_plugins = True

    def execute(self, cmd):
        say = "Системно доступные команды:\n\n"
        for plugin in cmd.add:
            if plugin.main.lvl <= cmd.by.admin_level: say += "/"+plugin.main.triggers[0] + "\n"

        vk_say(say, cmd.peer)