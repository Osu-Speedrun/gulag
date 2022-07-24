from __future__ import annotations

import functools
from enum import IntEnum
from enum import unique

from app.constants.mods import Mods
from app.utils import escape_enum
from app.utils import pymysql_encode

__all__ = (
    "GAMEMODE_REPR_LIST",
    "GameMode",
)

GAMEMODE_REPR_LIST = (
    "vn!std",
    "vn!taiko",
    "vn!catch",
    "vn!mania",
    "rx!std",
    "rx!taiko",
    "rx!catch",
    "rx!mania",  # unused
    "ap!std",
    "ap!taiko",  # unused
    "ap!catch",  # unused
    "ap!mania",  # unused
)

GULAG_2_INT_DEFAULT = {
    "vn!std": 0,
    "vn!taiko": 1,
    "vn!catch": 2,
    "vn!mania": 3,
    "rx!std": 0,
    "rx!taiko": 1,
    "rx!catch": 2,
    "rx!mania": 3,
    "ap!std": 0,
    "ap!taiko": 1,
    "ap!catch": 2,
    "ap!mania": 3,
}

GULAG_2_STR_DEFUALT = {
    "vn!std": "std",
    "vn!taiko": "taiko",
    "vn!catch": "catch",
    "vn!mania": "mania",
    "rx!std": "std",
    "rx!taiko": "taiko",
    "rx!catch": "catch",
    "rx!mania": "mania",
    "ap!std": "std",
    "ap!taiko": "taiko",
    "ap!catch": "catch",
    "ap!mania": "mania",
}
@unique
@pymysql_encode(escape_enum)
class GameMode(IntEnum):
    VANILLA_OSU = 0
    VANILLA_TAIKO = 1
    VANILLA_CATCH = 2
    VANILLA_MANIA = 3

    RELAX_OSU = 4
    RELAX_TAIKO = 5
    RELAX_CATCH = 6
    RELAX_MANIA = 7  # unused

    AUTOPILOT_OSU = 8
    AUTOPILOT_TAIKO = 9  # unused
    AUTOPILOT_CATCH = 10  # unused
    AUTOPILOT_MANIA = 11  # unused

    @classmethod
    @functools.lru_cache(maxsize=32)
    def from_params(cls, mode_vn: int, mods: Mods) -> GameMode:
        mode = mode_vn

        if mods & Mods.AUTOPILOT:
            mode += 8
        elif mods & Mods.RELAX:
            mode += 4

        return cls(mode)

    @functools.cached_property
    def as_vanilla(self) -> int:
        if self.value & self.AUTOPILOT_OSU:
            return self.value - 8
        elif self.value & self.RELAX_OSU:
            return self.value - 4
        else:
            return self.value

    def __repr__(self) -> str:
        return GAMEMODE_REPR_LIST[self.value]
