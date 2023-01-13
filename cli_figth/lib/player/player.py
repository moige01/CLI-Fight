from enum import Enum
from typing import NamedTuple, TypedDict
from dataclasses import dataclass

from cli_figth.lib.player import Combo, CombosList


class Player:
    def __init__(self, *, energy: int, name: str, combos_list: CombosList = None):
        self._energy = energy if isinstance(energy, int) and energy > 0 else 1
        self._name = name

        if combos_list is not None and not isinstance(combos_list, CombosList):
            raise ValueError('Only combos allowed.')

        self._combos_list = combos_list

    def __key(self):
        return (self._name, self._energy)

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            raise ValueError('Player can be only compared wih another player')

        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(self, other)

    def __repr__(self) -> str:
        return f'Player(name={self.name}, energy={self.energy}, combo_list={self.combos_list})'

    @property
    def name(self):
        return self._name

    @property
    def combos_list(self):
        return self._combos_list

    @property
    def energy(self):
        return self._energy

    @combos_list.setter
    def combos_list(self, combos_list: CombosList):
        if not isinstance(combos_list, CombosList):
            raise ValueError

        self._combos_list = combos_list

    def _decrease_energy_by(self, value: int) -> None:
        new_value = self._energy - value

        if new_value < 0:
            self._energy = 0
        else:
            self._energy = abs(new_value)

    def decrease_energy_by(self, value: int) -> None:
        self._decrease_energy_by(value)

    def _is_dead(self) -> bool:
        return self._energy <= 0

    def is_dead(self) -> bool:
        return self._is_dead()


class ActionType(Enum):
    COMBO = 1
    MOVEMENT = 2
    NORMAL_HIT = 3


@dataclass
class PlayerAction():
    player: Player
    moves: str
    attack: str
    hit: bool
    type: ActionType
    combo: Combo | None


PlayerActions = dict[Player, list[PlayerAction]]
RawActions = TypedDict('Actions', { 'movements': list[str], 'attacks': list[str] })
RawPlayerActions = dict[Player, RawActions]
RawPlayer = TypedDict('RawPlayer', {
    'name': str,
    'movements': list[str],
    'attacks': list[str],
    'energy': int,
    'combos_list': CombosList | None,
})
