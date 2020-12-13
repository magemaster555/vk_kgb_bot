from plugins.utils import *
import os, importlib

class main:
    lvl = 2
    need_plugins = True
    triggers = ['plugin', 'plug']

    def execute(self, cmd):
        if len(cmd.params) >= 2:
            if cmd.params[1] != "list" and len(cmd.params) > 2 and cmd.params[2] == "reload":
                foo = "bar"
            elif cmd.params[1] == "list":
                for i in range(cmd.add):
                    cmd.add[i] = importlib.reload(cmd.add[i])
            else: vk_say(f"Подсказка: /{cmd.cmd} [имя плагина | list] (reload)", cmd.peer)
        else: vk_say(f"Подсказка: /{cmd.cmd} [имя плагина | list] (reload)", cmd.peer)