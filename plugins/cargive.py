from plugins.utils import *

class main:
    triggers = ['gcar', 'cargive', 'warcargive', 'gwcar']
    
    need_cars = True
    need_warcars = True
    need_attach = True
    
    lvl = 2

    cars = {}
    def execute(self, cmd):
        if len(cmd.params) >= 3:
            if cmd.params[2].isdigit():
                cmd.params[2] = int(cmd.params[2])

                if "w" in cmd.cmd:
                    self.cars = cmd.warcars
                    usercarid = cmd.attach.warcar_id
                else:
                    self.cars = cmd.cars
                    usercarid = cmd.attach.car_id

                if cmd.params[2] in self.cars:
                    if usercarid != cmd.params[2]:
                        vk_say(f"Успешено выдан автомобиль {self.cars[cmd.params[2]].name}[{cmd.params[2]}] пользователю {cmd.attach.name.nom()}", cmd.peer)
                        
                        if "w" in cmd.cmd: cmd.attach.warcar_id = cmd.params[2]
                        else: cmd.attach.car_id = cmd.params[2]

                        cmd.attach.updateCar()
                    else: vk_say("У указанного пользователя уже эта машина.", cmd.peer)
                else: vk_say("Ошибка: Не найдено автомобиля с таким ID.", cmd.peer)
            #if "w" in cmd.cmd.raplce("give", ''):
            else: vk_say(f"Подсказка: /{cmd.cmd} @упоминание [ID автомобиля]", cmd.peer)   
        else: vk_say(f"Подсказка: /{cmd.cmd} @упоминание [ID автомобиля]", cmd.peer)