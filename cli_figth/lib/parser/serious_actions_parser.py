from itertools import zip_longest

from cli_figth.lib.exceptions import EmptyRawActions
from cli_figth.lib.parser import ActionsParserBase
from cli_figth.lib.player import (
    ActionType,
    RawActions,
    Combo,
    Player,
    PlayerAction,
    PlayerActions,
    RawPlayer,
    RawPlayerActions
)

class SeriousActionsParser(ActionsParserBase):
    def __init__(self) -> None:
        super().__init__()
        self._raw_actions: RawPlayerActions = {}
        self._parsed_actions: PlayerActions = {}

    def load_raw_player_actions(self, player: RawPlayer) -> None:
        if (name := player.get('name')) is None:
            raise ValueError('A player should have name')

        if (energy := player.get('energy')) is None:
            raise ValueError('A player should have energy')

        combos = player.get('combos_list')

        real_player = Player(energy=energy, name=name, combos_list=combos)

        movements = player.get('movements')
        attacks = player.get('attacks')

        if movements is None or attacks is None:
            raise ValueError('Neither movements or attacks could be empty')

        actions = {'movements': movements, 'attacks': attacks}

        self._raw_actions[real_player] = actions

    def parse_actions(self) -> None:
        if not self._raw_actions:
            raise EmptyRawActions

        player: Player
        actions: RawActions
        for (player, actions) in self._raw_actions.items():
            for (moves, attack) in zip_longest(actions.get('movements', []), actions.get('attacks', []), fillvalue=''):
                action = PlayerAction(
                    player=player,
                    moves=moves,
                    attack=attack,
                    hit=False,
                    type=ActionType.MOVEMENT,
                    combo=None
                )
                combo = Combo(movement=moves, attack=attack, energy='', name='')

                if (full_combo := player.combos_list.get_combo_by_attack_and_movements(combo)) is not None:
                    action.hit = True
                    action.type = ActionType.COMBO
                    action.combo = full_combo
                elif attack != '' and (attack == 'P' or attack == 'K'):
                    normal_hit = Combo(
                        movement=moves,
                        attack=attack,
                        energy=1,
                        name='Patada' if attack == 'K' else 'Puño'
                    )

                    action.hit = True
                    action.type = ActionType.NORMAL_HIT
                    action.combo = normal_hit

                if player not in self._parsed_actions:
                    self._parsed_actions[player] = [action]
                else:
                    self._parsed_actions[player].append(action)

        super().parse_actions()

    def get_parsed_actions(self) -> PlayerActions:
        return self._parsed_actions

    def get_raw_actions(self) -> RawPlayerActions:
        return self._raw_actions
