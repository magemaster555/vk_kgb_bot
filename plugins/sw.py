from plugins.utils import *

class main:
    lvl = 2
    triggers = ['sw']

    def execute(self, cmd):
        states = ['race', 'war']
        states_str = " | ".join(states)
        if len(cmd.params) >=2:
            if cmd.params[1] in states:
                newstate = state.switch(cmd.params[1])
                vk_say(f"Команда /{cmd.params[1]} "+("активна" if newstate else "отключена"), cmd.peer)
            else: vk_say(f"Подсказка: /sw [{states_str}]", cmd.peer)
        else: vk_say(f"Подсказка: /sw [{states_str}]", cmd.peer)