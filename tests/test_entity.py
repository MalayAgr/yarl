from yarl.entity import Entity


def test_initialization():
    x, y, char, color = 1, 5, "@", (255, 255, 255)

    entity = Entity(x=x, y=y, char=char, color=color)

    assert entity.x == x
    assert entity.y == y
    assert entity.char == char
    assert entity.color == color


def test_move():
    x, y, char, color = 1, 5, "@", (255, 255, 255)

    entity = Entity(x=x, y=y, char=char, color=color)

    dx, dy = 1, 2

    entity.move(dx=dx, dy=dy)

    assert entity.x == x + dx
    assert entity.y == y + dy
