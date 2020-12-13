import json, random, requests, time, datetime
import plugins.db as db
NO_ACCESS_TO_COMMAND = "Ошибка: У Вас нет доступа к использованию этой команды."
cfg = json.loads(open("config.json", 'r').read())

starttime = time.time()

wars = []
races = []

def utime():
    dt = datetime.datetime.today()
    return time.mktime((dt.year, dt.month, dt.day, 0, 0, 3*3600, 0, 0, 0))

def date(unixtime, format = '%d.%m.%Y %H:%M:%S'):
    d = datetime.datetime.fromtimestamp(unixtime)
    return d.strftime(format)

def log(text):
    text = '['+date(time.time()+8*3600)+']: '+str(text)
    print(text)
    return text+"\n"

def vk_api(method, token = cfg['token'], **params):
    url = "https://api.vk.com/method/"+method
    params['access_token'] = cfg['token']
    
    if 'v' not in params: params['v'] = cfg['api_v']
    if method == "messages.send": params['random_id'] = random.randint(0, 10000)
    
    try:
        r = requests.post(url, data=params)
        r = r.json()
    except Exception as e:
        log("Ошибка запроса на сервер VK API {}".format(e))
        return None

    if 'error' in r:
        log("Ошибка VK API: {}".format(r['error']))
        return None
    return r['response']

def vk_say(txt, peer):
    return vk_api("messages.send", peer_id=peer, message=txt)

class State:
    def get(self, key):
        if key != "":
            return json.loads(open("data/states.json", "r").read())[key]
        else: return None
    def switch(self, key):
        if key != "":
            js = json.loads(open("data/states.json", "r").read())
            js[key] = not js[key]
            open("data/states.json", "w").write(json.dumps(js))
            return js[key]
        else: return None
state = State()

class LongPoll:
    server : str
    key : str
    ts : int
    wait = 20

    def __init__(self):
        r = vk_api("groups.getLongPollServer", group_id=cfg['group_id'])
        if r != None:
            self.server = r['server']
            self.ts = r['ts']
            self.key = r['key']
        else: log("Ошбка инициализации лонгполла.")

    def update(self):
        try:
            r = requests.get(f"{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait={self.wait}", timeout=25).json()
            if 'failed' in r:
                print(r)
                self.__init__()
            elif 'updates' in r:
                if self.ts != r['ts']:
                    log("Обновлен TS. Новый - "+str(r['ts']))
                    self.ts = r['ts']
                return r['updates']
            else: return None
        except Exception as ex:
            log("Ошибка обновления лонгполла: "+str(ex))
            return None

class Name:
    first_name : str
    last_name : str
    first_name_gen : str
    last_name_gen : str

    def __init__(self, first_name, last_name, first_name_gen, last_name_gen):
        self.first_name         = first_name
        self.last_name          = last_name
        self.first_name_gen     = first_name_gen
        self.last_name_gen      = last_name_gen

    def nom(self):
        return self.last_name + " " + self.first_name

    def gen(self):
        return self.last_name_gen + " " + self.first_name_gen

class Div:
    name : str
    hp : int
    kri : int
    ranks : list
    def __init__(self, name, kri, ranks):
        self.name = name
        self.kri = kri
        self.ranks = ranks

    def getRankName(self, rank):
        return self.ranks[rank-1]
    
    def getFullRankStr(self, rank):
        toreturn = f"{self.ranks[rank-1]} [{rank}]"
        if rank == 8: toreturn = "[Z] "+toreturn
        elif rank == 9: toreturn = "[L] "+toreturn
        return toreturn

    def getPromote(self, rank, invdate):
        if rank <= 7:
            proms = open("data/div_proms.txt", "r").read().split("\n")
            days_to = proms[int(rank)-1].split(".")[1]
            value = datetime.datetime.fromtimestamp(int(invdate)+3600*24*int(days_to))
            return "Повышение: "+value.strftime("%d.%m.%Y")
        else: return ""

class Car:
    normal_id : int
    car_id : int
    name : str
    win_prob : int
    exp_to_reach : int

    def __init__(self, normal_id, car_id, name, win_prob, exp_to_reach):
        self.normal_id = normal_id
        self.name = name
        self.win_prob = win_prob
        self.exp_to_reach = exp_to_reach
        self.car_id = car_id

class WarCar:
    normal_id : int
    car_id : int
    name : str
    dmg : int
    hp : int
    exp_to_reach : int

    def __init__(self, normal_id, car_id, name, dmg, hp, exp_to_reach):
        self.normal_id = normal_id
        self.car_id = car_id
        self.name = name
        self.dmg = dmg
        self.hp = hp
        self.exp_to_reach = exp_to_reach

#returns array [nextCar: Car, expToIt : int]
def getNextCarAndExp(carid, cars):
    normalid = 0
    exp = 0
    for id in cars:
        if cars[id]:
            if cars[id].car_id == carid:
                normalid = cars[id].normal_id
                break
    for id in cars:
        if cars[id]:
            exp += cars[id].exp_to_reach
            if cars[id].normal_id == normalid+1:
                return [cars[id], exp]
    return None

class User:
    name : Name
    vk_id : int
    div_id : int
    rank : int
    admin_level : int
    car_id : int
    warcar_id : int
    invdate : int
    carexp : int
    warcarexp : int
    def __init__(self, vk_id, name, div_id, rank, admin_level, car_id, warcar_id, invdate, carexp, warcarexp):
        self.vk_id = vk_id
        self.name = name
        self.div_id = div_id
        self.rank = rank
        self.admin_level = admin_level
        self.car_id = car_id
        self.warcar_id = warcar_id
        self.invdate = invdate
        self.warcarexp = warcarexp
        self.carexp = carexp

    def updateDiv(self):
        db.exec(f"UPDATE users SET div_id = {self.div_id}, divrank = {self.rank}, invdate = {utime()} WHERE vkid = {self.vk_id}")

    def updateCarExp(self):
        db.exec(f"UPDATE users SET car_exp = {self.carexp}, war_exp = {self.warcarexp} WHERE vkid = {self.vk_id}")

    def updateCar(self):
        db.exec(f"UPDATE users SET car_id = {self.car_id}, warcar_id = {self.warcar_id} WHERE vkid = {self.vk_id}")

    def updateAdmin(self):
        db.exec(f"UPDATE users SET admin = {self.admin_level} WHERE vkid = {self.vk_id}")
    
def byRank_key(user):
    return user.rank


class Command:
    by : User
    params : list
    cmd : str
    peer : int
    attach : User
    divs : dict
    cars : dict
    warcars : dict
    users : dict
    add : dict
    def __init__(self, user, cmd, params, peer, attach = None, divs = None, cars = None, warcars = None, users = None, add = None):
        self.by = user
        self.cmd = cmd
        self.params = params
        self.peer = peer
        self.attach = attach
        self.divs = divs
        self.cars = cars
        self.warcars = warcars
        self.users = users
        self.add = add
        