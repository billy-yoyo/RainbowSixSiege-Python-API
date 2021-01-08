"""
Copyright (c) 2016-2019 billyoyo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from r6sapi.definitions.models import RankInfo
from r6sapi.definitions.stores import Seasons

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
             "Copper 5",   "Copper 4",   "Copper 3",   "Copper 2",   "Copper 1",
             "Bronze 5",   "Bronze 4",   "Bronze 3",   "Bronze 2",   "Bronze 1",
             "Silver 5",   "Silver 4",   "Silver 3",   "Silver 2",   "Silver 1",
             "Gold 3",     "Gold 2",     "Gold 1",
             "Platinum 3", "Platinum 2", "Platinum 1", 
             "Diamond",
             "Champion"]

    # DEPRACATED
    RANK_CHARMS = [
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20copper%20charm.44c1ede2.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20bronze%20charm.5edcf1c6.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20silver%20charm.adde1d01.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20gold%20charm.1667669d.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20platinum%20charm.d7f950d5.png",
        "https://ubistatic-a.akamaihd.net/0058/prod/assets/images/season02%20-%20diamond%20charm.e66cad88.png"
    ]

    COMPLETE_RANK_ICONS = [
        # unranked
        [
            "https://i.imgur.com/sB11BIz.png",  # unranked
        ],
        # copper
        [
            "https://i.imgur.com/0J0jSWB.jpg",  # copper 1
            "https://i.imgur.com/eI11lah.jpg",  # copper 2
            "https://i.imgur.com/6CxJoMn.jpg",  # copper 3
            "https://i.imgur.com/ehILQ3i.jpg",  # copper 4
            "https://i.imgur.com/B8NCTyX.png",  # copper 5
        ],
        # bronze
        [
            "https://i.imgur.com/hmPhPBj.jpg",  # bronze 1
            "https://i.imgur.com/9AORiNm.jpg",  # bronze 2
            "https://i.imgur.com/QD5LYD7.jpg",  # bronze 3
            "https://i.imgur.com/42AC7RD.jpg",  # bronze 4
            "https://i.imgur.com/TIWCRyO.png"   # bronze 5
        ],
        # silver
        [
            "https://i.imgur.com/KmFpkNc.jpg",  # silver 1
            "https://i.imgur.com/EswGcx1.jpg",  # silver 2
            "https://i.imgur.com/m8GToyF.jpg",  # silver 3
            "https://i.imgur.com/D36ZfuR.jpg",  # silver 4
            "https://i.imgur.com/PY2p17k.png",  # silver 5
        ],
        # gold
        [
            "https://i.imgur.com/ffDmiPk.jpg",  # gold 1
            "https://i.imgur.com/ELbGMc7.jpg",  # gold 2
            "https://i.imgur.com/B0s1o1h.jpg",  # gold 3,
            "https://i.imgur.com/6Qg6aaH.jpg",  # gold 4
        ],
        # platinum
        [
            "https://i.imgur.com/qDYwmah.png",  # plat 1
            "https://i.imgur.com/CYMO3Er.png",  # plat 2
            "https://i.imgur.com/tmcWQ6I.png",  # plat 3
        ],
        # diamond
        [
            "https://i.imgur.com/37tSxXm.png",  # diamond
        ],
        # champion
        [
            "https://i.imgur.com/VlnwLGk.png",  # champion
        ]
    ]

    RANK_ICONS = [
        COMPLETE_RANK_ICONS[0][0], # unranked

        COMPLETE_RANK_ICONS[1][4], # copper 5
        COMPLETE_RANK_ICONS[1][3], # copper 4
        COMPLETE_RANK_ICONS[1][2], # copper 3
        COMPLETE_RANK_ICONS[1][1], # copper 2
        COMPLETE_RANK_ICONS[1][0], # copper 1

        COMPLETE_RANK_ICONS[2][4], # bronze 5
        COMPLETE_RANK_ICONS[2][3], # bronze 4
        COMPLETE_RANK_ICONS[2][2], # bronze 3
        COMPLETE_RANK_ICONS[2][1], # bronze 2
        COMPLETE_RANK_ICONS[2][0], # bronze 1

        COMPLETE_RANK_ICONS[3][4], # silver 5
        COMPLETE_RANK_ICONS[3][3], # silver 4
        COMPLETE_RANK_ICONS[3][2], # silver 3
        COMPLETE_RANK_ICONS[3][1], # silver 2
        COMPLETE_RANK_ICONS[3][0], # silver 1

        COMPLETE_RANK_ICONS[4][2], # gold 3
        COMPLETE_RANK_ICONS[4][1], # gold 2
        COMPLETE_RANK_ICONS[4][0], # gold 1

        COMPLETE_RANK_ICONS[5][2], # platinum 3
        COMPLETE_RANK_ICONS[5][1], # platinum 2
        COMPLETE_RANK_ICONS[5][0], # platinum 1

        COMPLETE_RANK_ICONS[6][0], # diamond
        
        COMPLETE_RANK_ICONS[7][0], # champion
    ]

    

    @staticmethod
    def bracket_from_rank(rank_id):
        if rank_id == 0: return -1   # unranked
        elif rank_id <= 5: return 0  # copper
        elif rank_id <= 10: return 1 # bronze
        elif rank_id <= 15: return 2 # silver
        elif rank_id <= 18: return 3 # gold
        elif rank_id <= 21: return 4 # platinum
        elif rank_id <= 22: return 5 # diamond
        else: return 6               # champion

    @staticmethod
    def bracket_name(bracket):
        if bracket == -1: return "Unranked"
        elif bracket == 0: return "Copper"
        elif bracket == 1: return "Bronze"
        elif bracket == 2: return "Silver"
        elif bracket == 3: return "Gold"
        elif bracket == 4: return "Platinum"
        elif bracket == 5: return "Diamond"
        else: return "Champion"

    UNRANKED = -1
    COPPER = 0
    BRONZE = 1
    SILVER = 2
    GOLD = 3
    PLATINUM = 4
    DIAMOND = 5
    CHAMPION = 6

    def __init__(self, data, rank_definitions):
        """

        Parameters
        ----------
        data
        rank_definitions: :class:`RankInfoCollection`
        """
        self._rank_definitions = rank_definitions
        self._new_ranks_threshold = 14

        self.max_mmr = data.get("max_mmr")
        self.mmr = data.get("mmr")
        self.wins = data.get("wins")
        self.losses = data.get("losses")

        self.rank_id = data.get("rank", 0)
        self.rank = rank_definitions.get_rank(self.rank_id)

        self.max_rank = data.get("max_rank")
        self.next_rank_mmr = data.get("next_rank_mmr")
        self.season = data.get("season")
        self.region = data.get("region")
        self.abandons = data.get("abandons")
        self.skill_mean = data.get("skill_mean")
        self.skill_stdev = data.get("skill_stdev")

    @property
    def _season_definitions(self):
        if self.season >= len(self._rank_definitions):
            return self._rank_definitions.last_season
        return self._rank_definitions[self.season]

    def get_icon_url(self):
        """Get URL for this rank's icon

        Returns
        -------
        :class:`str`
            the URL for the rank icon"""

        if self.season > self._new_ranks_threshold:
            return Rank.RANK_ICONS[self.rank_id]

        bracket = self.get_bracket()
        rank_index = self._get_bracket_rank_index()

        print("getting icon url for bracket=%s, rank_index=%s (rank = %s)" % (bracket, rank_index, self.get_rank_name()))

        return Rank.COMPLETE_RANK_ICONS[bracket + 1][rank_index]

    # DEPRACATED
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

    def get_bracket(self, rank_id=None):
        """Get rank bracket

        Returns
        -------
        :class:`int`
            the id for the rank bracket this rank is in

        """
        rank_id = rank_id if rank_id is not None else self.rank_id

        if self.season > self._new_ranks_threshold:
            return Rank.bracket_from_rank(rank_id)

        for i, division in enumerate(self._season_definitions["divisions"]):
            if rank_id in division["ranks"]:
                return i
        return -1

    def get_bracket_name(self, rank_id=None):
        """Get rank bracket name

        Returns
        -------
        :class:`str`
            the name for the rank bracket this rank is in
        """
        bracket = self.get_bracket(rank_id=rank_id)

        if self.season > self._new_ranks_threshold:
            return Rank.bracket_name(bracket)
        
        if bracket < 0:
            return "Unranked"
        return self._season_definitions["divisions"][bracket]["id"].title()

    def _get_bracket_rank_index(self, rank_id=None):
        """Gets the rank index within the bracket (e.g. 0 for gold 1), returns -1 if it failed to find rank index

        Returns
        -------
        :class:`int`
            the rank index within the bracket
        """
        rank_id = rank_id if rank_id is not None else self.rank_id

        bracket = self.get_bracket(rank_id=rank_id)

        ranks = self._season_definitions["divisions"][bracket]["ranks"]

        rank_index = -1
        for i, rid in enumerate(ranks):
            if rid == rank_id:
                rank_index = len(ranks) - (i + 1)
                break
        
        return rank_index

    def get_rank_name(self, rank_id=None):
        """Get rank name

        Returns
        -------
        :class:`str`
            the name for this rank
        """
        rank_id = rank_id if rank_id is not None else self.rank_id

        if self.season > self._new_ranks_threshold:
            return Rank.RANKS[rank_id]

        bracket_name = self.get_bracket_name(rank_id)
        rank_index = self._get_bracket_rank_index(rank_id)
                
        if bracket_name.lower() in ["unranked", "diamond", "champion"]:
            return bracket_name

        return "%s %s" % (bracket_name, rank_index + 1)

    def get_max_rank_name(self):
        """Get rank name of max rank

        Returns
        -------
        :class:`str`
            the name for this rank
        """
        return self.get_rank_name(self.max_rank) 