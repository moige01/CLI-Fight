from abc import ABC, abstractmethod
from cli_figth.lib.player import Player, PlayerAction


class ActionsHanlderBase(ABC):
    @abstractmethod
    def handle_player_action(self, player_one: Player, player_two: Player, action: PlayerAction) -> str:
        return NotImplemented

    @abstractmethod
    def handle_end_match(self, winner: Player) -> str:
        return NotImplemented
