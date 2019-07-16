import tcod as libtcod
import tcod.event as event


def handle_keys(ev):
    # Movement keys
    if ev.sym == event.K_UP or ev.sym == event.K_k:
        return {'move': (0, -1)}
    elif ev.sym == event.K_DOWN or ev.sym == event.K_j:
        return {'move': (0, 1)}
    elif ev.sym == event.K_LEFT or ev.sym == event.K_h:
        return {'move': (-1, 0)}
    elif ev.sym == event.K_RIGHT or ev.sym == event.K_l:
        return {'move': (1, 0)}
    elif ev.sym == event.K_y:
        return {'move': (-1, -1)}
    elif ev.sym == event.K_u:
        return {'move': (1, -1)}
    elif ev.sym == event.K_b:
        return {'move': (-1, 1)}
    elif ev.sym == event.K_n:
        return {'move': (1, 1)}

    if ev.sym == event.K_RETURN and ev.mod & event.KMOD_LALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif ev.sym == event.K_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}
