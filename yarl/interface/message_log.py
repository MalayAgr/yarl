from __future__ import annotations

import textwrap
from typing import Reversible

import tcod
from yarl.interface import color


class Message:
    """Class to represent a colored text message.

    Attributes:
        plain_text (str): Text of the message.

        fg (tuple[int, int, int]): Color for the message.

        count (int): Multiplier to show beside the message.
    """

    def __init__(self, text: str, fg: tuple[int, int, int]) -> None:
        """Create a message.

        Args:
            text: Text of the message.
            fg: Color for the message.
        """
        self.plain_text = text
        self.fg = fg
        self.count = 1

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(plain_text={self.plain_text}, count={self.count})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def full_text(self) -> str:
        """The full text of the message with the count.

        Examples:
            >>> msg = Message(text="Hello", fg=(255, 255, 255))
            >>> msg.full_text
            'Hello'
            >>> msg.count = 3
            >>> msg.full_text
            'Hello (x3)'
        """
        return (
            f"{self.plain_text} (x{self.count})" if self.count > 1 else self.plain_text
        )


class MessageLog:
    """Class to represent a list of `Message` instances with rendering capabilities.

    Attributes:
        messages (list[Message]): Current messages in the log.
    """

    def __init__(self) -> None:
        """Create an empty message log."""
        self.messages: list[Message] = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.__repr__()

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
