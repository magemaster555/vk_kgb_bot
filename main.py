import os, importlib, threading, re
from plugins.utils import *
import plugins.db as db

log("===============")
log(">>STARTED")
log("===============")

global_peer = 0

def fsay(txt):
    if global_peer != 0:
        vk_api("messages.send", peer_id=global_peer, message=txt)

user_ids = []

users = {}
users[0] = None

divisions = {}
divisions[0] = None

cars = {}
cars[0] = None

warcars = {}
warcars[0] = None

bosses = {}
bosses[0] = None

plugins = []

LOG = ""

dbr = db.exec("SELECT * FROM divisions")
dbr = dbr.fetchall()
for row in dbr:
    ranks = open(f"data/ranks_{row[0]}.txt", "r").read().split("\n")
    divisions[row[0]] = Div(row[1], row[3], ranks)
LOG += log("Дивизионы проинициализированы")

dbr = db.exec("SELECT * FROM users")
dbr = dbr.fetchall()
for row in dbr:
    user_ids.append(row[1])

names = vk_api("users.get", user_ids=",".join(map(str, user_ids)))
names_gen = vk_api("users.get", user_ids=",".join(map(str, user_ids)), name_case="gen")
i = 0
for row in dbr:
    name = Name(names[i]['first_name'], names[i]['last_name'], names_gen[i]['first_name'], names_gen[i]['last_name'])
    users[user_ids[i]] = User(user_ids[i], name, row[2], row[3], row[9], row[7], row[8], row[4], row[5], row[6])
    i += 1
LOG += log("Пользователи проинициализированы.")

dbr = db.exec("SELECT * FROM def_cars")
dbr = dbr.fetchall()
for row in dbr:
    cars[row[1]] = Car(row[0], row[1], row[2], row[3], row[4])

dbr = db.exec("SELECT * FROM war_cars")
dbr = dbr.fetchall()
for row in dbr:
    warcars[row[1]] = WarCar(row[0], row[1], row[2], row[4], row[3], row[5])
LOG += log("Автомобили проинициализированы.")

dbr = db.exec("SELECT * FROM bosses")
dbr = dbr.fetchall()
for row in dbr:
    bosses[row[0]] = [row[0], row[1], row[2], row[3]]
LOG += log("Боссы проинициализированы.")

LOG += log("Начинается инициализация плагинов.")
for file in os.listdir('plugins'):
    if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py', 'db.py']:
        plugin = importlib.import_module('plugins.'+file.replace('.py',''))
        if hasattr(plugin.main, "triggers"):
            if hasattr(plugin.main, "lvl"):
                plugins.append(plugin)
                LOG += log("Загружен плагин "+file.replace('.py',''))
            else: LOG += log("Ошибка загрузки плагина "+file.replace('.py','')+" - отсутствует атрибут lvl")
        else: LOG += log("Ошибка загрузки плагина "+file.replace('.py','')+" - отсутствует атрибут triggers")
LOG += log("Загружены все плагины.")

activeboss = Boss()

LP = LongPoll()
LOG += log("Проинициальзорован LongPoll")
LOG += log("Бот успешно загружен.")
restartreason = open("restart.txt", "r").read()
if restartreason != "0":
    vk_api("messages.send", peer_id=restartreason, message=LOG)
    open("restart.txt", "w").write("0")

while True:
    try:
        upd = LP.update()
        if upd == None:
            log("Неизвестная ошибка лонгполла. Игнорируем.")
            continue
        for action in upd:
            if action['type'] == "message_new":
                msg = action['object']['message']
                author = msg['from_id']

                if msg['text'].startswith('/'):

                    if author not in users:
                        log("Сообщение от незарегистрированного пользователя")
                        continue

                    cmd_params = msg['text'].lower().split(" ")
                    curcmd = cmd_params[0].replace('/','')

                    attach_user = 0
                    if len(cmd_params) > 1:
                        found_id = re.findall(r"\[id(\d+)\|.+\]", cmd_params[1])
                        if len(found_id) == 1:
                            attach_user = int(found_id[0])
                            if attach_user not in users:
                                fsay("Ошибка: У указанного пользователя отсутствует аккаунт в БД.Создать - /add(не работает пока что)")
                                continue

                    global_peer = msg['peer_id']
                    for plugin in plugins:
                        if curcmd in plugin.main.triggers:
                            if users[author].admin_level >= plugin.main.lvl:
                                    if hasattr(plugin.main, 'need_attach') and plugin.main.need_attach and attach_user == 0:
                                        fsay(f"Ошибка: Укажите цель: /{curcmd} @упоминание [аргументы]")
                                        continue

                                    cmd = Command(users[author], curcmd, cmd_params, global_peer, users[attach_user])

                                    if hasattr(plugin.main, 'need_divs') and plugin.main.need_divs:
                                        cmd.divs = divisions
                                    if hasattr(plugin.main, 'need_cars') and plugin.main.need_cars:
                                        cmd.cars = cars
                                    if hasattr(plugin.main, 'need_warcars') and plugin.main.need_warcars:
                                        cmd.warcars = warcars
                                    if hasattr(plugin.main, 'need_users') and plugin.main.need_users:
                                        cmd.users = users
                                    if hasattr(plugin.main, 'need_plugins') and plugin.main.need_plugins:
                                        cmd.add = plugins
                                    if hasattr(plugin.main, 'need_bosses') and plugin.main.need_bosses:
                                        cmd.ab = activeboss
                                        cmd.add = bosses
                                        
                                    activemod = plugin.main()
                                    threading.Thread(target=activemod.execute,args=(cmd,)).start()
                            else:
                                fsay(NO_ACCESS_TO_COMMAND)
    except KeyboardInterrupt:
        print()
        log("Рестарт <= Keyboard")
        os._exit(0)
    except Exception as e:
        log("Ошибка: "+str(e))
