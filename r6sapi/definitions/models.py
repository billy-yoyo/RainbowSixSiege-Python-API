"""
Copyright (c) 2016-2020 jackywathy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Classes that convert the raw dict data into a more structured representation
"""
from typing import Iterable, Union

import enum

import r6sapi.definitions


class OperatorSide(enum.Enum):
    attacker = "attacker"
    defender = "defender"


class WeaponType(enum.Enum):
    primary = "primary"
    secondary = "secondary"
    gadget = "gadget"
    unique_ability = "unique_ability"


class Loadout:
    """
    Contains a loadout for 1 weapon. Each operator has several loadouts and loadouts can be shared between operators

    Attributes
    ----------
    id : str
        The id of this weapon. Each loadout with the same gun share the same 'id', e.g. the mk-14-ebr on both dokk and
        aruni have the id `6xDz1HSwIn3ZcV9nKIeKUN` as of the time this documentation was written
    name : str
        the language independent name of this weapon. Generally lowercase english version of the localisedName
    weapon_type : WeaponType
        the type of weapon. Can be PRIMARY of SECONDARY
    weapon_image_url : str
        the URL of the image of this weapon

    """
    def __repr__(self):
        return "Loadout(id='{}', name='{}', weapon_type='{}', weapon_image_url={})".format(self.id, self.name, self.weapon_type, self.weapon_image_url)

    def __eq__(self, other):
        return other.id == self.id and other.name == self.name and other.weapon_type == self.weapon_type and other.weapon_image_url == self.weapon_image_url

    def __init__(self, id, name, weapon_type, weapon_image_url):
        self.id = id
        self.name = name
        if isinstance(weapon_type, WeaponType):
            self.weapon_type = weapon_type
        else:
            self.weapon_type = WeaponType[weapon_type]
        self.weapon_image_url = weapon_image_url

    def __str__(self):
        return self.__repr__()


class OperatorInfo:
    """
    Contains only information describing the operator as it appears in the game file
    This includes weapon loadouts, name, and icon

    The operator's faction name and image are available in the json, however, these are only available
    in a localized fashion and change depending on what language the extracted JSON file is in, so additional
    data processing will be required to remove language dependent features

    Attributes
    ----------
    id : str
        the id of this operator. `should` be unique across all operators
    name : str
        the language independent name of this operator. Generally lowercase english
    icon_url : str
        the url at which the operator's badge or icon can be found
    loadouts : list[:class:`Loadout`]
        a list of loadouts that this operator has access to
    side : OperatorSide
        which side the operator is one (ATK or DEF)
    roles : list[str]
        the operator's roles as returned by the API. Can be incomplete or empty, but generally consists of some of the
        following:
        'secure', 'intel-gathers', 'anchor', 'covering-fire', 'shield',
    index : str
        the `index` of this operator as defined by the v1 ubisoft api. this value is needed to query for operator
        stats
    unique_abilities : Iterable[:class:`UniqueOperatorStat`]
        the unique abilities that only this operator has.
    """
    def __init__(self, id, name, icon_url, loadouts, side, roles, index, unique_abilities):
        """
        Creates a new OperatorInfo object.
        Parameters
        ----------
        gadget_template: Union[str, Iterable[str]]
            the string or strings used to fetch
        """
        self.id = id
        self.name = name
        self.icon_url = icon_url
        self.loadouts = loadouts
        self.side = side
        self.roles = roles
        self.index = index
        self.unique_abilities = tuple(unique_abilities)

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.icon_url == other.icon_url and self.loadouts == r6sapi.definitions.loadouts and self.index == other.index

    def __repr__(self):
        return "OperatorInfo(id='{}', name='{}', icon_url='{}'," \
               "loadouts={}, side={}, roles={}, index={})".format(self.id, self.name, self.icon_url, self.loadouts,
                                                        self.side, self.roles, self.index)

    def __str__(self):
        return self.__repr__()


class RankInfo:
    def __init__(self, name, min_mmr, max_mmr):
        self.name = name
        self.min_mmr = min_mmr
        self.max_mmr = max_mmr


UNRANKED = RankInfo("unranked", -1, -1)
RankInfo.UNRANKED = UNRANKED


class Season:
    """
    Represents a single season
    Attributes
    ----------
    id: the id of the season. Guaranteed to be unique
    season_code: the code name of the season. In the format YaSb, where a and b are the year and season number.
        e.g. Y5S1 for year 5 season 1
    season_ranks: the ranks that that occured in this season. Note that the rank system has been
        reworked multiple time so some seasons have a different set of ranks from others
    operation_name: the full (English) name of the season

    """
    def __init__(self, id, season_code, start_date, season_ranks, operation_name):
        self.id = id
        self.season_code = season_code
        self.start_date = start_date
        self.season_ranks = season_ranks
        self.operation_name = operation_name


class UniqueOperatorStat:
    """
    Unique Statistic for an operator (e.g. how many kills with cap's fire bolt)
    We query the API using a certain magic string, which varies depending on
    Attributes
    ----------
    id_template: str
        template which can be used to construct the full stat name to use
        In the form of `operator{}_smoke_poisongaskill`
    name: str
        the name of the stat e.g. `Gadgets Jammed`
    """
    def __init__(self, id_template, name):
        self.id_template = id_template
        self.name = name

    @property
    def pvp_stat_name(self):
        return self.id_template.format("pvp")

    @property
    def pve_stat_name(self):
        return self.id_template.format("pve")

    def __repr__(self):
        return "UniqueOperatorStat(name={}, id_template={})".format(self.name, self.id_template)

    def __str__(self):
        return repr(self)
