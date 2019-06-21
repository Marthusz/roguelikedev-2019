import tcod as libtcod
import tcod.event as event

from input_handlers import handle_keys

def main():
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    root_console = libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False, renderer=libtcod.RENDERER_OPENGL2, vsync=True)
    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
        events = event.get()
        libtcod.console_put_char(con, player_x, player_y, '@', libtcod.BKGND_NONE)
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()

        libtcod.console_put_char(con, player_x, player_y, ' ', libtcod.BKGND_NONE)

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
                    player_x += dx
                    player_y += dy

                if exit:
                    raise SystemExit()

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
