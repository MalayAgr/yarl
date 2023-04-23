from __future__ import annotations

import textwrap
from typing import Reversible

import tcod
from yarl.interface import color


class Message:
    def __init__(self, text: str, fg: tuple[int, int, int]) -> None:
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        return (
            f"{self.plain_text} (x{self.count})" if self.count > 1 else self.plain_text
        )


class MessageLog:
    def __init__(self) -> None:
        self.messages: list[Message] = []

    def add_message(
        self, text: str, fg: tuple[int, int, int] = color.WHITE, *, stack: bool = True
    ) -> None:
        if stack and self.messages and self.messages[-1].plain_text == text:
            self.messages[-1].count += 1
            return None

        self.messages.append(Message(text=text, fg=fg))

    def render(self, console: tcod.Console, x: int, y: int, width: int, height: int):
        self.render_messages(
            console=console,
            x=x,
            y=y,
            width=width,
            height=height,
            messages=self.messages,
        )

    @staticmethod
    def render_messages(
        console: tcod.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        for message in reversed(messages):
            lines = reversed(textwrap.wrap(text=message.full_text, width=width))

            for line in lines:
                console.print(x=x, y=y + height - 1, string=line, fg=message.fg)
                height -= 1

                if height <= 0:
                    return
