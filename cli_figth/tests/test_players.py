import unittest
from unittest.mock import patch, DEFAULT, MagicMock

from cli_figth.lib.player import Player


class TestPlayer(unittest.TestCase):
    def test_i_can_create_my_favorite_player(self):
        player = Player(name='Naruto', energy=3)

        self.assertEqual(player.name, 'Naruto')
        self.assertEqual(player.energy, 3)
        self.assertIsNone(player.combos_list)

    def test_two_players_are_the_same_if_they_have_the_same_name(self):
        player_one = Player(name='Player 1', energy=2)
        player_two = Player(name='Player 1', energy=5)

        self.assertEqual(player_one, player_two)

    def test_i_can_not_modify_my_player_name_and_energy_after_create_it(self):
        player = Player(name='Naruto', energy=3)

        with self.assertRaises(AttributeError):
            player.name = 'Test'
            player.energy = 3

    def test_the_energy_of_my_player_can_not_drop_far_from_zero(self):
        player = Player(name='Naruto', energy=3)

        player.decrease_energy_by(5)

        self.assertAlmostEqual(player.energy, 0)

    def test_my_player_should_dead_if_it_energy_drop_far_from_zero(self):
        player = Player(name='Naruto', energy=3)

        self.assertFalse(player.is_dead())

        player.decrease_energy_by(3)

        self.assertTrue(player.is_dead())
