"""
Copyright (c) 2016-2019 billyoyo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

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
    def __init__(self, weaponType, stats=None):
        self.type = weaponType
        self.name = WeaponNames[self.type]
        
        stat_name = lambda name: "weapontypepvp_%s:%s:infinite" % (name, self.type)

        stats = stats or {}
        self.kills = stats.get(stat_name("kills"), 0)
        self.headshots = stats.get(stat_name("headshot"), 0)
        self.hits = stats.get(stat_name("bullethit"), 0)
        self.shots = stats.get(stat_name("bulletfired"), 0)