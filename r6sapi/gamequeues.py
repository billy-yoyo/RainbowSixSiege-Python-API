"""
Copyright (c) 2016-2019 billyoyo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
    def __init__(self, name, stats=None):
        self.name = name

        statname = name + "pvp_"

        stats = stats or {}
        self.won = stats.get(statname + "matchwon", 0)
        self.lost = stats.get(statname + "matchlost", 0)
        self.time_played = stats.get(statname + "timeplayed", 0)
        self.played = stats.get(statname + "matchplayed", 0)
        self.kills = stats.get(statname + "kills", 0)
        self.deaths = stats.get(statname + "death", 0)

    @property
    def wins(self):
        return self.won

    @property
    def losses(self):
        return self.lost