"""
Use this as a store for all in game operator info, and any info that needs to be stored in player state to allow
for interfacing with the ubi api
"""
from typing import Optional
import logging

from r6sapi.definitions.converters import Loadout, OperatorInfo, OperatorSide
from r6sapi.definitions.loadouts import loadouts_const
from r6sapi.definitions.operators import operators_const


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
            finished_fields = {key: value for key, value in operator_dict.items() if key in ("id", "name", "icon_url", "index", "roles")}
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


loadouts = Loadouts(loadouts_const)
operators = Operators(operators_const, loadouts)
