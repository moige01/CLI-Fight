from abc import ABC, abstractmethod

from cli_figth.lib.player import PlayerActions, RawPlayerActions


class ActionsParserBase(ABC):
    @abstractmethod
    def load_raw_player_actions(self, actions: RawPlayerActions) -> None:
        return NotImplemented

    @abstractmethod
    def parse_actions(self) -> None:
        return NotImplemented

    @abstractmethod
    def get_parsed_actions(self) -> PlayerActions:
        return NotImplemented
