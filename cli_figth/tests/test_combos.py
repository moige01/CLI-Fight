import unittest

from cli_figth.lib.exceptions import RepeatedCombo
from cli_figth.lib.player import Combo, CombosList


class TestCombosList(unittest.TestCase):
    def test_i_can_create_my_combo(self):
        combo = Combo(movement='DDS', attack='P', energy=2, name='Falcon Punch')

        self.assertEqual(combo.attack, 'P')
        self.assertEqual(combo.movement, 'DDS')
        self.assertEqual(combo.energy, 2)
        self.assertEqual(combo.name, 'Falcon Punch')

    def test_i_can_check_combo_equality(self):
        combo1 = Combo(movement='DDS', attack='P', energy=2, name='Falcon Punch')
        combo2 = Combo(movement='DDS', attack='P', energy=1, name='Falcon Punch')
        combo3 = Combo(movement='DS', attack='K', energy=2, name='Falcon Punch')
        combo4 = Combo(movement='DS', attack='K', energy=2, name='Falcon Kick')

        self.assertEqual(combo1, combo2, "Two combos are equal even if the energy differ")
        self.assertEqual(combo1, combo3, "Two combos with same name should be trated as same combo")
        self.assertNotEqual(combo1, combo4, "Two combos are differents if them differ from attacks, moves and name")

        with self.assertRaises(ValueError, msg='A Combo should be compared only with another Combo.'):
            combo1 == 2

    def test_i_can_create_my_combo_list_only_with_my_favorites_combos(self):
        combo1 = Combo(movement='DDS', attack='P', energy=2, name='Falcon Punch')
        combo2 = Combo(movement='ASD', attack='P', energy=3, name='Hadouken')
        combo3 = Combo(movement='WSAS', attack='K', energy=5, name='Final Flash')

        combo_list = CombosList([combo1, combo2, combo3])

        self.assertEqual(len(combo_list), 3)
        self.assertEqual(combo_list[0], combo1)
        self.assertEqual(combo_list[1], combo2)
        self.assertEqual(combo_list[2], combo3)

        with self.assertRaises(ValueError):
            CombosList(1)
            CombosList([True])
            combo_list.append('not a combo')

    def test_i_can_not_add_the_same_combo_twice(self):
        combo1 = Combo(movement='DDS', attack='P', energy=2, name='Falcon Punch')
        combo2 = Combo(movement='DDS', attack='P', energy=2, name='Falcon Punch')

        combo_list = CombosList()

        with self.assertRaises(RepeatedCombo):
            combo_list.append(combo1)
            combo_list.append(combo2)

    def test_i_can_find_a_combo_at_least_having_the_attack_and_the_movements(self):
        full_combo = Combo(movement='DSD', attack='P', energy=5, name='Test Combo')
        search_combo = Combo(movement='DSD', attack='P', energy=0, name='')

        combo_list = CombosList([full_combo])

        with self.assertRaises(ValueError):
            combo_list.get_combo_by_attack_and_movements(2)

        result_combo = combo_list.get_combo_by_attack_and_movements(search_combo)

        self.assertIsNotNone(result_combo)
        self.assertEqual(result_combo.movement, 'DSD')
        self.assertEqual(result_combo.attack, 'P')
        self.assertEqual(result_combo.energy, 5)
        self.assertEqual(result_combo.name, 'Test Combo')
