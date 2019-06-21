import tcod as libtcod
import tcod.event as event

from entity import Entity
from input_handlers import handle_keys
from render_functions import clear_all, render_all

def main():
    screen_width = 80
    screen_height = 50

    player = Entity(int(screen_width/2), int(screen_height/2), '@', libtcod.white)
    entities = [player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    root_console = libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False, renderer=libtcod.RENDERER_OPENGL2, vsync=True)
    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
        events = event.get()

        render_all(con, entities, screen_width, screen_height)
        libtcod.console_flush()

        clear_all(con, entities)

        for ev in events:
            if ev.type == 'QUIT':
                raise SystemExit()
            elif ev.type == 'KEYDOWN':
                action = handle_keys(ev)

                move = action.get('move')
                fullscreen = action.get('fullscreen')
                exit = action.get('exit')

                if move:
                    dx, dy = move
                    player.move(dx, dy)

                if exit:
                    raise SystemExit()

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
