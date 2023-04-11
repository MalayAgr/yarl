from __future__ import annotations


class Entity:
    def __init__(self, x: int, y: int, char: str, color: tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

    def spawn(self, x, y) -> None:
        self.x, self.y = x, y
