from plugins.utils import *

class main:
    lvl = 0
    triggers = ['expinfo', 'stats']
    need_divs = True
    need_cars = True
    need_warcars = True
    cars = {}
    warcars = {}
    def execute(self, cmd):
        self.cars = cmd.cars
        self.warcars = cmd.warcars
        if cmd.attach != None:
            if cmd.by.admin_level == 2 or cmd.by.vk_id == cmd.attach.vk_id:
                vk_say(self.getinfo(cmd.attach, cmd.divs[cmd.attach.div_id]), cmd.peer)
            else: vk_say("Вы можете просматривать только свою статистику.", cmd.peer)
        else: vk_say(self.getinfo(cmd.by, cmd.divs[cmd.by.div_id]), cmd.peer)

    def getinfo(self, about, div):
        tosay = "-- " + about.name.nom() + " --\n"
        #div info
        if about.rank > 0 and div:
            tosay += f"Член подразделения \"{div.name}\"\n"
            tosay += f"Ранг: {div.getFullRankStr(about.rank)}\n"
            tosay += div.getPromote(about.rank, about.invdate)
        else:
            tosay += "Не состоит в подразделении."

        #car info
        if about.car_id > 0:
            tosay += "\n\nАвтомобильная статистика:\n"
            tosay += "Автомобиль: "+self.cars[about.car_id].name+"\n"
            nextcar = getNextCarAndExp(about.car_id, self.cars)
            if nextcar != None:
                #tosay += f"рял опыта {about.carexp}. Функция подсчета вернула что нужно {nextcar[1]}\n"
                need_exp = nextcar[1] - about.carexp
                #TEMP SOLUTION
                if need_exp <= 0:
                    vk_say(f"[warning]\nУ {about.name.gen()} возможно неверная ОБЫЧНАЯ машина.\nСейчас у него {self.cars[about.car_id].name}, опыта до {nextcar.name} \'{need_exp}\'", 218999719)
                #^^^^^^^^^^^^^^^^
                tosay += f"Нужно {need_exp} опыта для получения {nextcar[0].name}"
            else: tosay+= "Максимальный уровень."

        #warcar info
        if about.warcar_id > 0:
            tosay += "\n\nБоевой автомобиль:"+self.warcars[about.warcar_id].name+"\n"
            nextcar = getNextCarAndExp(about.warcar_id, self.warcars)
            if nextcar != None:
                #tosay += f"рял опыта {about.warcarexp}. Функция подсчета вернула что нужно {nextcar[1]}\n"
                need_exp = nextcar[1] - about.warcarexp
                #TEMP SOLUTION
                if need_exp <= 0:
                    vk_say(f"[warning]\nУ {about.name.gen()} возможно неверная БОЕВАЯ машина.\nСейчас у него {self.warcars[about.warcar_id].name}, опыта до {nextcar[0].name} \'{need_exp}\'", 218999719)
                #^^^^^^^^^^^^^^^^
                tosay += f"Нужно {need_exp} опыта для получения {nextcar[0].name}"
            else: tosay+= "Максимальный уровень."
        return tosay
