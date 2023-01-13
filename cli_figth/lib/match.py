from cli_figth.lib.event_loop import EventHandler
from cli_figth.lib.parser import ActionsParserBase, ActionsHanlderBase
from cli_figth.lib.player import PlayerActions, RawPlayer, PlayerAction, Player


class Match:
    def __init__(self) -> None:
        self._event_loop: EventHandler = None
        self._raw_players: list[RawPlayer] = []
        self._action_parser: ActionsParserBase = None
        self._narrator: ActionsHanlderBase = None
        self._actions_hanlder: ActionsHanlderBase = None
        self._parsed_players_actions: PlayerActions = None

    def _set_action_handler(self, actions_handler: ActionsHanlderBase) -> None:
        self._actions_hanlder = actions_handler

    actions_hanlder = property(fset=_set_action_handler)

    def _set_narrator(self, narrator: ActionsHanlderBase) -> None:
        self._narrator = narrator

    narrator = property(fset=_set_narrator)

    def _set_event_loop(self, event_handler: EventHandler) -> None:
        self._event_loop = event_handler

    event_loop = property(fset=_set_event_loop)

    def load_raw_player(self, raw_players: RawPlayer) -> None:
        self._raw_players.append(raw_players)

    def _set_action_parser(self, parser: ActionsParserBase) -> None:
        self._action_parser = parser

    action_parser = property(fset=_set_action_parser)

    def _check_if_action_parser_is_loaded(self) -> None:
        if self._action_parser is None:
            raise ValueError('An ActionParser must be loaded.')

    def _check_if_narrator_is_loaded(self) -> None:
        if self._narrator is None:
            raise ValueError('This game needs a narrator!')

    def _check_if_action_handler_is_loaded(self) -> None:
        if self._actions_hanlder is None:
            raise ValueError('An AnctionsHandler must be loaded.')

    def _check_if_the_event_loop_is_loaded(self) -> None:
        if self._event_loop is None:
            raise ValueError('EventLoop must be loaded.')

    def _check_dependencies_integrity(self) -> None:
        self._check_if_action_handler_is_loaded()
        self._check_if_action_parser_is_loaded
        self._check_if_narrator_is_loaded()
        self._check_if_the_event_loop_is_loaded()

    def _load_players_to_action_parser(self) -> None:
        self._check_if_action_parser_is_loaded()

        for raw_player in self._raw_players:
            self._action_parser.load_raw_player_actions(raw_player)

    def _parse_players_actions(self) -> None:
        self._check_if_action_parser_is_loaded()

        self._action_parser.parse_actions()

        self._parsed_players_actions = self._action_parser.get_parsed_actions()

    def _check_players_integrity(self) -> None:
        if self._parsed_players_actions is None:
            raise ValueError('There is no players ready yet!')

        if len(self._parsed_players_actions) != 2:
            raise ValueError('Only 2 players allowed. No more. No less.')

    def _handle_action(self, player_one: Player, player_two: Player, action: PlayerAction):
        self._event_loop.trigger("player_action", player_one=player_one, player_two=player_two, action=action)

    def _show_narrator_action_speach(self, player_one: Player, player_two: Player, action: PlayerAction):
        text = self._narrator.handle_player_action(player_one=player_one, player_two=player_two, action=action)

        print(text)

    def _show_narrator_end_speach(self, winner: Player):
        text = self._narrator.handle_end_match(winner=winner)

        print(text)

    def _verify_is_some_one_dead(self, player_one: Player, player_two: Player):
        if (player_one.is_dead() or player_two.is_dead()):
            self._event_loop.trigger("end_match", winner=player_one if player_two.is_dead() else player_two)

    def start_match(self) -> None:
        self._load_players_to_action_parser()
        self._parse_players_actions()
        self._check_dependencies_integrity()
        self._check_players_integrity()

        players = list(self._parsed_players_actions.keys())
        actions = list(self._parsed_players_actions.values())

        player_one = players[0]
        player_two = players[1]
        player_one_actions = actions[0]
        player_two_actions = actions[1]

        self._event_loop.on("player_action", self._actions_hanlder.handle_player_action)
        self._event_loop.on("player_action", self._show_narrator_action_speach)

        self._event_loop.on("end_match", self._actions_hanlder.handle_end_match)
        self._event_loop.on("end_match", self._show_narrator_end_speach)

        for (player_one_action, player_two_action) in zip(player_one_actions, player_two_actions):
            # Turn N
            self._handle_action(player_one=player_one, player_two=player_two, action=player_one_action)

            self._verify_is_some_one_dead(player_one=player_one, player_two=player_two)

            # Turn N+1
            self._handle_action(player_one=player_one, player_two=player_two, action=player_two_action)

            self._verify_is_some_one_dead(player_one=player_one, player_two=player_two)
