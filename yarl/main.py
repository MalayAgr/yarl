import tcod
from yarl.engine import Engine
from yarl.entity import ActiveEntity
from yarl.mapgen import MapGenerator
from yarl.utils.ai import AttackingAI


def main() -> None:
    screen_width = 100
    screen_height = 50

    map_width = 100
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(
        "./assets/tileset.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = ActiveEntity(
        char="@",
        color=(255, 255, 255),
        name="Player",
        ai_cls=AttackingAI,
        max_hp=30,
        defense=2,
        power=5,
        speed=2,
    )

    map_generator = MapGenerator(
        map_width=map_width,
        map_height=map_height,
        room_min_size=5,
        depth=10,
        max_enemies_per_room=2,
        full_rooms=False,
    )

    game_map = map_generator.generate_map(player=player)

    engine = Engine(game_map=game_map, player=player)

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

            engine.event_handler.handle_events(events)


if __name__ == "__main__":
    main()
