
class Character():
    def __init__(self):
        self.health = 100
        self.damage = 1

    def handle_damage(self, damage: int):
        self.health -= damage

    def get_damage(self):
        return self.damage
