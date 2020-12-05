"""
Classes that convert the raw dict data into a more structured representation

"""
import enum


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
    loadouts : list[Loadout]
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
    """
    def __init__(self, id, name, icon_url, loadouts, side, roles, index):
        self.id = id
        self.name = name
        self.icon_url = icon_url
        self.loadouts = loadouts
        self.side = side
        self.roles = roles
        self.index = index

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name and self.icon_url == other.icon_url and self.loadouts == other.loadouts and self.index == other.index

    def __repr__(self):
        return "OperatorInfo(id='{}', name='{}', icon_url='{}'," \
               "loadouts={}, side={}, roles={}, index={})".format(self.id, self.name, self.icon_url, self.loadouts,
                                                        self.side, self.roles, self.index)

    def __str__(self):
        return self.__repr__()
