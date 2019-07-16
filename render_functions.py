import tcod as libtcod

def render_all(src_con, dst_con,entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = fov_map.fov[y, x]
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        src_con.tiles['bg'][x, y, :3] = colors.get('light_wall')
                        src_con.tiles['ch'][x, y] = ord('#')
                    else:
                        src_con.tiles['bg'][x, y, :3] = colors.get('light_ground')
                        src_con.tiles['ch'][x, y] = ord(' ')

                    src_con.tiles['fg'][x, y, :3] = libtcod.white
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        src_con.tiles['bg'][x, y, :3] = colors.get('dark_wall')
                        src_con.tiles['ch'][x, y] = ord('#')
                    else:
                        src_con.tiles['bg'][x, y, :3] = colors.get('dark_ground')
                        src_con.tiles['ch'][x, y] = ord(' ')
                    src_con.tiles['fg'][x, y, :3] = libtcod.gray

    for entity in entities:
        draw_entity(src_con, entity, fov_map)

    src_con.blit(dst_con)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if fov_map.fov[entity.y, entity.x]:
        con.tiles['fg'][entity.x, entity.y, :3] = entity.color
        # Index this array with console.ch[i, j]  # order='C' or console.ch[x, y]  # order='F'.
        con.tiles['ch'][entity.x, entity.y] = ord(entity.char)

def clear_entity(con, entity):
    con.tiles['ch'][entity.x, entity.y] = ord(' ')
