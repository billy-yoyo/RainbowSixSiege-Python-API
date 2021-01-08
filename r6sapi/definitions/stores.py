"""
Copyright (c) 2016-2020 jackywathy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

These collection classes store a collection of the definition objects that are needed. They convert from the "raw" '
definitions of models found in {ranks, seasons, maps}.py and make it available as a collection of `model` objects in
the class's constructor.

If we use an alternative data store in the future it may be worth refactoring out this logic.
"""
from typing import Optional

import collections
import datetime

import logging

from r6sapi.definitions.models import Loadout, OperatorInfo, OperatorSide, Season, RankInfo, UniqueOperatorStat


class Loadouts:
    """
    Stores all loadouts, providing operations to fetch loadouts depending name and id.
    """
    def __init__(self, all_loadouts):
        """

        Reads a list of loadouts and stores it in this object

        Parameters
        ----------
        all_loadouts: list[dict]
            a list of loadout dictionary objects
        """
        self._name_to_loadout = {}
        self._id_to_loadout = {}
        for loadout_dict in all_loadouts:
            loadout = Loadout(**loadout_dict)
            self._id_to_loadout[loadout.id] = loadout
            self._name_to_loadout[loadout.name.lower()] = loadout

    def from_name(self, name):
        """
        Gets a loadout by the name of the weapon
        Parameters
        ----------
        name

        Returns:
        -------
        Optional[:class:`Loadout`]: the found loadout
        """
        return self._name_to_loadout.get(name.lower())

    def from_id(self, id_):
        """
        Gets a loadout by its id.
        Parameters
        ----------
        id_

        Returns
        -------
        Optional[:class:`Loadout`]

        """
        return self._id_to_loadout.get(id_)


class Operators:
    """
    Stores all operators, providing operations to fetch operators depending on name and id.
    """
    def __init__(self, all_operators, loadouts_store):
        """

        Reads a list of operators and stores it in this object. We also

        Parameters
        ----------
        all_operators: list[dict]
            a list of loadout dictionary objects
        loadouts_store: :class:`Loadouts`
            a Loadouts object containing all the operators' loadouts
        """
        self._name_to_operator = {}
        self._id_to_operator = {}
        for operator_dict in all_operators:
            # separate out the parts of the dictionary that can be just passed through to the constructor
            finished_fields = {
                key: value for key, value in operator_dict.items()
                if key in ("id", "name", "icon_url", "index", "roles")
            }
            side = OperatorSide[operator_dict["side"]]

            # convert the id -> actual loadout objects
            loadouts = []
            for loadout_id in operator_dict["loadouts"]:
                found = loadouts_store.from_id(loadout_id)
                if found is not None:
                    loadouts.append(found)
                else:
                    logging.warning("Skipped a loadout from operator %s with id %s", operator_dict["name"], operator_dict["id"])

            # load in the unique abilities
            op_stats = []
            for ability in operator_dict["unique_stats"]:
                stat = UniqueOperatorStat(ability["id"], ability["name"])
                op_stats.append(stat)

            op = OperatorInfo(**finished_fields, side=side, loadouts=loadouts, unique_abilities=op_stats)
            self._id_to_operator[op.id] = op
            self._name_to_operator[op.name.lower()] = op

    def from_name(self, name):
        """
        Gets a operator by the name of the weapon
        Parameters
        ----------
        name

        Returns
        -------
        Optional[:class:`OperatorInfo`]: the operator with this name
        """
        return self._name_to_operator.get(name.lower())

    def from_id(self, id_):
        """
        Gets a operator by its id.
        Parameters
        ----------
        id_

        Returns
        -------
        Optional[:class:`OperatorInfo`]
        """
        return self._name_to_operator.get(id_)

    def get_all(self):
        """
        Gets all the operators, as a list
        Returns
        list[:class:`OperatorInfo`]
        -------

        """
        return self._name_to_operator.values()


class RankInfoCollection(collections.UserList):
    """
    Basically a list; but supports a couple convenience methods
    """
    def get_rank(self, rank_id):
        if rank_id == 0:
            # taken from bracket_from_rank
            return RankInfo.UNRANKED


class Seasons:
    """

    """
    def __init__(self, all_seasons):
        self._seasons = []
        for season_dict in all_seasons:
            # seperate out the parts of the dictionary that can be just passed through to the constructor
            finished_fields = {key: value for key, value in season_dict.items() if
                               key in ("id", "season_code", "operation_name")}

            season_ranks = RankInfoCollection()
            for rank_dict in season_dict["season_ranks"]:
                season_ranks.append(RankInfo(**rank_dict))

            start_date = datetime.datetime.strptime(season_dict["startDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

            season = Season(**finished_fields, start_date=start_date, season_ranks=season_ranks)

            self._seasons.append(season)

    def from_code(self, code):
        """
        Gets a season by its code name
        Parameters
        ----------
        code

        Returns
        -------
        Optional[:class:`Season`]: the operator with this name
        """
        return next((season for season in self._seasons if season.season_code == code.lower()), None)

    def from_id(self, id_):
        """
        Gets a operator by its id.
        Parameters
        ----------
        id_

        Returns
        -------
        Optional[:class:`Season`]
        """
        return next((season for season in self._seasons if season.id == id_), None)

    def __len__(self):
        return len(self._seasons)

    @property
    def last_season(self):
        return self._seasons[-1]

    def __getitem__(self, item):
        return self._seasons[item]


