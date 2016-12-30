"""
Copyright (c) 2016-2017 billyoyo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import aiohttp
import asyncio
import time
import json
from urllib import parse


class InvalidRequest(Exception): pass


class FailedToConnect(Exception): pass


class RankedRegions:
    EUWEST = "emea"
valid_regions = [x.lower() for x in dir(RankedRegions) if "_" not in x]


class Platforms:
    UPLAY = "uplay"
    STEAM = "steam"
    XBOX = "xbl"
    PLAYSTATION = "psn"
valid_platforms = [x.lower() for x in dir(Platforms) if "_" not in x]


OperatorIcons = {
    "DOC": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-doc.0b0321eb.png",
    "TWITCH": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-twitch.70219f02.png",
    "ASH": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-ash.9d28aebe.png",
    "THERMITE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-thermite.e973bb04.png",
    "BLITZ": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-blitz.734e347c.png",
    "BUCK": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-buck.78712d24.png",
    "HIBANA": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-hibana.2010ec35.png",
    "KAPKAN": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-kapkan.db3ab661.png",
    "PULSE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-pulse.30ab3682.png",
    "CASTLE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-castle.b95704d7.png",
    "ROOK": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-rook.b3d0bfa3.png",
    "BANDIT": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-bandit.6d7d15bc.png",
    "SMOKE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-smoke.1bf90066.png",
    "FROST": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-frost.f4325d10.png",
    "VALKYRIE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-valkyrie.c1f143fb.png",
    "TACHANKA": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-tachanka.41caebce.png",
    "GLAZ": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-glaz.8cd96a16.png",
    "FUZE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-fuze.dc9f2a14.png",
    "SLEDGE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-sledge.832f6c6b.png",
    "MONTAGNE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-montagne.1d04d00a.png",
    "MUTE": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-mute.ae51429f.png",
    "ECHO": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-echo.662156dc.png",
    "THATCHER": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-thatcher.73132fcd.png",
    "CAPITAO": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-capitao.1d0ea713.png",
    "IQ": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-iq.d97d8ee2.png",
    "BLACKBEARD": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-blackbeard.2292a791.png",
    "JAGER": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-jaeger.d8a6c470.png",
    "CAVEIRA": "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/large-caveira.e4d82365.png",
    "DEFAULT": "https://ubistatic-a.akamaihd.net/0058/prod/assets/styles/images/mask-large-bandit.fc038cf1.png"
}


OperatorStatistics = {
    "DOC": "teammaterevive",
    "TWITCH": "gadgetdestroybyshockdrone",
    "ASH": "bonfirewallbreached",
    "THERMITE": "reinforcementbreached",
    "BLITZ": "flashedenemey",
    "BUCK": "kill",
    "HIBANA": "detonate_projectile",
    "KAPKAN": "boobytrapkill",
    "PULSE": "heartbeatspot",
    "CASTLE": "kevlarbarricadedeployed",
    "ROOK": "armortakenteammate",
    "BANDIT": "batterykill",
    "SMOKE": "poisongaskill",
    "FROST": "dbno",
    "VALKYRIE": "camdeployed",
    "TACHANKA": "turretkill",
    "GLAZ": "sniperkill",
    "FUZE": "clusterchargekill",
    "SLEDGE": "hammerhole",
    "MONTAGNE": "shieldblockdamage",
    "MUTE": "gadgetjammed",
    "ECHO": "enemy_sonickburst_affected",
    "THATCHER": "gadgetdestroyedwithemp",
    "CAPITAO": "lethaldartkills",
    "IQ": "gadgetspotbyef",
    "BLACKBEARD": "gunshieldblockdamage",
    "JAGER": "gadgetdestroybycatcher",
    "CAVEIRA": "interrogations"
}


OperatorStatisticNames = {
    "DOC": "Teammates Revived",
    "TWITCH": "Gadgets Destroyed With Shock Drone",
    "ASH": "Walls Breached",
    "THERMITE": "Reinforcements Breached",
    "BLITZ": "Enemies Flahsed",
    "BUCK": "Shotgun Kills",
    "HIBANA": "Projectiles Detonated",
    "KAPKAN": "Boobytrap Kills",
    "PULSE": "Heartbeat Spots",
    "CASTLE": "Barricades Deployed",
    "ROOK": "Armor Taken",
    "BANDIT": "Battery Kills",
    "SMOKE": "Poison Gas Kills",
    "FROST": "DBNOs From Traps",
    "VALKYRIE": "Cameras Deployed",
    "TACHANKA": "Turret Kills",
    "GLAZ": "Sniper Kills",
    "FUZE": "Cluster Charge Kills",
    "SLEDGE": "Hammer Holes",
    "MONTAGNE": "Damage Blocked",
    "MUTE": "Gadgets Jammed",
    "ECHO": "Enemies Sonic Bursted",
    "THATCHER": "Gadgets Destroyed",
    "CAPITAO": "Lethal Dart Kills",
    "IQ": "Gadgets Spotted",
    "BLACKBEARD": "Damage Blocked",
    "JAGER": "Projectiles Destroyed",
    "CAVEIRA": "Interrogations"
}


class WeaponTypes:
    ASSAULT_RIFLE = 0
    SUBMACHINE_GUN = 1
    MARKSMAN_RIFLE = 2
    SHOTGUN = 3
    HANDGUN = 4
    LIGHT_MACHINE_GUN = 5
    MACHINE_PISTOL = 6


WeaponNames = [
    "Assault Rifle",
    "Submachine Gun",
    "Marksman Rifle",
    "Shotgun",
    "Handgun",
    "Light Machine Gun",
    "Machine Pistol"
]

GamemodeNames = {
    "securearea": "Secure Area",
    "rescuehostage": "Hostage Rescue",
    "plantbomb": "Bomb"
}


class Auth:

    def __init__(self, token, appid, cachetime=120):
        self.session = aiohttp.ClientSession()
        self.token = token
        self.appid = appid

        self.sessionid = ""
        self.key = ""
        self.uncertain_spaceid = ""
        self.spaceid = "5172a557-50b5-4665-b7db-e3f2e8c5041d"
        self.profileid = ""
        self.userid = ""

        self.cachetime = cachetime
        self.cache={}

    @asyncio.coroutine
    def connect(self):
        resp = yield from self.session.post("https://connect.ubi.com/ubiservices/v2/profiles/sessions", headers = {
            "Content-Type": "application/json",
            "Ubi-AppId": self.appid,
            "Authorization": "Basic " + self.token
        }, data=json.dumps({"rememberMe": True}))
        data = yield from resp.json()
        #print(json.dumps(data, indent=4))

        if "ticket" in data:
            self.key = data.get("ticket")
            self.sessionid = data.get("sessionId")
            self.uncertain_spaceid = data.get("spaceId")
        else:
            print(data)
            raise FailedToConnect


    @asyncio.coroutine
    def get(self, *args, retries=0, **kwargs):
        if "headers" not in kwargs: kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "Ubi_v1 t=" + self.key
        kwargs["headers"]["Ubi-AppId"] = self.appid

        resp = yield from self.session.get(*args, **kwargs)
        data = yield from resp.json()
        if "httpCode" in data:
            if data["httpCode"] == 401:
                if retries > 5: raise FailedToConnect
                yield from self.connect()
                result = yield from self.get(*args, retries=retries+1, **kwargs)
                return result

        return data

    @asyncio.coroutine
    def get_players(self, term, platform):
        if "platform" not in self.cache: self.cache[platform] = {}

        if term in self.cache[platform]:
            if self.cachetime > 0 and self.cache[platform][term][0] < time.time():
                del self.cache[platform][term]
            else:
                return self.cache[platform][term][1]

        data = yield from self.get("https://public-ubiservices.ubi.com/v2/profiles?nameOnPlatform=%s&platformType=%s" % (parse.quote(term), parse.quote(platform)))

        if "profiles" in data:
            results = [Player(self, x) for x in data["profiles"] if x.get("platformType", "") == platform]
            if len(results) == 0: raise InvalidRequest
            if self.cachetime != 0:
                self.cache[platform][term] = [time.time() + self.cachetime, results]
            return results
        else:
            print(data)
            raise InvalidRequest

    @asyncio.coroutine
    def get_player(self, term, platform):
        results = yield from self.get_players(term, platform)
        return results[0]


class Rank:
    RANKS = ["Unranked",
             "Copper 1",   "Copper 2",   "Copper 3",   "Copper 4",
             "Bronze 1",   "Bronze 2",   "Bronze 3",   "Bronze 4",
             "Silver 1",   "Silver 2",   "Silver 3",   "Silver 4",
             "Gold 1",     "Gold 2",     "Gold 3",     "Gold 4",
             "Platinum 1", "Platinum 2", "Platinum 3", "Diamond"]

    RANK_CHARMS = [
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20copper%20charm.44c1ede2.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20bronze%20charm.5edcf1c6.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20silver%20charm.adde1d01.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20gold%20charm.1667669d.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20platinum%20charm.d7f950d5.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20diamond%20charm.e66cad88.png"
    ]

    def __init__(self, data):
        self.max_mmr = data.get("max_mmr")
        self.mmr = data.get("mmr")
        self.wins = data.get("wins")
        self.losses = data.get("losses")
        self.rank_id = data.get("rank", 0)
        self.rank = Rank.RANKS[self.rank_id]
        self.max_rank = data.get("max_rank")
        self.next_rank_mmr = data.get("next_rank_mmr")
        self.season = data.get("season")
        self.region = data.get("region")
        self.abandons = data.get("abandons")
        self.skill_mean = data.get("skill_mean")
        self.skill_stdev = data.get("skill_stdev")

    def get_charm_url(self):
        if self.rank_id <= 4: return self.RANK_CHARMS[0]
        if self.rank_id <= 8: return self.RANK_CHARMS[1]
        if self.rank_id <= 12: return self.RANK_CHARMS[2]
        if self.rank_id <= 16: return self.RANK_CHARMS[3]
        if self.rank_id <= 19: return self.RANK_CHARMS[4]
        return self.RANK_CHARMS[5]


class Operator:
    def __init__(self, name, data):
        self.name = name.lower()

        self.wins = data["roundwon"]
        self.losses = data["roundlost"]
        self.kills = data["kills"]
        self.deaths = data["death"]

        self.statistic = data[self.name]
        self.statistic_name = OperatorStatisticNames[self.name.upper()]


class Weapon:
    def __init__(self, type):
        self.type = type
        self.name = WeaponNames[self.type]

        self.kills = 0
        self.headshots = 0
        self.hits = 0
        self.shots = 0


class Gamemode:
    def __init__(self, type):
        self.type = type
        self.name = GamemodeNames[self.type]

        self.won = 0
        self.lost = 0
        self.played = 0
        self.best_score = 0


class GameQueue:
    def __init__(self, name):
        self.name = name

        self.won = 0
        self.lost = 0
        self.time_played = 0
        self.played = 0
        self.kills = 0
        self.deaths = 0


def format_time(time_played, format):
    hours = time_played // 3600
    minutes = (time_played - (hours * 3600)) // 60
    seconds = time_played - ((hours * 3600) + (minutes * 60))

    return format.replace("%h", str(hours)).replace("%m", str(minutes)).replace("%s", str(seconds))


class Player:

    def __init__(self, auth, data):
        self.auth = auth

        self.id = data.get("profileId")
        self.userid = data.get("userId")
        self.platform = data.get("platformType")
        self.id_on_platform = data.get("idOnPlatform")
        self.name = data.get("nameOnPlatform")

        self.url = "https://game-rainbow6.ubi.com/en-us/%s/player-statistics/%s/multiplayer" % (self.platform, self.id)
        self.icon_url = "https://ubisoft-avatars.akamaized.net/%s/default_146_146.png" % (self.id)

        self.xp = data.get("xp", None)
        self.level = data.get("level", None)

        self.ranks = {}
        self.operators = {}
        self.gamemodes = {}
        self.weapons = []

        self.casual = None
        self.ranked = None

    @asyncio.coroutine
    def load_level(self): # 5172a557-50b5-4665-b7db-e3f2e8c5041d
        resp = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/r6playerprofile/playerprofile/progressions?profile_ids=%s" % (self.auth.spaceid, self.id))
        data = yield from resp.json()

        if "player_profiles" in data and len(data["player_profiles"]) > 0:
            self.xp = data["player_profiles"][0].get("xp", 0)
            self.level = data["player_profiles"][0].get("level", 0)
        else:
            print(data)

    @asyncio.coroutine
    def check_level(self):
        if self.xp is None:
            yield from self.load_level()

    @asyncio.coroutine
    def load_rank(self, region):
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/r6karma/players?board_id=pvp_ranked&profile_ids=%s&region_id=%s&season_id=-1" % (self.auth.spaceid, self.id, region))

        if "players" in data and self.id in data["players"]:
            self.ranks[region] = Rank(data["players"][self.id])
            return self.ranks[region]
        else:
            raise InvalidRequest

    @asyncio.coroutine
    def get_rank(self, region):
        if region in self.ranks:
            return self.ranks[region]

        result = yield from self.load_rank(region)
        return result

    @asyncio.coroutine
    def load_operator(self, operator):
        operator_key = "operatorpvp_" + operator.lower() + "_" + OperatorStatistics[operator.upper()]

        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/playerstats2/statistics?populations=%s&statistics=operatorpvp_kills,operatorpvp_death,operatorpvp_roundwon,operatorpvp_roundlost,%s" % (self.auth.spaceid, self.id, operator_key))

        if not "results" in data or not self.id in data["results"]:
            print(data)
            raise InvalidRequest

        data = data["results"][self.id]

        location = None
        for x in data:
            if x.startswith(operator_key) and data[x] != 0:
                location = ":".join(x.split(":")[1:3])
                break

        data = {x.split(":")[0].split("_")[1]: data[x] for x in data if location in x}
        if len(data) != 5:
            print(data)
            raise InvalidRequest

        oper = Operator(operator, data)
        self.operators[operator] = oper
        return oper

    @asyncio.coroutine
    def get_operator(self, operator):
        if operator in self.operators:
            return self.operators[operator]

        result = yield from self.load_operator(operator)
        return result

    @asyncio.coroutine
    def load_weapons(self):
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/playerstats2/statistics?populations=%s&statistics=weapontypepvp_kills,weapontypepvp_headshot,weapontypepvp_bulletfired,weapontypepvp_bullethit" % (self.auth.spaceid, self.id))

        if not "results" in data or not self.id in data["results"]:
            print(data)
            raise InvalidRequest

        data = data["results"][self.id]
        self.weapons = [Weapon(i) for i in range(7)]

        for x in data:
            spl = x.split(":")
            category = spl[0].split("_")[1]
            try:
                weapontype = int(spl[1]) - 1
                weapon = self.weapons[weapontype]
                if category == "kills": weapon.kills = data[x]
                elif category == "headshot": weapon.headshots = data[x]
                elif category == "bulletfired": weapon.shots = data[x]
                elif category == "bullethit": weapon.hits = data[x]
            except (ValueError, TypeError, IndexError):
                pass

        return self.weapons

    @asyncio.coroutine
    def check_weapons(self):
        if len(self.weapons) == 0:
            yield from self.load_weapons()
        return self.weapons

    @asyncio.coroutine
    def load_gamemodes(self):
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/playerstats2/statistics?populations=%s&statistics=secureareapvp_matchwon,secureareapvp_matchlost,secureareapvp_matchplayed,secureareapvp_bestscore,rescuehostagepvp_matchwon,rescuehostagepvp_matchlost,rescuehostagepvp_matchplayed,rescuehostagepvp_bestscore,plantbombpvp_matchwon,plantbombpvp_matchlost,plantbombpvp_matchplayed,plantbombpvp_bestscore" % (self.auth.spaceid, self.id))

        if not "results" in data or not self.id in data["results"]:
            print(data)
            raise InvalidRequest

        data = data["results"][self.id]
        self.gamemodes = {x: Gamemode(x) for x in GamemodeNames}
        for x in data:
            gamemode_name = x.split("_")[0][:-3]
            if gamemode_name in self.gamemodes:
                gamemode = self.gamemodes[gamemode_name]
                category = x.split(":")[0].split("_")[1]
                if category == "bestscore": gamemode.best_score = data[x]
                elif category == "matchlost": gamemode.lost = data[x]
                elif category == "matchwon": gamemode.won = data[x]
                elif category == "matchplayed": gamemode.played = data[x]

        return self.gamemodes

    @asyncio.coroutine
    def check_gamemodes(self):
        if len(self.gamemodes) == 0:
            yield from self.load_gamemodes()
        return self.gamemodes

    @asyncio.coroutine
    def load_general(self):
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/playerstats2/statistics?populations=%s&statistics=generalpvp_timeplayed,generalpvp_matchplayed,generalpvp_matchwon,generalpvp_matchlost,generalpvp_kills,generalpvp_death,generalpvp_bullethit,generalpvp_bulletfired,generalpvp_killassists,generalpvp_revive,generalpvp_headshot,generalpvp_penetrationkills,generalpvp_meleekills" % (self.auth.spaceid, self.id))

        if not "results" in data or not self.id in data["results"]:
            print(data)
            raise InvalidRequest

        data = data["results"][self.id]
        for x in data:
            category = x.split(":")[0].split("_")[1]
            if category == "death": self.deaths = data[x]
            elif category == "penetrationkills": self.penetration_kills = data[x]
            elif category == "matchwon": self.matches_won = data[x]
            elif category == "bullethit": self.bullets_hit = data[x]
            elif category == "meleekills": self.melee_kills = data[x]
            elif category == "bulletfired": self.bullets_fired = data[x]
            elif category == "matchplayed": self.matches_played = data[x]
            elif category == "killassists": self.kill_assists = data[x]
            elif category == "timeplayed": self.time_played = data[x]
            elif category == "revive": self.revives = data[x]
            elif category == "kills": self.kills = data[x]
            elif category == "headshot": self.headshots = data[x]
            elif category == "matchlost": self.matches_lost = data[x]

    @asyncio.coroutine
    def check_general(self):
        if not hasattr(self, "kills"):
            yield from self.load_general()

    @asyncio.coroutine
    def load_queues(self):
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/OSBOR_PC_LNCH_A/playerstats2/statistics?populations=%s&statistics=casualpvp_matchwon,casualpvp_matchlost,casualpvp_timeplayed,casualpvp_matchplayed,casualpvp_kills,casualpvp_death,rankedpvp_matchwon,rankedpvp_matchlost,rankedpvp_timeplayed,rankedpvp_matchplayed,rankedpvp_kills,rankedpvp_death" % (self.auth.spaceid, self.id))

        if not "results" in data or not self.id in data["results"]:
            print(data)
            raise InvalidRequest

        data = data["results"][self.id]
        self.ranked = GameQueue("ranked")
        self.casual = GameQueue("casual")
        for x in data:
            name = x.split(":")[0].split("_")
            queue = name[0][:-3]
            if queue == "ranked" or queue == "casual":
                gq = self.ranked
                if queue == "casual": gq = self.casual
                category = name[1]
                if category == "matchwon": gq.won = data[x]
                elif category == "matchlost": gq.lost = data[x]
                elif category == "timeplayed": gq.time_played = data[x]
                elif category == "matchplayed": gq.played = data[x]
                elif category == "kills": gq.kills = data[x]
                elif category == "death": gq.deaths = data[x]

    @asyncio.coroutine
    def check_queues(self):
        if self.casual is None:
            yield from self.load_queues()
