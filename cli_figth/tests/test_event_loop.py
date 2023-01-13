import unittest
from unittest.mock import Mock

from cli_figth.lib import EventHandler


class TestEventLoop(unittest.TestCase):
    def test_i_can_add_a_callback_to_an_event(self):
        event_loop = EventHandler()
        callback_1 = Mock()

        event_loop.on("test_event", callback_1)
        event_loop.trigger("test_event")

        callback_1.assert_called_once()

    def test_i_can_add_multiples_callbacks_to_a_single_event(self):
        event_loop = EventHandler()

        callback_1 = Mock()
        callback_2 = Mock()
        callback_3 = Mock()

        event_loop.on("test_event", callback_1)
        event_loop.on("test_event", callback_2)
        event_loop.on("test_event", callback_3)
        event_loop.trigger("test_event")

        callback_1.assert_called_once()
        callback_2.assert_called_once()
        callback_3.assert_called_once()

    def test_i_can_send_args_to_the_callbacks(self):
        event_loop = EventHandler()

        callback_1 = Mock()

        event_loop.on("test_event", callback_1)
        event_loop.trigger("test_event", test=1, random_arg='foo')

        callback_1.assert_called_once_with(test=1, random_arg='foo')
