import tcod as libtcod


def render_all(con, game_map, fov_map, fov_recompute, entities, screen_width, screen_height, colors):
    if fov_recompute:
        for x in range(game_map.width):
            for y in range(game_map.height):
                visible = fov_map.fov[y][x]
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors["light_wall"], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors["light_ground"], libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors["dark_wall"], libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors["dark_ground"], libtcod.BKGND_SET)

    for entity in entities:
        if fov_map.fov[entity.y][entity.x]:
            draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.symbol, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)
