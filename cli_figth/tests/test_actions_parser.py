import unittest

from cli_figth.lib.parser import SeriousActionsParser
from cli_figth.lib.player import RawPlayer, CombosList, Combo, Player, PlayerAction, ActionType

class TestActionsParser(unittest.TestCase):
    def setUp(self) -> None:
        self.actions_parser = SeriousActionsParser()
        combo_list = CombosList()

        combo_list.append(Combo(movement='WS', attack='P', energy=3, name='Ultra Punch'))
        combo_list.append(Combo(movement='ADS', attack='K', energy=5, name='Ultra Kick'))

        player: RawPlayer = {
            'name': 'Tomy',
            'energy': 6,
            'movements': ['WS', 'SS', 'SDA', 'ADS'],
            'attacks': ['P', 'K', '', 'K'],
            'combos_list': combo_list,
        }

        self.raw_player = player

        super().setUp()

    def test_load_raw_players_actions(self):
        self.actions_parser.load_raw_player_actions(player=self.raw_player)

        hipotetic_player = Player(name='Tomy', energy=6, combos_list=self.raw_player['combos_list'])
        raw_actions = self.actions_parser.get_raw_actions()

        self.assertIn(hipotetic_player, raw_actions)

        raw_player_actions = raw_actions[hipotetic_player]

        self.assertEqual(raw_player_actions['movements'], ['WS', 'SS', 'SDA', 'ADS'])
        self.assertEqual(raw_player_actions['attacks'], ['P', 'K', '', 'K'])

    def test_parse_actions(self):
        self.actions_parser.load_raw_player_actions(player=self.raw_player)
        self.actions_parser.parse_actions()

        hipotetic_player = Player(name='Tomy', energy=6, combos_list=self.raw_player['combos_list'])

        action_1 = PlayerAction(
            player=hipotetic_player,
            moves='WS',
            attack='P',
            type=ActionType.COMBO,
            hit=True,
            combo=Combo(movement='WS', attack='P', energy=3, name='Ultra Punch'),
        )

        action_2 = PlayerAction(
            player=hipotetic_player,
            moves='SS',
            attack='K',
            type=ActionType.NORMAL_HIT,
            hit=True,
            combo=Combo(movement='SS', attack='K', energy=1, name='Patada'),
        )

        action_3 = PlayerAction(
            player=hipotetic_player,
            moves='SDA',
            attack='',
            type=ActionType.MOVEMENT,
            hit=False,
            combo=None,
        )

        action_4 = PlayerAction(
            player=hipotetic_player,
            moves='ADS',
            attack='K',
            type=ActionType.COMBO,
            hit=True,
            combo=Combo(movement='ADS', attack='K', energy=5, name='Ultra Kick'),
        )

        hipotetic_actions_list = [action_1, action_2, action_3, action_4]

        parsed_actions = self.actions_parser.get_parsed_actions()

        self.assertIn(hipotetic_player, parsed_actions)

        actions_list = parsed_actions[hipotetic_player]

        for hipotetic_action in hipotetic_actions_list:
            self.assertIn(hipotetic_action, actions_list)

        # Ensure order
        self.assertEqual(action_1, actions_list[0])
        self.assertEqual(action_2, actions_list[1])
        self.assertEqual(action_3, actions_list[2])
        self.assertEqual(action_4, actions_list[3])
