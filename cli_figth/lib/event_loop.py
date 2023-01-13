from collections import deque
from typing import Callable, Deque


class EventHandler:
    callbacks: dict[str, Deque[Callable]] = {}

    def on(self, event_name: str, callback: Callable) -> None:
        if event_name not in self.callbacks:
            self.callbacks[event_name] = deque([callback])
        else:
            self.callbacks[event_name].appendleft(callback)

    def trigger(self, event_name, **args):
        if not self.callbacks or event_name not in self.callbacks:
            return

        callbacks = self.callbacks[event_name]

        for callback in callbacks:
            callback(**args)
