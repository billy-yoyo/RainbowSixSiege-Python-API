"""
These collection classes convert the "raw" definitions of models found in {ranks, seasons, maps}.py
and make it available as a collection of `model` objects
"""
import collections
from typing import Optional
import logging

import dateutil.parser

from r6sapi.definitions.models import Loadout, OperatorInfo, OperatorSide, Season, RankInfo


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
            a Loadouts object containing all the operator's loadouts
        """
        self._name_to_operator = {}
        self._id_to_operator = {}
        for operator_dict in all_operators:
            # seperate out the parts of the dictionary that can be just passed through to the constructor
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

            op = OperatorInfo(**finished_fields, side=side, loadouts=loadouts)
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

            start_date = dateutil.parser.parse(season_dict["startDate"])

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


