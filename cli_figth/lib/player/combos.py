from cli_figth.lib import RepeatedCombo
from collections import UserList
from collections.abc import Iterable

from typing import NamedTuple


class Combo(NamedTuple):
    movement: str
    attack: str
    energy: int
    name: str

    def __eq__(self, other) -> bool:
        """A combo should be equal if either attacks and moves or name are the same.

        This would be avoid repeated combos on a ComboList.

        Args:
            other (Combo)

        Raises:
            ValueError: A Combo can only be compared with another Combo

        Returns:
            bool
        """

        if not isinstance(other, Combo):
            raise ValueError

        return (self.movement == other.movement and self.attack == other.attack) or self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)


class CombosList(UserList):
    def __init__(self, initlist=None):
        if initlist is not None:
            if isinstance(initlist, Iterable):
                for item in initlist:
                    self._assert_type(item)
            else:
                raise ValueError('Please, provide an iterable of Combo')

        super().__init__(initlist)

    def __setitem__(self, *, i: int, combo: Combo) -> None:
        self._validate_combo(combo)

        return super().__setitem__(i, combo)

    def append(self, item: Combo) -> None:
        self._validate_combo(item)

        return super().append(item)

    def insert(self, i: int, item: Combo) -> None:
        self._validate_combo(item)

        return super().insert(i, item)

    def _assert_type(self, combo: Combo, /) -> None:
        if not isinstance(combo, Combo):
            raise ValueError

    def _validate_combo(self, combo: Combo, /) -> None:
        self._assert_type(combo)

        if self.have_combo(combo):
            raise RepeatedCombo

    def have_combo(self, hipotetic_combo: Combo, /) -> bool:
        return super().__contains__(hipotetic_combo)

    def get_combo_by_attack_and_movements(self, combo: Combo, /) -> Combo | None:
        self._assert_type(combo)

        item: Combo

        for item in self.data:
            if item.movement == combo.movement and item.attack == combo.attack:
                return item

        return None
