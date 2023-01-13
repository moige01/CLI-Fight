import unittest

from cli_figth.lib.parser.serious_narrator import SeriousNarrator
from cli_figth.lib.player import Player, Combo, CombosList, PlayerAction, ActionType


class TestSeriousNarrator(unittest.TestCase):
    def setUp(self) -> None:
        combo_player_one = CombosList()
        combo_player_one.append(Combo(movement='SD', attack='P', energy=3, name='Hadouken'))
        combo_player_one.append(Combo(movement='ASD', attack='K', energy=2, name='Kickoun'))

        combo_player_two = CombosList()
        combo_player_two.append(Combo(movement='WSA', attack='P', energy=2, name='Upper punch'))
        combo_player_two.append(Combo(movement='DAD', attack='K', energy=4, name='Quick Kick'))

        self.player_one = Player(energy=6, name='Player One', combos_list=combo_player_one)
        self.player_two = Player(energy=6, name='Player Two', combos_list=combo_player_two)

        self.narrator = SeriousNarrator()

        super().setUp()

    def test_narrator_movement_speach(self):
        action = PlayerAction(player=self.player_one, moves='ASD', attack='', hit=False, type=ActionType.MOVEMENT, combo=None)

        result = self.narrator.handle_player_action(self.player_one, self.player_two, action)

        self.assertEqual(result, 'Player One realiza un movimiento hacia adelante')

    def test_narrator_combo_hit(self):
        action = PlayerAction(player=self.player_one, moves='ASD', attack='K', hit=True, type=ActionType.COMBO, combo=Combo(movement='ASD', attack='K', energy=2, name='Kickoun'))

        result = self.narrator.handle_player_action(self.player_one, self.player_two, action)

        self.assertEqual(result, '¡Player One conecta un poderoso Kickoun y le resta 2 de energia a Player Two!')

    def test_narrator_normal_hit(self):
        action = PlayerAction(player=self.player_one, moves='SSA', attack='P', hit=True, type=ActionType.NORMAL_HIT, combo=Combo(movement='SSA', attack='P', energy=1, name='Puño'))

        result = self.narrator.handle_player_action(self.player_one, self.player_two, action)

        self.assertEqual(result, 'Player One conecta un golpe a Player Two y le resta 1 de energia')

    def test_end_match(self):
        result = self.narrator.handle_end_match(self.player_two)

        self.assertEqual(result, '¡Y el ganador es: Player Two!')
