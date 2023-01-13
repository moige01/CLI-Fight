import unittest

from cli_figth.lib.match import Match
from cli_figth.lib.parser import (
    SeriousActionsHandler,
    SeriousActionsParser,
    SeriousNarrator
)
from cli_figth.lib.event_loop import EventHandler
from cli_figth.lib.player import Player, Combo, CombosList, RawPlayer


class TestIntegration(unittest.TestCase):
    def test_the_game_should_be_go_ok(self):
        match = Match()

        match.action_parser = SeriousActionsParser()
        match.actions_hanlder = SeriousActionsHandler()
        match.narrator = SeriousNarrator()
        match.event_loop = EventHandler()

        combo_list_player_one = CombosList()

        combo_list_player_one.append(Combo(movement='WS', attack='P', energy=3, name='Ultra Punch'))
        combo_list_player_one.append(Combo(movement='ADS', attack='K', energy=5, name='Ultra Kick'))

        combo_list_player_two = CombosList()

        combo_list_player_two.append(Combo(movement='SSD', attack='P', energy=2, name='Soft Punch'))
        combo_list_player_two.append(Combo(movement='WWS', attack='K', energy=3, name='Foo Kick'))

        player_one: RawPlayer = {
            'name': 'Tomy',
            'energy': 6,
            'movements': ['WS', 'SS', 'SDA', 'ADS', 'S'],
            'attacks': ['P', 'K', '', 'K', ''],
            'combos_list': combo_list_player_one,
        }

        player_two: RawPlayer = {
            'name': 'Timoti',
            'energy': 6,
            'movements': ['WS', 'SS', 'SSD', 'ADS', 'WWS'],
            'attacks': ['P', '', 'P', '', 'K'],
            'combos_list': combo_list_player_two,
        }

        match.load_raw_player(player_one)
        match.load_raw_player(player_two)

        with self.assertRaises(SystemExit) as raised_exception:
            match.start_match()

        self.assertEqual(raised_exception.exception.code, 0)
