import tcod
from yarl.engine import Engine
from yarl.entity import Entity
from yarl.input_handlers import EventHandler


def main() -> None:
    screen_width = 100
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "./assets/tileset.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = Entity(x=player_x, y=player_y, char="@", color=(255, 255, 255))
    npc = Entity(x=player_x - 5, y=player_y - 5, char="@", color=(255, 255, 0))

    entities = {player, npc}

    event_handler = EventHandler()

    engine = Engine(entities=entities, event_handler=event_handler, player=player)

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=tileset,
        title="Yet Another RogueLike",
        vsync=True,
    ) as context:
        root_console = tcod.Console(width=screen_width, height=screen_height, order="F")

        while True:
            engine.render(console=root_console, context=context)

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()
