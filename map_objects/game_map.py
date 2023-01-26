import string

from .tile import Tile
from .rectangle import Rect
from random import randint, choice
from entity import Entity
import tcod as libtcod
from components.fighter import Fighter
from components.ai import BasicMonster
from render_functions import RenderOrder


class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def make_map(self, room_min_size, room_max_size, map_width, map_height, max_rooms, player, entities, max_monster_per_room):
        rooms = []
        num_rooms = 0
        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room, entities, max_monster_per_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room, entities, max_monster_per_room):
        for x in range(room.x1+1, room.x2):
            for y in range(room.y1+1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        self.place_entities(room, entities, max_monster_per_room)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def place_entities(self, room, entities, max_monster_per_room):
        num_of_monsters = randint(0, max_monster_per_room)
        for i in range(num_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    ai_component = BasicMonster()
                    fighter_component = Fighter(10, 0, 2)
                    monster = Entity(x, y, "o", libtcod.darker_red,
                                     "Orc "+choice(string.ascii_uppercase)+choice(string.ascii_lowercase), blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    ai_component = BasicMonster()
                    fighter_component = Fighter(16, 1, 4)
                    monster = Entity(x, y, "T", libtcod.darker_green,
                                     "Troll "+choice(string.ascii_uppercase)+choice(string.ascii_lowercase)+choice(string.ascii_lowercase),
                                     blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                entities.append(monster)
