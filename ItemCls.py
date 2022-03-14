import pygame
from random import randint


class Item:

    def __init__(self):
        self.item_image = "Images/various/gas.png"
        self.get_item_sound = pygame.mixer.Sound("Sounds/get_item_sound.wav")
        self.x_left_border = 550
        self.x_right_border = 935
        self.y_top_border = 100
        self.y_down_border = 700
        self.speed = 5
        self.x_pos = randint(self.x_left_border, self.x_right_border)
        self.y_pos = -100
        self.image = pygame.image.load(self.item_image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.shape = pygame.Rect(self.get_pos()[0], self.get_pos()[1], self.width, self.height)

    def get_pos(self):
        return [self.x_pos, self.y_pos]

    def show(self, window):
        self.y_pos += self.speed - 2
        self.shape = pygame.Rect(self.get_pos()[0], self.get_pos()[1], self.width, self.height)
        window.blit(self.image, (self.x_pos, self.y_pos))

    def play_music(self, loop=0):
        self.get_item_sound.play(loops=loop)


class Fuel(Item):

    def __init__(self):
        super().__init__()
        self.item_image = "Images/various/gas.png"
        self.fuel = randint(50, 80)
        self.image = pygame.image.load(self.item_image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def interact(self, player):
        if self.shape.colliderect(player.shape):
            self.play_music(loop=0)
            player.increase_fuel(self.fuel)
            return True


class Life(Item):

    def __init__(self):
        super().__init__()
        self.item_image = "Images/various/heart.png"
        self.life = 1
        self.image = pygame.image.load(self.item_image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def interact(self, player):
        if self.shape.colliderect(player.shape):
            self.play_music(loop=0)
            player.increase_lifes(self.life)
            return True
