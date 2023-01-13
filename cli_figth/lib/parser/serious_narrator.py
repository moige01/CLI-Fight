from cli_figth.lib.parser.actions_handler_base import ActionsHanlderBase
from cli_figth.lib.player import Player, PlayerAction, ActionType


class SeriousNarrator(ActionsHanlderBase):
    LAST_MOVE_TRASLATOR = {
        'W': 'realiza un alto',
        'D': 'realiza un movimiento hacia adelante',
        'A': 'realiza un movimiento hacia atrás',
        'S': 'se agacha',
        '': 'Se mantiene estático',
    }

    ATTACK_TRASLATOR = {
        'P': 'conecta un golpe',
        'K': 'conecta una patada',
    }

    def handle_player_action(self, player_one: Player, player_two: Player, action: PlayerAction) -> str:
        return self._narrate_player_action(player_one, player_two, action)

    def _narrate_player_action(self, player_one: Player, player_two: Player, action: PlayerAction) -> str:
        match action.type:
            case ActionType.COMBO | ActionType.NORMAL_HIT:
                hitted = player_two if action.player == player_one else player_one

                return self._narrate_player_hit(hitter=action.player, hitted=hitted, hitter_action=action)
            case ActionType.MOVEMENT:
                return self._narrate_player_movement(action=action)
            case _:
                raise ValueError('Unrecognized action.')

    def _narrate_player_hit(self, hitter: Player, hitted: Player, hitter_action: PlayerAction) -> str:
        result = ''

        if hitter_action.type == ActionType.COMBO:
            result = self._narrate_player_combo_hit(hitter=hitter, hitted=hitted, hitter_action=hitter_action)
        elif hitter_action.type == ActionType.NORMAL_HIT:
            result = self._narrate_player_normal_hit(hitter=hitter, hitted=hitted, hitter_action=hitter_action)

        return result

    def _narrate_player_combo_hit(self, hitter: Player, hitted: Player, hitter_action: PlayerAction) -> str:
        combo_name = hitter_action.combo.name
        combo_damage = hitter_action.combo.energy
        hitter_name = hitter.name
        hitted_name = hitted.name

        return f'¡{hitter_name} conecta un poderoso {combo_name} y le resta {combo_damage} de energia a {hitted_name}!'

    def _narrate_player_normal_hit(self, hitter: Player, hitted: Player, hitter_action: PlayerAction) -> str:
        combo_name = self.ATTACK_TRASLATOR[hitter_action.attack]
        combo_damage = hitter_action.combo.energy
        hitter_name = hitter.name
        hitted_name = hitted.name

        return f'{hitter_name} {combo_name} a {hitted_name} y le resta {combo_damage} de energia'

    def handle_end_match(self, winner: Player) -> str:
        return self._narrate_end_match(winner)

    def _narrate_end_match(self, winner: Player) -> str:
        winner_name = winner.name

        return f'¡Y el ganador es: {winner_name}!'

    def _narrate_player_movement(self, action: PlayerAction) -> str:
        movements = action.moves
        player = action.player

        last_move = movements[-1]

        traslated_move = self.LAST_MOVE_TRASLATOR.get(last_move)

        return f'{player.name} {traslated_move}'
