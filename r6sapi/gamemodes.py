"""
Copyright (c) 2016-2019 billyoyo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

GamemodeNames = {
    "securearea": "Secure Area",
    "rescuehostage": "Hostage Rescue",
    "plantbomb": "Bomb"
}

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
    def __init__(self, gamemodeType, stats=None):
        self.type = gamemodeType
        self.name = GamemodeNames[self.type]

        statname = gamemodeType + "pvp_"

        stats = stats or {}
        self.best_score = stats.get(statname + "bestscore", 0)
        self.lost = stats.get(statname + "matchlost", 0)
        self.won = stats.get(statname + "matchwon", 0)
        self.played = stats.get(statname + "matchplayed", 0)

        if gamemodeType == "securearea":
            self.areas_secured = stats.get("generalpvp_servershacked", 0)
            self.areas_defended = stats.get("generalpvp_serverdefender", 0)
            self.areas_contested = stats.get("generalpvp_serveraggression", 0)
        elif gamemodeType == "rescuehostage":
            self.hostages_rescued = stats.get("generalpvp_hostagerescue", 0)
            self.hostages_defended = stats.get("generalpvp_hostagedefense", 0)

    @property
    def wins(self):
        return self.won

    @property
    def losses(self):
        return self.lost

