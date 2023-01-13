import unittest

from cli_figth.lib.parser.serious_actions_handler import SeriousActionsHandler
from cli_figth.lib.player import Player, Combo, CombosList, PlayerAction, ActionType


class TestActionsHandler(unittest.TestCase):
    def setUp(self) -> None:
        combo_player_one = CombosList()
        combo_player_one.append(Combo(movement='SD', attack='P', energy=3, name='Hadouken'))
        combo_player_one.append(Combo(movement='ASD', attack='K', energy=2, name='Kickoun'))

        combo_player_two = CombosList()
        combo_player_two.append(Combo(movement='WSA', attack='P', energy=2, name='Upper punch'))
        combo_player_two.append(Combo(movement='DAD', attack='K', energy=4, name='Quick Kick'))

        self.player_one = Player(energy=6, name='Player One', combos_list=combo_player_one)
        self.player_two = Player(energy=6, name='Player Two', combos_list=combo_player_two)

        self.actions_handler = SeriousActionsHandler()

        super().setUp()

    def test_end_match(self):
        with self.assertRaises(SystemExit) as tested_exception:
            self.actions_handler.handle_end_match(self.player_one)

        self.assertEqual(tested_exception.exception.code, 0)

    def test_player_combo_hit(self):
        action = PlayerAction(player=self.player_one, moves='ASD', attack='K', hit=True, type=ActionType.COMBO, combo=Combo(movement='ASD', attack='K', energy=2, name='Kickoun'))

        self.actions_handler.handle_player_action(self.player_one, self.player_two, action)

        self.assertEqual(self.player_two.energy, 4)

    def test_player_normal_hit(self):
        action = PlayerAction(player=self.player_one, moves='WS', attack='P', hit=True, type=ActionType.NORMAL_HIT, combo=Combo(movement='WS', attack='P', energy=1, name='Golpe'))

        self.actions_handler.handle_player_action(self.player_one, self.player_two, action)

        self.assertEqual(self.player_two.energy, 5)
