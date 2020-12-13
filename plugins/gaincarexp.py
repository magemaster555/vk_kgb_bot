from plugins.utils import *

class main:
    lvl = 2
    need_attach = True
    need_cars = True
    need_warcars = True
    triggers = ['carexp', 'warexp']
    cars = {}
    warcars = {}
    def execute(self, cmd):
        if len(cmd.params) >= 3 and cmd.params[2].isdigit():
            self.cars = cmd.cars
            self.warcars = cmd.warcars
            cmd.params[2] = int(cmd.params[2])
            if cmd.cmd.replace("exp", '') == 'car':
                newexp = cmd.attach.carexp+cmd.params[2]
                nextcar = getNextCarAndExp(cmd.attach.car_id, self.cars)
                if nextcar:
                    tosay = f"Выдано {cmd.params[2]} опыта. Теперь у {cmd.attach.name.gen()} {newexp} опыта."
                    cmd.attach.carexp = newexp
                    if newexp >= nextcar[1]:
                        cmd.attach.car_id = nextcar[0].car_id
                        tosay += "\nВыдан новый автомобиль - "+nextcar[0].name
                        cmd.attach.updateCar()
                    vk_say(tosay, cmd.peer)
                    cmd.attach.updateCarExp()
                else: vk_say("Ошибка: хз какая, мб максимальный уровень уже.", cmd.peer)

            if cmd.cmd.replace("exp", '') == 'war':
                newexp = cmd.attach.warcarexp+cmd.params[2]
                nextcar = getNextCarAndExp(cmd.attach.warcar_id, self.warcars)
                if nextcar:
                    tosay = f"Выдано {cmd.params[2]} опыта. Теперь у {cmd.attach.name.gen()} {newexp} опыта."
                    cmd.attach.warcarexp = newexp
                    if newexp >= nextcar[1]:
                        cmd.attach.warcar_id = nextcar[0].car_id
                        tosay += "\nВыдан новый автомобиль - "+nextcar[0].name
                        cmd.attach.updateCar()
                    vk_say(tosay, cmd.peer) 
                    cmd.attach.updateCarExp()
                else: vk_say("Ошибка: хз какая, мб максимальный уровень уже.", cmd.peer)
        else: vk_say(f"Подсказка: /{cmd.cmd} @упоминание [сколько опыта выдать]", cmd.peer)
            
