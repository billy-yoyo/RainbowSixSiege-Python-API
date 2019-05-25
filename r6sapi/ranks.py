"""
Copyright (c) 2016-2019 billyoyo

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


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
        "https://i.imgur.com/sB11BIz.png",  # unranked
        "https://i.imgur.com/ehILQ3i.jpg",  # copper 4
        "https://i.imgur.com/6CxJoMn.jpg",  # copper 3
        "https://i.imgur.com/eI11lah.jpg",  # copper 2
        "https://i.imgur.com/0J0jSWB.jpg",  # copper 1
        "https://i.imgur.com/42AC7RD.jpg",  # bronze 4
        "https://i.imgur.com/QD5LYD7.jpg",  # bronze 3
        "https://i.imgur.com/9AORiNm.jpg",  # bronze 2
        "https://i.imgur.com/hmPhPBj.jpg",  # bronze 1
        "https://i.imgur.com/D36ZfuR.jpg",  # silver 4
        "https://i.imgur.com/m8GToyF.jpg",  # silver 3
        "https://i.imgur.com/EswGcx1.jpg",  # silver 2
        "https://i.imgur.com/KmFpkNc.jpg",  # silver 1
        "https://i.imgur.com/6Qg6aaH.jpg",  # gold 4
        "https://i.imgur.com/B0s1o1h.jpg",  # gold 3
        "https://i.imgur.com/ELbGMc7.jpg",  # gold 2
        "https://i.imgur.com/ffDmiPk.jpg",  # gold 1
        "https://i.imgur.com/Sv3PQQE.jpg",  # plat 3
        "https://i.imgur.com/Uq3WhzZ.jpg",  # plat 2
        "https://i.imgur.com/xx03Pc5.jpg",  # plat 1
        "https://i.imgur.com/nODE0QI.jpg"   # diamond
    ]

    @staticmethod
    def bracket_from_rank(rank_id):
        if rank_id == 0: return 0
        elif rank_id <= 4: return 1
        elif rank_id <= 8: return 2
        elif rank_id <= 12: return 3
        elif rank_id <= 16: return 4
        elif rank_id <= 19: return 5
        else: return 6

    @staticmethod
    def bracket_name(bracket):
        if bracket == 0: return "Unranked"
        elif bracket == 1: return "Copper"
        elif bracket == 2: return "Bronze"
        elif bracket == 3: return "Silver"
        elif bracket == 4: return "Gold"
        elif bracket == 5: return "Platinum"
        else: return "Diamond"


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
        return Rank.bracket_from_rank(self.rank_id)



