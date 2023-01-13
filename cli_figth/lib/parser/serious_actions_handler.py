from cli_figth.lib.parser.actions_handler_base import ActionsHanlderBase
from cli_figth.lib.player import Player, PlayerAction, ActionType

class SeriousActionsHandler(ActionsHanlderBase):
    def handle_end_match(self, winner: Player) -> str:
        exit(0)

    def handle_player_action(self, player_one: Player, player_two: Player, action: PlayerAction) -> str:
        match action.type:
            case ActionType.COMBO | ActionType.NORMAL_HIT:
                hitted = player_two if action.player == player_one else player_one

                return self._handle_player_hit(hitter=action.player, hitted=hitted, hitter_action=action)
            case ActionType.MOVEMENT:
                return self._handle_player_movement(action=action)
            case _:
                raise ValueError('Unrecognized action.')

    def _handle_player_movement(self, action: PlayerAction) -> str:
        pass

    def _handle_player_hit(self, hitter: Player, hitted: Player, hitter_action: PlayerAction) -> str:
        hitted.decrease_energy_by(hitter_action.combo.energy)
