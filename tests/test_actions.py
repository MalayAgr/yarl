from typing import Callable

import tcod.event
from tcod.event import KeyDown
from yarl.actions import Action, EscapeAction, MovementAction
from yarl.input_handlers import EventHandler

MakeKeyDownEventType = Callable[[int, int, int], KeyDown]


def test_escape_action(
    event_handler: EventHandler, make_keydown_event: MakeKeyDownEventType
):
    event = make_keydown_event(
        scancode=tcod.event.Scancode.ESCAPE,
        sym=tcod.event.K_ESCAPE,
        mod=tcod.event.Modifier.NONE,
    )

    action = event_handler.dispatch(event)

    assert isinstance(action, EscapeAction)


def test_movement_action_up(
    event_handler: EventHandler, make_keydown_event: MakeKeyDownEventType
):
    event = make_keydown_event(
        scancode=tcod.event.Scancode.UP,
        sym=tcod.event.K_UP,
        mod=tcod.event.Modifier.NONE,
    )

    action = event_handler.dispatch(event)

    assert isinstance(action, MovementAction)
    assert action.dx == 0
    assert action.dy == -1


def test_movement_action_down(
    event_handler: EventHandler, make_keydown_event: MakeKeyDownEventType
):
    event = make_keydown_event(
        scancode=tcod.event.Scancode.DOWN,
        sym=tcod.event.K_DOWN,
        mod=tcod.event.Modifier.NONE,
    )

    action = event_handler.dispatch(event)

    assert isinstance(action, MovementAction)
    assert action.dx == 0
    assert action.dy == 1


def test_movement_action_left(
    event_handler: EventHandler, make_keydown_event: MakeKeyDownEventType
):
    event = make_keydown_event(
        scancode=tcod.event.Scancode.LEFT,
        sym=tcod.event.K_LEFT,
        mod=tcod.event.Modifier.NONE,
    )

    action = event_handler.dispatch(event)

    assert isinstance(action, MovementAction)
    assert action.dx == -1
    assert action.dy == 0


def test_movement_action_right(
    event_handler: EventHandler, make_keydown_event: MakeKeyDownEventType
):
    event = make_keydown_event(
        scancode=tcod.event.Scancode.RIGHT,
        sym=tcod.event.K_RIGHT,
        mod=tcod.event.Modifier.NONE,
    )

    action = event_handler.dispatch(event)

    assert isinstance(action, MovementAction)
    assert action.dx == 1
    assert action.dy == 0


def test_invalid_key(
    event_handler: EventHandler, make_keydown_event: MakeKeyDownEventType
):
    event = make_keydown_event(
        scancode=tcod.event.Scancode.KP_PLUS,
        sym=tcod.event.K_KP_PLUS,
        mod=tcod.event.Modifier.NONE,
    )

    action = event_handler.dispatch(event)

    assert action is None
