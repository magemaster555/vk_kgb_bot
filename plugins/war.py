from plugins.utils import *
import random, json, re

class main:
    lvl = 0
    triggers = ['war', 'warid']
    need_attach = True
    need_warcars = True
    need_users = True

    abilities_file = json.loads(open('data/abilities.json', 'r').read())
    abilities = []
    warcars = {}

    def execute(self, cmd):
        isid = "id" in cmd.cmd
        if isid and cmd.by.admin_level != 2:
            vk_say(NO_ACCESS_TO_COMMAND, cmd.peer)
            return None
        if state.get("war") or isid:
            if isid:
                attach_user = 0
                if len(cmd.params) > 2:
                    found_id = re.findall(r"\[id(\d+)\|[@,*].+\]", cmd.params[2])
                    if len(found_id) == 1:
                        attach_user = int(found_id[0])
                    else:
                        vk_say("подсказка: /warid @упоминание @упоминание", cmd.peer)
                        return None
                else:
                    vk_say("подсказка: /warid @упоминание @упоминание", cmd.peer)
                    return None
                    
            self.warcars = cmd.warcars
            for ab in self.abilities_file:
                cprob = random.randint(int(self.abilities_file[ab]["prob"]["from"]*100),int(self.abilities_file[ab]["prob"]["to"]*100))
                self.abilities.append({"n":ab, "p":cprob/100, "d":self.abilities_file[ab]["dmg"]})

            warlog, data = self.war(cmd.attach, cmd.users[attach_user], cmd.peer) if isid else self.war(cmd.by, cmd.attach, cmd.peer)
            if warlog:
                vk_say(f"{warlog}",cmd.peer)
                wars.append(data)
        else: vk_say("В данный момент команда отключена.", cmd.peer)
    
    def war(self, st, nd, peer):
        if not st is nd:
            if state.get("base") and st.div_id == nd.dv_id:
                vk_say("Союзники не могут сражаться во время события.", peer)
                return None
        else:
            vk_say("Вы не можете сразиться самим с собой", peer)
            return None
        moveN = 0
        log = f"{st.name.nom()} VS {nd.name.nom()}\n\n"
        savehp = [self.warcars[st.warcar_id].hp, self.warcars[nd.warcar_id].hp]
        while(self.warcars[st.warcar_id].hp > 0 and nd.warcar_id > 0):
            if moveN % 2 == 0:
                log += self.move(st, nd)
            else:
                log += self.move(nd, st)
            moveN += 1
        log += "\nВ этом сражении победил "
        win = nd if moveN % 2 == 0 else st
        log += win.name.nom()

        self.warcars[st.warcar_id].hp = savehp[0]
        self.warcars[nd.warcar_id].hp = savehp[1]

        return log, [st, nd, win]
    def move(self, st, nd):
        log = ""
        dmg = int(self.warcars[st.warcar_id].dmg)
        random_ability = random.randint(0, len(self.abilities)-1)
        random_val_of_ability = random.randint(0, 100)/100
        #attack
        log += f"[A]{st.name.first_name} => {nd.name.first_name} -- {dmg}\n"
        #skill    
        if random_val_of_ability < self.abilities[random_ability]['p']:
            log += f"[S]{st.name.first_name} => {self.abilities[random_ability]['n']}\n"
            dmg = int(dmg * self.abilities[random_ability]['d'])
        #damage
        self.warcars[nd.warcar_id].hp -= dmg
        log += f"[D]{nd.name.first_name} <= {dmg}. HP: {self.warcars[nd.warcar_id].hp}\n"
        log += "====================\n"

        return log

