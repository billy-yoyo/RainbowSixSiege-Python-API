from r6sapi.definitions.converters import Loadouts, Operators, Seasons
from r6sapi.definitions.loadouts import loadouts_const
from r6sapi.definitions.operators import operators_const
from r6sapi.definitions.seasons import seasons_const

loadouts = Loadouts(loadouts_const)
operators = Operators(operators_const, loadouts)
seasons = Seasons(seasons_const)
