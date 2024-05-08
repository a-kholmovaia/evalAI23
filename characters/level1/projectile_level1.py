from characters.enemy import Enemy
from characters.attack_info import AttackInfo
from scenes.scene_state import SceneState
from masters.sprite_master import SpriteMaster
import pygame
import random
class Projectile(Enemy):
    def __init__(self, game_screen, start_position):
        super().__init__(game_screen, start_position, SpriteMaster("levels/level1/projectile", 
                              idle=0, walk=0, attack=4, 
                              hurt=0, death=3, block=0, start_action="hit"))
        self.current_action = "hit"
        self.attack_info = AttackInfo(10, False)
        self.speed = 3
        self.collision_distance = 50
        self.current_position[1] += 20
        self.text = self.get_text_projectile()

    def policy(self, scene_state: SceneState) -> str:
        """
        Moves left and attacks constantly
        """

        if self.cal_distance2player(scene_state.get_player_pos()) < self.collision_distance:
            self.health = 0

        if self.health<=0 and self.death_counter>0:
            self.death_counter -= self.speed
            return "death"   
        
        if self.health <= 0 and self.death_counter <= 0:
            self.current_position = (-100, -100)
            return "death"
        
        self.current_position[0] -= self.speed 
        return "hit"

    def copy(self):
        """
        Copy constructor
        """
        return Projectile(self.game_screen, self.current_position.copy())
    
    def draw_current_action(self):
        text = self.text
        rendered_text = self.font.render(text, True, (255,0,0))
        sprite = pygame.transform.scale(self.sprite_master.get_sprite_frame(self.current_action), (self.size, self.size))
        if self.reflect:
            sprite = pygame.transform.flip(sprite, True, False)
        self.game_screen.blit(sprite, self.current_position)
        self.game_screen.blit(rendered_text, (self.current_position[0], self.current_position[1]+30))


    def get_text_projectile(self):
        texts = ['…approaching deadline…',"…I’m on vacation…", 
                 '…last-minute changes…','…lost the source code…', '…zoom meeting at 8 AM…',
                 '…group chat exploded…', '…buggy software…']
        return random.choice(texts)



