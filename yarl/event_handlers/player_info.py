from tcod.console import Console

from .ask_user import AskUserEventHandler


class PlayerInfoEventHandler(AskUserEventHandler):
    title = "Player information"

    def on_render(self, console: Console) -> None:
        super().on_render(console)

        player = self.engine.player

        x = 40 if player.x <= 30 else 0
        y = 0

        width = len(self.title) + 4

        console.draw_frame(
            x=x,
            y=y,
            width=width,
            height=4,
            title=self.title,
            clear=True,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
        )

        console.print(x=x + 1, y=y + 1, string=f"Attack: {player.fighter.base_power}")
        console.print(
            x=x + 1, y=y + 2, string=f"Defense: {player.fighter.base_defense}"
        )
