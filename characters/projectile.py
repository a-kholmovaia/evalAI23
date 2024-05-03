from enemy import Enemy

class Projectile(Enemy):
    def __init__(self, game_screen, start_position, sprite_master):
        super.__init__(game_screen, start_position, sprite_master)

