"""This module provides a message log with rendering capabilities."""


from __future__ import annotations

from tcod.console import Console
from yarl.interface import color
from yarl.interface.renderer import render_messages


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
        """Add a message to the message log with optional stacking.

        It creates a [`Message`][yarl.interface.message_log.Message] instance and adds it to the log.

        Args:
            text: Text of the message.

            fg: Color for the message. Defaults to `color.WHITE`.

            stack: Indicates whether the message should be stacked.
                If `True` and the last message in the log has the same text as `text`,
                the count of the message is incremented. Otherwise, the message is appended
                to the log. Defaults to `True`.
        """
        if stack and self.messages and self.messages[-1].plain_text == text:
            self.messages[-1].count += 1
            return None

        self.messages.append(Message(text=text, fg=fg))

    def render(
        self,
        console: Console,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        limit: int | None = None,
    ):
        """Method to render the message log to the console.

        The messages will be rendered starting at `(x, y)`. A horizontal
        space of `width` and a vertical space of `height` will be used.
        Message lines will be wrapped to fit within `width` and
        each line will take up one unit of `height`. Thus, only
        as many message lines as can be fitted in `height` will be rendered.

        Args:
            console: Console to render the log to.

            x: x-coordinate of the location where rendering should start on the console.

            y: y-coordinate of the location where rendering should start on the console.

            width: Amount of horizontal space to use for rendering.

            height: Amount of vertical space to use for rendering.

            limit: Limits the number of messages rendered to the first `limit` messages.
                When set to `None`, all the messages in the log are rendered.
        """
        messages = self.messages if limit is None else self.messages[:limit]

        render_messages(
            console=console,
            x=x,
            y=y,
            width=width,
            height=height,
            messages=reversed(
                [(message.full_text, message.fg) for message in messages]
            ),
        )
