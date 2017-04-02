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
import base64
from urllib import parse


class InvalidRequest(Exception): pass


class FailedToConnect(Exception): pass


class RankedRegions:
    """Ranked regions supported

    Attributes
    ----------
    EU : str
        name of the european data centre
    NA : str
        name of the north american data centre
    ASIA : str
        name of the asian data centre"""
    EU = "emea"
    NA = "ncsa"
    ASIA = "apac"


valid_regions = [x.lower() for x in dir(RankedRegions) if "_" not in x]


class Platforms:
    """Platforms supported

    Attributes
    ----------
    UPLAY : str
        name of the uplay platform
    XBOX : str
        name of the xbox platform
    PLAYSTATION : str
        name of the playstation platform"""

    UPLAY = "uplay"
    XBOX = "xbl"
    PLAYSTATION = "psn"


valid_platforms = [x.lower() for x in dir(Platforms) if "_" not in x]


PlatformURLNames = {
    "uplay": "OSBOR_PC_LNCH_A",
    "psn": "OSBOR_PS4_LNCH_A",
    "xbl": "OSBOR_XBOXONE_LNCH_A"
}


OperatorProfiles = {
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


OperatorIcons = {
    "DEFAULT": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Glaz_Badge_229122.png",
    "HIBANA": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-hibana_275569.png",
    "SMOKE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Smoke_Badge_196198.png",
    "KAPKAN": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Kapkan_Badge_229123.png",
    "TACHANKA": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Tachanka_Badge_229124.png",
    "THERMITE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Thermite_Badge_196408.png",
    "THATCHER": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Thatcher_Badge_196196.png",
    "GLAZ": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Glaz_Badge_229122.png",
    "BANDIT": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Bandit_Badge_222163.png",
    "ROOK": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Rook_Badge_211296.png",
    "IQ": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/IQ_Badge_222165.png",
    "PULSE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Pulse_Badge_202497.png",
    "MUTE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Mute_Badge_196195.png",
    "VALKYRIE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-valkyrie_250313.png",
    "FROST": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-frost_237595.png",
    "DOC": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Doc_Badge_211294.png",
    "SLEDGE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Sledge_Badge_196197.png",
    "JAGER": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Jager_Badge_222166.png",
    "BLACKBEARD": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-blackbeard_250312.png",
    "FUZE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Fuze_Badge_229121.png",
    "ECHO": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-echo_275572.png",
    "CAVEIRA": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-caveira_263102.png",
    "BLITZ": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Blitz_Badge_222164.png",
    "MONTAGNE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Montagne_Badge_211295.png",
    "ASH": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Ash_Badge_196406.png",
    "TWITCH": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Twitch_Badge_211297.png",
    "CASTLE": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/Castle_Badge_196407.png",
    "BUCK": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-buck_237592.png",
    "CAPITAO": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-operators-badge-capitao_263100.png",
    "JACKAL": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-velvet-shell-badge-jackal_282825.png",
    "MIRA": "https://ubistatic19-a.akamaihd.net/resource/en-GB/game/rainbow6/siege/R6-velvet-shell-badge-mira_282826.png"
}


OperatorStatistics = {
    "DOC": "teammaterevive",
    "TWITCH": "gadgetdestroybyshockdrone",
    "ASH": "bonfirewallbreached",
    "THERMITE": "reinforcementbreached",
    "BLITZ": "flashedenemy",
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
    "ECHO": "enemy_sonicburst_affected",
    "THATCHER": "gadgetdestroywithemp",
    "CAPITAO": "lethaldartkills",
    "IQ": "gadgetspotbyef",
    "BLACKBEARD": "gunshieldblockdamage",
    "JAGER": "gadgetdestroybycatcher",
    "CAVEIRA": "interrogations",
    "JACKAL": "cazador_assist_kill",
    "MIRA": "black_mirror_gadget_deployed"
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
    "CAVEIRA": "Interrogations",
    "JACKAL": "Footprint Scan Assists",
    "MIRA": "Black Mirrors Deployed"
}


class WeaponTypes:
    """Weapon Types

    Attributes
    ----------
    ASSAULT_RIFLE : int
        the assault rifle weapon id
    SUBMACHINE_GUN : int
        the submachine gun weapon id
    MARKSMAN_RIFLE : int
        the marksman rifle weapon id
    SHOTGUN : int
        the shotgun weapon id
    HANDGUN : int
        the handgun weapon id
    LIGHT_MACHINE_GUN : int
        the light machine gun weapon id
    MACHINE_PISTOL : int
        the machine pistol weapon id"""
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
    """Holds your authentication information. Used to retrieve Player objects

    Parameters
    ----------
    email : Optional[str]
        Your Ubisoft email
    password : Optional[str]
        Your Ubisoft password
    token : Optional[str]
        Your Ubisoft auth token, either supply this OR email/password
    appid : Optional[str]
        Your Ubisoft appid, not required
    cachetime : Optional[float]
        How long players are cached for (in seconds)
    max_connect_retries : Optional[int]
        How many times the auth client will automatically try to reconnect, high numbers can get you temporarily banned

    Attributes
    ----------
    session
        aiohttp client session
    token : str
        your token
    appid : str
        your appid
    sessionid : str
        the current connections session id (will change upon attaining new key)
    key : str
        your current auth key (will change every time you connect)
    spaceids : dict
        contains the spaceid for each platform
    profileid : str
        your profileid (corresponds to your appid)
    userid : str
        your userid (corresponds to your appid)
    cachetime : float
        the time players are cached for
    cache : dict
        the current player cache

    """

    @staticmethod
    def get_basic_token(email, password):
        return base64.b64encode((email + ":" + password).encode("utf-8")).decode("utf-8")

    def __init__(self, email=None, password=None, token=None, appid=None, cachetime=120, max_connect_retries=1):
        self.session = aiohttp.ClientSession()
        self.max_connect_retries = max_connect_retries

        if email is not None and password is not None:
            self.token = Auth.get_basic_token(email, password)
        elif token is not None:
            self.token = token
        else:
            raise TypeError("Argument error, requires either email/password or token to be set, neither given")

        if appid is not None:
            self.appid = appid
        else:
            self.appid = "39baebad-39e5-4552-8c25-2c9b919064e2"

        self.sessionid = ""
        self.key = ""
        self.uncertain_spaceid = ""
        self.spaceids = {
            "uplay": "5172a557-50b5-4665-b7db-e3f2e8c5041d",
            "psn": "05bfb3f7-6c21-4c42-be1f-97a33fb5cf66",
            "xbl": "98a601e5-ca91-4440-b1c5-753f601a2c90"
        }
        self.profileid = ""
        self.userid = ""

        self.cachetime = cachetime
        self.cache={}

    @asyncio.coroutine
    def connect(self):
        """|coro|

        Connect to ubisoft, automatically called when needed"""
        resp = yield from self.session.post("https://connect.ubi.com/ubiservices/v2/profiles/sessions", headers = {
            "Content-Type": "application/json",
            "Ubi-AppId": self.appid,
            "Authorization": "Basic " + self.token
        }, data=json.dumps({"rememberMe": True}))

        data = yield from resp.json()

        if "ticket" in data:
            self.key = data.get("ticket")
            self.sessionid = data.get("sessionId")
            self.uncertain_spaceid = data.get("spaceId")
        else:
            raise FailedToConnect


    @asyncio.coroutine
    def get(self, *args, retries=0, referer=None, json=True, **kwargs):
        if "headers" not in kwargs: kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "Ubi_v1 t=" + self.key
        kwargs["headers"]["Ubi-AppId"] = self.appid
        kwargs["headers"]["Ubi-SessionId"] = self.sessionid
        kwargs["headers"]["Connection"] = "keep-alive"
        if referer is not None:
            if isinstance(referer, Player):
                referer = "https://game-rainbow6.ubi.com/en-gb/uplay/player-statistics/%s/multiplayer" % referer.id
            kwargs["headers"]["Referer"] = str(referer)

        resp = yield from self.session.get(*args, **kwargs)

        if json:
            data = yield from resp.json()

            if "httpCode" in data:
                if data["httpCode"] == 401:
                    if retries >= self.max_connect_retries: raise FailedToConnect
                    yield from self.connect()
                    result = yield from self.get(*args, retries=retries+1, **kwargs)
                    return result
                else:
                    msg = data.get("message", "")
                    if data["httpCode"] == 404: msg = "missing resource %s" % data["resource"]
                    raise InvalidRequest("HTTP Code: %s, Message: %s" % (data["httpCode"], msg))

            return data
        else:
            text = yield from resp.text()
            return text

    @asyncio.coroutine
    def get_players(self, term, platform):
        """|coro|

        get a list of players matching the term on that platform,
        this list almost always has only 1 element, so it's easier to use get_player

        Parameters
        ----------
        term : str
            the name of the player you're searching for
        platform : str
            the name of the platform you're searching on (See :class:`Platforms`)

        Returns
        -------
        list[:class:`Player`]
            list of found players"""
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
            raise InvalidRequest("Missing key profiles in returned JSON object %s" % str(data))

    @asyncio.coroutine
    def get_player(self, term, platform):
        """|coro|

        Calls get_players and returns the first element

        Parameters
        ----------
        term : str
            the name of the player you're searching for
        platform : str
            the name of the platform you're searching on (See :class:`Platforms`)

        Returns
        -------
        :class:`Player`
            player found"""
        results = yield from self.get_players(term, platform)
        return results[0]


class Rank:
    """Contains information about your rank

    Attributes
    ----------
    RANKS : list[str]
        Names of the ranks
    RANK_CHARMS : list[str]
        URLs for the rank charms
    UNRANKED : int
        the unranked bracket id
    COPPER : int
        the copper bracket id
    BRONZE : int
        the bronze bracket id
    SILVER : int
        the silver bracket id
    GOLD : int
        the gold bracket id
    PLATINUM : int
        the platinum bracket id
    DIAMOND : int
        the diamond bracket id
    max_mmr : int
        the maximum MMR the player has achieved
    mmr : int
        the MMR the player currently has
    wins : int
        the number of wins this player has this season
    losses : int
        the number of losses this player has this season
    abandons : int
        the number of abandons this player has this season

    rank_id : int
        the id of the players current rank
    rank : str
        the name of the players current rank
    max_rank : int
        the id of the players max rank
    next_rank_mmr : int
        the mmr required for the player to achieve their next rank
    season : int
        the season this rank is for
    region : str
        the region this rank is for
    skill_mean : float
        the mean for this persons skill
    skill_stdev : float
        the standard deviation for this persons skill
    """
    RANKS = ["Unranked",
             "Copper 4",   "Copper 3",   "Copper 2",   "Copper 1",
             "Bronze 4",   "Bronze 3",   "Bronze 2",   "Bronze 1",
             "Silver 4",   "Silver 3",   "Silver 2",   "Silver 1",
             "Gold 4",     "Gold 3",     "Gold 2",     "Gold 1",
             "Platinum 3", "Platinum 2", "Platinum 1", "Diamond"]

    RANK_CHARMS = [
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20copper%20charm.44c1ede2.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20bronze%20charm.5edcf1c6.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20silver%20charm.adde1d01.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20gold%20charm.1667669d.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20platinum%20charm.d7f950d5.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20diamond%20charm.e66cad88.png"
    ]

    RANK_ICONS = [
        "https://i.imgur.com/ehILQ3i.jpg",
        "https://i.imgur.com/6CxJoMn.jpg",
        "https://i.imgur.com/eI11lah.jpg",
        "https://i.imgur.com/0J0jSWB.jpg",
        "https://i.imgur.com/42AC7RD.jpg",
        "https://i.imgur.com/QD5LYD7.jpg",
        "https://i.imgur.com/9AORiNm.jpg",
        "https://i.imgur.com/hmPhPBj.jpg",
        "https://i.imgur.com/D36ZfuR.jpg",
        "https://i.imgur.com/m8GToyF.jpg",
        "https://i.imgur.com/m8GToyF.jpg",
        "https://i.imgur.com/EswGcx1.jpg",
        "https://i.imgur.com/KmFpkNc.jpg",
        "https://i.imgur.com/6Qg6aaH.jpg",
        "https://i.imgur.com/B0s1o1h.jpg",
        "https://i.imgur.com/ELbGMc7.jpg",
        "https://i.imgur.com/ffDmiPk.jpg",
        "https://i.imgur.com/Sv3PQQE.jpg",
        "https://i.imgur.com/Uq3WhzZ.jpg",
        "https://i.imgur.com/xx03Pc5.jpg",
        "https://i.imgur.com/nODE0QI.jpg"
    ]

    UNRANKED = 0
    COPPER = 1
    BRONZE = 2
    SILVER = 3
    GOLD = 4
    PLATINUM = 5
    DIAMOND = 6

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

    def get_icon_url(self):
        """Get URL for this rank's icon

        Returns
        -------
        :class:`str`
            the URL for the rank icon"""
        return self.RANK_ICONS[self.rank_id]

    def get_charm_url(self):
        """Get charm URL for the bracket this rank is in

        Returns
        -------
        :class:`str`
            the URL for the charm

        """
        if self.rank_id <= 4: return self.RANK_CHARMS[0]
        if self.rank_id <= 8: return self.RANK_CHARMS[1]
        if self.rank_id <= 12: return self.RANK_CHARMS[2]
        if self.rank_id <= 16: return self.RANK_CHARMS[3]
        if self.rank_id <= 19: return self.RANK_CHARMS[4]
        return self.RANK_CHARMS[5]

    def get_bracket(self):
        """Get rank bracket

        Returns
        -------
        :class:`int`
            the id for the rank bracket this rank is in

        """
        if self.rank_id == 0: return 0
        elif self.rank_id <= 4: return 1
        elif self.rank_id <= 8: return 2
        elif self.rank_id <= 12: return 3
        elif self.rank_id <= 15: return 4
        elif self.rank_id <= 19: return 5
        else: return 6


class Operator:
    """Contains information about an operator

    Attributes
    ----------
    name : str
        the name of the operator
    wins : int
        the number of wins the player has on this operator
    losses : int
        the number of losses the player has on this operator
    kills : int
        the number of kills the player has on this operator
    deaths : int
        the number of deaths the player has on this operator
    headshots : int
        the number of headshots the player has on this operator
    melees : int
        the number of melee kills the player has on this operator
    dbnos : int
        the number of DBNO (down-but-not-out)'s the player has on this operator
    xp : int
        the total amount of xp the player has on this operator
    time_played : int
        the amount of time the player has played this operator for in seconds
    statistic : int
        the value for this operators unique statistic
    statistic_name : str
        the human-friendly name for this operators statistic"""
    def __init__(self, name, data):
        self.name = name.lower()

        self.wins = data.get("roundwon", 0)
        self.losses = data.get("roundlost", 0)
        self.kills = data.get("kills", 0)
        self.deaths = data.get("death", 0)
        self.headshots = data.get("headshot", 0)
        self.melees = data.get("meleekills", 0)
        self.dbnos = data.get("dbno", 0)
        self.xp = data.get("totalxp", 0)
        self.time_played = data.get("timeplayed", 0)

        statistic_name = self.name
        if self.name == "jackal": statistic_name = "cazador"
        if self.name == "mira": statistic_name = "black"
        self.statistic = data[statistic_name]
        self.statistic_name = OperatorStatisticNames[self.name.upper()]


class Weapon:
    """Contains information about a weapon

    Attributes
    ----------
    type : int
        the weapon type
    name : str
        the human-friendly name for this weapon type
    kills : int
        the number of kills the player has for this weapon
    headshots : int
        the number of headshots the player has for this weapon
    hits : int
        the number of bullet this player has hit with this weapon
    shots : int
        the number of bullets this player has shot with this weapon

    """
    def __init__(self, type):
        self.type = type
        self.name = WeaponNames[self.type]

        self.kills = 0
        self.headshots = 0
        self.hits = 0
        self.shots = 0


class Gamemode:
    """Contains information about a gamemode

    Attributes
    ----------
    type : str
        the gamemode id
    name : str
        the human-readable name for this gamemode
    won : int
        the number of wins the player has on this gamemode
    lost : int
        the number of losses the player has on this gamemode
    played : int
        the number of games this player has played on this gamemode
    best_score : int
        the best score this player has achieved on this gamemode"""
    def __init__(self, type):
        self.type = type
        self.name = GamemodeNames[self.type]

        self.won = 0
        self.lost = 0
        self.played = 0
        self.best_score = 0


class GameQueue:
    """Contains information about a specific game queue

    Attributes
    ----------
    name : str
        the name for this gamemode (always either "ranked" or "casual"
    won : int
        the number of wins the player has on this gamemode
    lost : int
        the number of losses the player has on this gamemode
    time_played : int
        the amount of time in seconds the player has spent playing on this gamemode
    played : int
        the number of games the player has played on this gamemode
    kills : int
        the number of kills the player has on this gamemode
    deaths : int
        the number of deaths the player has on this gamemode"""
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
    """Contains information about a specific player

    Attributes
    ----------
    auth : :class:`Auth`
        the auth object used to find this player
    id : str
        the players profile id
    userid : str
        the players user id
    platform : str
        the platform this player is on
    platform_url : str
        the URL name for this platform (used internally)
    id_on_platform : str
        the players ID on the platform
    name : str
        the players name on the platform
    url : str
        a link to the players profile
    icon_url : str
        a link to the players avatar
    xp : int
        the amount of xp the player has, must call check_level or load_level first
    level : int
        the level of the player, must call check_level or load_level first
    ranks : dict
        dict containing already found ranks ("region_name:season": :class:`Rank`)
    operators : dict
        dict containing already found operators (operator_name: :class:`Operator`)
    gamemodes : dict
        dict containing already found gamemodes (gamemode_id: :class:`Gamemode`)
    weapons : dict
        dict containing already found weapons (weapon_id: :class:`Weapon`)
    casual : :class:`GameQueue`
        stats for the casual queue, must call load_queues or check_queues first
    ranked : :class:`GameQueue`
        stats for the ranked queue, must call load_queues or check_queues first
    deaths : int
        the number of deaths the player has (must call load_general or check_general first)
    kills : int
        the number of kills the player has (must call load_general or check_general first)
    kill_assists : int
        the number of kill assists the player has (must call load_general or check_general first)
    penetration_kills : int
        the number of penetration kills the player has (must call load_general or check_general first)
    melee_kills : int
        the number of melee kills the player has (must call load_general or check_general first)
    revives : int
        the number of revives the player has (must call load_general or check_general first)
    matches_won : int
        the number of matches the player has won (must call load_general or check_general first)
    matches_lost : int
        the number of matches the player has lost (must call load_general or check_general first)
    matches_played : int
        the number of matches the player has played (must call load_general or check_general first)
    time_played : int
        the amount of time in seconds the player has played for (must call load_general or check_general first)
    bullets_fired : int
        the amount of bullets the player has fired (must call load_general or check_general first)
    bullets_hit : int
        the amount of bullets the player has hit (must call load_general or check_general first)
    headshots : int
        the amount of headshots the player has hit (must call load_general or check_general first)
    terrorist_hunt : :class:`GameQueue`
        contains all of the above state (from deaths to headshots) inside a gamequeue object.
    """

    def __init__(self, auth, data):
        self.auth = auth

        self.id = data.get("profileId")
        self.userid = data.get("userId")
        self.platform = data.get("platformType")
        self.platform_url = PlatformURLNames[self.platform]
        self.id_on_platform = data.get("idOnPlatform")
        self.name = data.get("nameOnPlatform")

        self.url = "https://game-rainbow6.ubi.com/en-us/%s/player-statistics/%s/multiplayer" % (self.platform, self.id)
        self.icon_url = "https://ubisoft-avatars.akamaized.net/%s/default_146_146.png" % (self.id)

        self.ranks = {}
        self.operators = {}
        self.gamemodes = {}
        self.weapons = []

        self.casual = None
        self.ranked = None
        self.terrorist_hunt = None

    @property
    def spaceid(self):
        return self.auth.spaceids[self.platform]

    @asyncio.coroutine
    def _fetch_statistics(self, *statsitics):
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/%s/playerstats2/statistics?populations=%s&statistics=%s" % (self.spaceid, self.platform_url, self.id, ",".join(statsitics)))

        if not "results" in data or not self.id in data["results"]:
            raise InvalidRequest("Missing results key in returned JSON object %s" % str(data))

        data = data["results"][self.id]
        stats = {}

        for x in data:
            statistic = x.split(":")[0]
            if statistic in statsitics:
                stats[statistic] = data[x]

        return stats

    @asyncio.coroutine
    def load_level(self):
        """|coro|

        Load the players XP and level"""
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/%s/r6playerprofile/playerprofile/progressions?profile_ids=%s" % (self.spaceid, self.platform_url, self.id))

        if "player_profiles" in data and len(data["player_profiles"]) > 0:
            self.xp = data["player_profiles"][0].get("xp", 0)
            self.level = data["player_profiles"][0].get("level", 0)
        else:
            raise InvalidRequest("Missing key player_profiles in returned JSON object %s" % str(data))

    @asyncio.coroutine
    def check_level(self):
        """|coro|

        Check the players XP and level, only loading it if it hasn't been loaded yet"""
        if not hasattr(self, "level"):
            yield from self.load_level()

    @asyncio.coroutine
    def load_rank(self, region, season=-1):
        """|coro|
        Loads the players rank for this region and season

        Parameters
        ----------
        region : str
            the name of the region you want to get the rank for
        season : Optional[int]
            the season you want to get the rank for (defaults to -1, latest season)

        Returns
        -------
        :class:`Rank`
            the players rank for this region and season"""
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/%s/r6karma/players?board_id=pvp_ranked&profile_ids=%s&region_id=%s&season_id=%s" % (self.spaceid, self.platform_url, self.id, region, season))

        if "players" in data and self.id in data["players"]:
            regionkey = "%s:%s" % (region, season)
            self.ranks[regionkey] = Rank(data["players"][self.id])
            return self.ranks[regionkey]
        else:
            raise InvalidRequest("Missing players key in returned JSON object %s" % str(data))

    @asyncio.coroutine
    def get_rank(self, region, season=-1):
        """|coro|

        Checks the players rank for this region, only loading it if it hasn't already been found

        Parameters
        ----------
        region : str
            the name of the region you want to get the rank for
        season : Optional[int]
            the season you want to get the rank for (defaults to -1, latest season)

        Returns
        -------
        :class:`Rank`
            the players rank for this region and season"""
        cache_key = "%s:%s" % (region, season)
        if cache_key in self.ranks:
            return self.ranks[cache_key]

        result = yield from self.load_rank(region, season)
        return result

    @asyncio.coroutine
    def load_operator(self, operator):
        """|coro|

        Loads the players stats for the operator

        Parameters
        ----------
        operator : str
            the name of the operator

        Returns
        -------
        :class:`Operator`
            the operator object found"""
        operator_key = "operatorpvp_" + operator.lower() + "_" + OperatorStatistics[operator.upper()]
        if operator.lower() == "jackal" or operator.lower() == "mira":
            operator_key = "operatorpvp_" + OperatorStatistics[operator.upper()]

        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/%s/playerstats2/statistics?populations=%s&statistics=operatorpvp_kills,operatorpvp_death,operatorpvp_roundwon,operatorpvp_roundlost,operatorpvp_meleekills,operatorpvp_totalxp,operatorpvp_headshot,operatorpvp_timeplayed,operatorpvp_dbno,%s" % (self.spaceid, self.platform_url, self.id, operator_key))

        if not "results" in data or not self.id in data["results"]:
            raise InvalidRequest("Missing results key in returned JSON object %s" % str(data))

        data = data["results"][self.id]

        location = None
        for x in data:
            if x.startswith(operator_key) and data[x] != 0:
                location = ":".join(x.split(":")[1:3])
                break

        data = {x.split(":")[0].split("_")[1]: data[x] for x in data if x is not None and location in x}
        if len(data) < 5:
            raise InvalidRequest("invalid number of results for operator in JSON object %s" % data)

        oper = Operator(operator, data)
        self.operators[operator] = oper
        return oper

    @asyncio.coroutine
    def get_operator(self, operator):
        """|coro|

        Checks the players stats for this operator, only loading them if they haven't already been found

        Parameters
        ----------
        operator : str
            the name of the operator

        Returns
        -------
        :class:`Operator`
            the operator object found"""
        if operator in self.operators:
            return self.operators[operator]

        result = yield from self.load_operator(operator)
        return result

    @asyncio.coroutine
    def load_weapons(self):
        """|coro|

        Load the players weapon stats

        Returns
        -------
        list[:class:`Weapon`]
            list of all the weapon objects found"""
        data = yield from self.auth.get("https://public-ubiservices.ubi.com/v1/spaces/%s/sandboxes/%s/playerstats2/statistics?populations=%s&statistics=weapontypepvp_kills,weapontypepvp_headshot,weapontypepvp_bulletfired,weapontypepvp_bullethit" % (self.spaceid, self.platform_url, self.id))

        if not "results" in data or not self.id in data["results"]:
            raise InvalidRequest("Missing key results in returned JSON object %s" % str(data))

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
        """|coro|

        Check the players weapon stats, only loading them if they haven't already been found

        Returns
        -------
        list[:class:`Weapon`]
            list of all the weapon objects found"""
        if len(self.weapons) == 0:
            yield from self.load_weapons()
        return self.weapons

    @asyncio.coroutine
    def load_gamemodes(self):
        """|coro|

        Loads the players gamemode stats

        Returns
        -------
        dict
            dict of all the gamemodes found (gamemode_name: :class:`Gamemode`)"""

        stats = yield from self._fetch_statistics("secureareapvp_matchwon", "secureareapvp_matchlost", "secureareapvp_matchplayed",
                                                  "secureareapvp_bestscore", "rescuehostagepvp_matchwon", "rescuehostagepvp_matchlost",
                                                  "rescuehostagepvp_matchplayed", "rescuehostagepvp_bestscore", "plantbombpvp_matchwon",
                                                  "plantbombpvp_matchlost", "plantbombpvp_matchplayed", "plantbombpvp_bestscore",
                                                  "generalpvp_servershacked", "generalpvp_serverdefender", "generalpvp_serveraggression",
                                                  "generalpvp_hostagerescue", "generalpvp_hostagedefense")

        self.gamemodes = {x: Gamemode(x) for x in GamemodeNames}
        for name in self.gamemodes:
            statname, gamemode = name + "pvp_", self.gamemodes[name]

            gamemode.best_score = stats.get(statname + "bestscore", 0)
            gamemode.lost = stats.get(statname + "matchlost", 0)
            gamemode.won = stats.get(statname + "matchwon", 0)
            gamemode.played = stats.get(statname + "matchplayed", 0)

            if name == "securearea":
                gamemode.areas_secured = stats.get("generalpvp_servershacked", 0)
                gamemode.areas_defended = stats.get("generalpvp_serverdefender", 0)
                gamemode.areas_contested = stats.get("generalpvp_serveraggression", 0)
            elif name == "rescuehostage":
                gamemode.hostages_rescued = stats.get("generalpvp_hostagerescue", 0)
                gamemode.hostages_defended = stats.get("generalpvp_hostagedefense", 0)



        return self.gamemodes

    @asyncio.coroutine
    def check_gamemodes(self):
        """|coro|

        Checks the players gamemode stats, only loading them if they haven't already been found

        Returns
        -------
        dict
            dict of all the gamemodes found (gamemode_name: :class:`Gamemode`)"""
        if len(self.gamemodes) == 0:
            yield from self.load_gamemodes()
        return self.gamemodes

    @asyncio.coroutine
    def load_general(self):
        """|coro|

        Loads the players general stats"""

        stats = yield from self._fetch_statistics("generalpvp_timeplayed", "generalpvp_matchplayed", "generalpvp_matchwon",
                                                  "generalpvp_matchlost", "generalpvp_kills", "generalpvp_death",
                                                  "generalpvp_bullethit", "generalpvp_bulletfired", "generalpvp_killassists",
                                                  "generalpvp_revive", "generalpvp_headshot", "generalpvp_penetrationkills",
                                                  "generalpvp_meleekills", "generalpvp_dbnoassists", "generalpvp_suicide",
                                                  "generalpvp_barricadedeployed", "generalpvp_reinforcementdeploy", "generalpvp_totalxp",
                                                  "generalpvp_rappelbreach", "generalpvp_distancetravelled", "generalpvp_revivedenied",
                                                  "generalpvp_dbno", "generalpvp_gadgetdestroy", "generalpvp_blindkills")

        statname = "generalpvp_"
        self.deaths = stats.get(statname + "death", 0)
        self.penetration_kills = stats.get(statname + "penetrationkills", 0)
        self.matches_won = stats.get(statname + "matchwon", 0)
        self.bullets_hit = stats.get(statname + "bullethit", 0)
        self.melee_kills = stats.get(statname + "meleekills", 0)
        self.bullets_fired = stats.get(statname + "bulletfired", 0)
        self.matches_played = stats.get(statname + "matchplayed", 0)
        self.kill_assists = stats.get(statname + "killassists", 0)
        self.time_played = stats.get(statname + "timeplayed", 0)
        self.revives = stats.get(statname + "revive", 0)
        self.kills = stats.get(statname + "kills", 0)
        self.headshots = stats.get(statname + "headshot", 0)
        self.matches_lost = stats.get(statname + "matchlost", 0)
        self.dbno_assists = stats.get(statname + "dbnoassists", 0)
        self.suicides = stats.get(statname + "suicide", 0)
        self.barricades_deployed = stats.get(statname + "barricadedeployed", 0)
        self.reinforcements_deployed = stats.get(statname + "reinforcementdeploy", 0)
        self.total_xp = stats.get(statname + "totalxp", 0)
        self.rappel_breaches = stats.get(statname + "rappelbreach", 0)
        self.distance_travelled = stats.get(statname + "distancetravelled", 0)
        self.revives_denied = stats.get(statname + "revivedenied", 0)
        self.dbnos = stats.get(statname + "dbno", 0)
        self.gadgets_destroyed = stats.get(statname + "gadgetdestroy", 0)
        self.blind_kills = stats.get(statname + "blindkills")


    @asyncio.coroutine
    def check_general(self):
        """|coro|

        Checks the players general stats, only loading them if they haven't already been found"""
        if not hasattr(self, "kills"):
            yield from self.load_general()

    @asyncio.coroutine
    def load_queues(self):
        """|coro|

        Loads the players game queues"""

        stats = yield from self._fetch_statistics("casualpvp_matchwon", "casualpvp_matchlost", "casualpvp_timeplayed",
                                                  "casualpvp_matchplayed", "casualpvp_kills", "casualpvp_death",
                                                  "rankedpvp_matchwon", "rankedpvp_matchlost", "rankedpvp_timeplayed",
                                                  "rankedpvp_matchplayed", "rankedpvp_kills", "rankedpvp_death")

        self.ranked = GameQueue("ranked")
        self.casual = GameQueue("casual")

        for gq in (self.ranked, self.casual):
            statname = gq.name + "pvp_"

            gq.won = stats.get(statname + "matchwon", 0)
            gq.lost = stats.get(statname + "matchlost", 0)
            gq.time_played = stats.get(statname + "timeplayed", 0)
            gq.played = stats.get(statname + "matchplayed", 0)
            gq.kills = stats.get(statname + "kills", 0)
            gq.deaths = stats.get(statname + "death", 0)


    @asyncio.coroutine
    def check_queues(self):
        """|coro|

        Checks the players game queues, only loading them if they haven't already been found"""
        if self.casual is None:
            yield from self.load_queues()

    @asyncio.coroutine
    def load_terrohunt(self):
        """|coro|

        Loads the player's general stats for terrorist hunt"""
        stats = yield from self._fetch_statistics("generalpve_dbnoassists", "generalpve_death", "generalpve_revive",
                                                  "generalpve_matchwon", "generalpve_suicide", "generalpve_servershacked",
                                                  "generalpve_serverdefender", "generalpve_barricadedeployed", "generalpve_reinforcementdeploy",
                                                  "generalpve_kills", "generalpve_hostagedefense", "generalpve_bulletfired",
                                                  "generalpve_matchlost", "generalpve_killassists", "generalpve_totalxp",
                                                  "generalpve_hostagerescue", "generalpve_penetrationkills", "generalpve_meleekills",
                                                  "generalpve_rappelbreach", "generalpve_distancetravelled", "generalpve_matchplayed",
                                                  "generalpve_serveraggression", "generalpve_timeplayed", "generalpve_revivedenied",
                                                  "generalpve_dbno", "generalpve_bullethit", "generalpve_blindkills", "generalpve_headshot",
                                                  "generalpve_gadgetdestroy", "generalpve_accuracy")

        self.terrorist_hunt = GameQueue("terrohunt")

        statname = "generalpve_"
        self.terrorist_hunt.deaths = stats.get(statname + "death", 0)
        self.terrorist_hunt.penetration_kills = stats.get(statname + "penetrationkills", 0)
        self.terrorist_hunt.matches_won = stats.get(statname + "matchwon", 0)
        self.terrorist_hunt.bullets_hit = stats.get(statname + "bullethit", 0)
        self.terrorist_hunt.melee_kills = stats.get(statname + "meleekills", 0)
        self.terrorist_hunt.bullets_fired = stats.get(statname + "bulletfired", 0)
        self.terrorist_hunt.matches_played = stats.get(statname + "matchplayed", 0)
        self.terrorist_hunt.kill_assists = stats.get(statname + "killassists", 0)
        self.terrorist_hunt.time_played = stats.get(statname + "timeplayed", 0)
        self.terrorist_hunt.revives = stats.get(statname + "revive", 0)
        self.terrorist_hunt.kills = stats.get(statname + "kills", 0)
        self.terrorist_hunt.headshots = stats.get(statname + "headshot", 0)
        self.terrorist_hunt.matches_lost = stats.get(statname + "matchlost", 0)
        self.terrorist_hunt.dbno_assists = stats.get(statname + "dbnoassists", 0)
        self.terrorist_hunt.suicides = stats.get(statname + "suicide", 0)
        self.terrorist_hunt.barricades_deployed = stats.get(statname + "barricadedeployed", 0)
        self.terrorist_hunt.reinforcements_deployed = stats.get(statname + "reinforcementdeploy", 0)
        self.terrorist_hunt.total_xp = stats.get(statname + "totalxp", 0)
        self.terrorist_hunt.rappel_breaches = stats.get(statname + "rappelbreach", 0)
        self.terrorist_hunt.distance_travelled = stats.get(statname + "distancetravelled", 0)
        self.terrorist_hunt.revives_denied = stats.get(statname + "revivedenied", 0)
        self.terrorist_hunt.dbnos = stats.get(statname + "dbno", 0)
        self.terrorist_hunt.gadgets_destroyed = stats.get(statname + "gadgetdestroy", 0)
        self.terrorist_hunt.areas_secured = stats.get(statname + "servershacked", 0)
        self.terrorist_hunt.areas_defended = stats.get(statname + "serverdefender", 0)
        self.terrorist_hunt.areas_contested = stats.get(statname + "serveraggression", 0)
        self.terrorist_hunt.hostages_rescued = stats.get(statname + "hostagerescue", 0)
        self.terrorist_hunt.hostages_defended = stats.get(statname + "hostagedefense", 0)
        self.terrorist_hunt.blind_kills = stats.get(statname + "blindkills", 0)

        return self.terrorist_hunt

    @asyncio.coroutine
    def check_terrohunt(self):
        """|coro|

        Checks the players general stats for terrorist hunt, only loading them if they haven't been loaded already"""
        if self.terrorist_hunt is None:
            yield from self.load_terrohunt()
        return self.terrorist_hunt

