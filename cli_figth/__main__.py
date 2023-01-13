from cli_figth.lib.match import Match
from cli_figth.lib.parser import (
    SeriousActionsHandler,
    SeriousActionsParser,
    SeriousNarrator
)
from cli_figth.lib.event_loop import EventHandler
from cli_figth.lib.player import Combo, CombosList, RawPlayer


def main():
    match = Match()

    match.action_parser = SeriousActionsParser()
    match.actions_hanlder = SeriousActionsHandler()
    match.narrator = SeriousNarrator()
    match.event_loop = EventHandler()

    combo_list_player_one = CombosList()

    combo_list_player_one.append(Combo(movement='DSD', attack='P', energy=3, name='Taladoken'))
    combo_list_player_one.append(Combo(movement='SD', attack='K', energy=2, name='Remuyuken'))

    combo_list_player_two = CombosList()

    combo_list_player_two.append(Combo(movement='ASA', attack='P', energy=2, name='Taladoken'))
    combo_list_player_two.append(Combo(movement='SA', attack='K', energy=3, name='Remuyuken'))

    player_one: RawPlayer = {
        'name': 'Tonyn Stallone',
        'energy': 6,
        'movements': ['D', 'DSD', 'S', 'DSD', 'SD'],
        'attacks': ['K', 'P', '', 'K', 'P'],
        'combos_list': combo_list_player_one,
    }

    player_two: RawPlayer = {
        'name': 'Arnaldor Shuatseneguer',
        'energy': 6,
        'movements': ['SA', 'SA', 'SA', 'ASA', 'SA'],
        'attacks': ['K', '', 'K', 'P', 'P'],
        'combos_list': combo_list_player_two,
    }

    match.load_raw_player(player_one)
    match.load_raw_player(player_two)

    match.start_match()


if __name__ == '__main__':
    main()
