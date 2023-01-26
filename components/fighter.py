from game_messages import Message
import tcod as libtcod


class Fighter:
    def __init__(self, hp, defence, power):
        self.hp = hp
        self.max_hp = hp
        self.defence = defence
        self.power = power

    def take_damage(self, amount):
        result = []
        self.hp -= amount
        print(self.owner.name + " have " + str(self.hp))

        if self.hp <= 0:
            result.append({"dead": self.owner})
        return result

    def attack(self, target):
        result = []
        damage = self.power - target.fighter.defence
        if damage > 0:
            result.append({
                "message": Message("The {} attack {} and deal {} damage!".format(self.owner.name, target.name, str(damage)), libtcod.white)
            })
            result.extend(target.fighter.take_damage(damage))
        else:
            result.append({
                "message": Message("The {} was attacked by {}, but have a good defence".format(target.name, self.owner.name), libtcod.white)
            })
        return result
