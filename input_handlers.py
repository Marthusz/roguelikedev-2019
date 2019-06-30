import tcod as libtcod
import tcod.event as event


def handle_keys(ev):
    # Movement keys
    if ev.sym == event.K_UP:
        return {'move': (0, -1)}
    elif ev.sym == event.K_DOWN:
        return {'move': (0, 1)}
    elif ev.sym == event.K_LEFT:
        return {'move': (-1, 0)}
    elif ev.sym == event.K_RIGHT:
        return {'move': (1, 0)}
    elif ev.sym == event.K_SPACE:
        return {'map': True}

    if ev.sym == event.K_RETURN and ev.mod & event.KMOD_LALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif ev.sym == event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
