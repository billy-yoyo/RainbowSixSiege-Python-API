"""
Copyright (c) 2016-2019 billyoyo

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

from .players import Player, PlayerBatch
from .exceptions import *


class Auth:
    """Holds your authentication information. Used to retrieve Player objects
    Once you're done with the auth object, auth.close() should be called.

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
    refresh_session_period : Optional[int]
        How frequently the http session should be refreshed, in seconds. Negative number for never. Defaults to 3 minutes.

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

    def __init__(self, email=None, password=None, token=None, appid=None,
                 cachetime=120, max_connect_retries=1, session=None,
                 refresh_session_period=180):
        if session is not None:
            self.session = session
        else:
            self.session = aiohttp.ClientSession()

        self.max_connect_retries = max_connect_retries
        self.refresh_session_period = refresh_session_period

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
        self.genome = ""

        self.cachetime = cachetime
        self.cache={}

        self._login_cooldown = 0
        self._session_start = time.time()

    @asyncio.coroutine
    def close(self):
        """|coro|
        
        Closes the session associated with the auth object"""
        yield from self.session.close()

    @asyncio.coroutine
    def refresh_session(self):
        """|coro|

        Closes the current session and opens a new one"""
        if self.session:
            try:
                yield from self.session.close()
            except:
                # we don't care if closing the session does nothing
                pass 

        self.session = aiohttp.ClientSession()
        self._session_start = time.time()

    @asyncio.coroutine
    def _ensure_session_valid(self):
        if not self.session:
            yield from self.refresh_session()
        elif self.refresh_session_period >= 0 and time.time() - self._session_start >= self.refresh_session_period:
            yield from self.refresh_session()

    @asyncio.coroutine
    def get_session(self):
        """|coro|
        
        Retrieves the current session, ensuring it's valid first"""
        yield from self._ensure_session_valid()
        return self.session

    @asyncio.coroutine
    def connect(self):
        """|coro|

        Connect to ubisoft, automatically called when needed"""
        if time.time() < self._login_cooldown:
            raise FailedToConnect("login on cooldown")

        session = yield from self.get_session()
        resp = yield from session.post("https://public-ubiservices.ubi.com/v3/profiles/sessions", headers = {
            "Content-Type": "application/json",
            "Ubi-AppId": self.appid,
            "Authorization": "Basic " + self.token
        }, data=json.dumps({"rememberMe": True}))

        data = yield from resp.json()

        message = "Unknown Error"
        if "message" in data and "httpCode" in data:
            message = "HTTP %s: %s" % (data["httpCode"], data["message"])
        elif "message" in data:
            message = data["message"]
        elif "httpCode" in data:
            message = str(data["httpCode"])

        if "ticket" in data:
            self.key = data.get("ticket")
            self.sessionid = data.get("sessionId")
            self.uncertain_spaceid = data.get("spaceId")
        else:
            raise FailedToConnect(message)

    @asyncio.coroutine
    def get(self, *args, retries=0, referer=None, json=True, **kwargs):
        if not self.key:
            last_error = None
            for i in range(self.max_connect_retries):
                try:
                    yield from self.connect()
                    break
                except FailedToConnect as e:
                    last_error = e
            else:
                # assume this error is going uncaught, so we close the session
                yield from self.close()

                if last_error:
                    raise last_error
                else:
                    raise FailedToConnect("Unknown Error")

        if "headers" not in kwargs: kwargs["headers"] = {}
        kwargs["headers"]["Authorization"] = "Ubi_v1 t=" + self.key
        kwargs["headers"]["Ubi-AppId"] = self.appid
        kwargs["headers"]["Ubi-SessionId"] = self.sessionid
        kwargs["headers"]["Connection"] = "keep-alive"
        if referer is not None:
            if isinstance(referer, Player):
                referer = "https://game-rainbow6.ubi.com/en-gb/uplay/player-statistics/%s/multiplayer" % referer.id
            kwargs["headers"]["Referer"] = str(referer)

        session = yield from self.get_session()
        resp = yield from session.get(*args, **kwargs)

        if json:
            try:
                data = yield from resp.json()
            except:
                text = yield from resp.text()

                message = text.split("h1>")
                if len(message) > 1:
                    message = message[1][:-2]
                    code = 0
                    if "502" in message: code = 502
                else:
                    message = text

                raise InvalidRequest("Received a text response, expected JSON response. Message: %s" % message, code=code)

            if "httpCode" in data:
                if data["httpCode"] == 401:
                    if retries >= self.max_connect_retries:
                        # wait 30 seconds before sending another request
                        self._login_cooldown = time.time() + 30

                    # key no longer works, so remove key and let the following .get() call refresh it
                    self.key = None
                    result = yield from self.get(*args, retries=retries+1, **kwargs)
                    return result
                else:
                    msg = data.get("message", "")
                    if data["httpCode"] == 404: msg = "Missing resource %s" % data.get("resource", args[0])
                    raise InvalidRequest("HTTP %s: %s" % (data["httpCode"], msg), code=data["httpCode"])

            return data
        else:
            text = yield from resp.text()
            return text

    @asyncio.coroutine
    def get_players(self, name=None, platform=None, uid=None):
        """|coro|

        get a list of players matching the term on that platform,
        exactly one of uid and name must be given, platform must be given,
        this list almost always has only 1 element, so it's easier to use get_player

        Parameters
        ----------
        name : str
            the name of the player you're searching for
        platform : str
            the name of the platform you're searching on (See :class:`Platforms`)
        uid : str
            the uid of the player you're searching for

        Returns
        -------
        list[:class:`Player`]
            list of found players"""

        if name is None and uid is None:
            raise TypeError("name and uid are both None, exactly one must be given")

        if name is not None and uid is not None:
            raise TypeError("cannot search by uid and name at the same time, please give one or the other")

        if platform is None:
            raise TypeError("platform cannot be None")

        if "platform" not in self.cache: self.cache[platform] = {}

        if name:
            cache_key = "NAME:%s" % name
        else:
            cache_key = "UID:%s" % uid

        if cache_key in self.cache[platform]:
            if self.cachetime > 0 and self.cache[platform][cache_key][0] < time.time():
                del self.cache[platform][cache_key]
            else:
                return self.cache[platform][cache_key][1]

        if name:
            data = yield from self.get("https://public-ubiservices.ubi.com/v3/profiles?nameOnPlatform=%s&platformType=%s" % (parse.quote(name), parse.quote(platform)))
        else:
            data = yield from self.get("https://public-ubiservices.ubi.com/v3/users/%s/profiles?platformType=%s" % (uid, parse.quote(platform)))

        if "profiles" in data:
            results = [Player(self, x) for x in data["profiles"] if x.get("platformType", "") == platform]
            if len(results) == 0: raise InvalidRequest("No results")
            if self.cachetime != 0:
                self.cache[platform][cache_key] = [time.time() + self.cachetime, results]
            return results
        else:
            raise InvalidRequest("Missing key profiles in returned JSON object %s" % str(data))

    @asyncio.coroutine
    def get_player(self, name=None, platform=None, uid=None):
        """|coro|

        Calls get_players and returns the first element,
        exactly one of uid and name must be given, platform must be given

        Parameters
        ----------
        name : str
            the name of the player you're searching for
        platform : str
            the name of the platform you're searching on (See :class:`Platforms`)
        uid : str
            the uid of the player you're searching for

        Returns
        -------
        :class:`Player`
            player found"""

        results = yield from self.get_players(name=name, platform=platform, uid=uid)
        return results[0]

    @asyncio.coroutine
    def get_player_batch(self, names=None, platform=None, uids=None):
        """|coro|
        
        Calls get_player for each name and uid you give, and creates a player batch out of
        all the resulting player objects found. See :class:`PlayerBatch` for how to use this.

        Parameters
        ----------
        names : list[str]
            a list of player names to add to the batch, can be none
        uids : list[str]
            a list of player uids to add to the batch, can be none
        platform : str
            the name of the platform you're searching for players on (See :class:`Platforms`)

        Returns
        -------
        :class:`PlayerBatch`
            the player batch
        """
        if names is None and uids is None:
            raise TypeError("names and uids are both None, at least one must be given")

        players = {}

        if names is not None:
            for name in names:
                player = yield from self.get_player(name=name, platform=platform)
                players[player.id] = player

        if uids is not None:
            for uid in uids:
                player = yield from self.get_player(uid=uid, platform=platform)
                players[player.id] = player
        
        return PlayerBatch(players)
