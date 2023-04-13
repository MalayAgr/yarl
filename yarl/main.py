import tcod
from yarl.engine import Engine
from yarl.entity import Entity
from yarl.gamemap import GameMap
from yarl.input_handlers import EventHandler
from yarl.mapgen import MapGenerator


def main() -> None:
    screen_width = 100
    screen_height = 50

    map_width = 100
    map_height = 45

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "./assets/tileset.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = Entity(x=player_x, y=player_y, char="@", color=(255, 255, 255))
    npc = Entity(x=player_x - 5, y=player_y - 5, char="@", color=(255, 255, 0))

    entities = {player, npc}

    map_generator = MapGenerator(
        map_width=map_width,
        map_height=map_height,
        room_min_size=5,
        depth=10,
        full_rooms=False,
    )

    game_map = map_generator.generate_map(player=player)

    event_handler = EventHandler()

    engine = Engine(
        entities=entities, event_handler=event_handler, game_map=game_map, player=player
    )

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
