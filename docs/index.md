# Welcome to YARL - Yet Another RogueLike

Get ready to dive into the dark dungeons :door: and fight terrifying monsters :japanese_goblin: :japanese_ogre: ?

## Project Layout

```
.
└── yarl
    ├── actions.py
    ├── assets
    │   └── tileset.png
    ├── components
    │   ├── ai.py
    │   ├── consumable.py
    │   ├── fighter.py
    │   ├── __init__.py
    │   ├── inventory.py
    │   └── render_order.py
    ├── engine.py
    ├── entity.py
    ├── event_handlers
    │   ├── ask_user.py
    │   ├── consume_single_item.py
    │   ├── controls.py
    │   ├── event_handler.py
    │   ├── game_over.py
    │   ├── history.py
    │   ├── __init__.py
    │   ├── inventory_drop.py
    │   ├── inventory.py
    │   ├── look.py
    │   ├── main_game.py
    │   ├── select_index.py
    │   ├── select_item.py
    │   ├── select_item_to_consume.py
    │   ├── select_item_to_pick_up.py
    │   ├── select_target_area.py
    │   ├── select_target_index.py
    │   └── switachable.py
    ├── exceptions.py
    ├── gamemap.py
    ├── __init__.py
    ├── interface
    │   ├── color.py
    │   ├── __init__.py
    │   ├── message_log.py
    │   └── renderer.py
    ├── logger.py
    ├── main.py
    ├── mapgen.py
    └── tile_types.py
```
