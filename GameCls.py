import pygame
import sys

from AutoCls import PlayerCar, Cars
from ItemCls import Life, Fuel
from random import choice


class Window:

    def __init__(self):
        self.width = 1124
        self.high = 858
        self.window = pygame.display.set_mode((self.width, self.high))
        self.blinking_value = 40
        pygame.mixer.init()
        pygame.init()
        pygame.font.init()

        self.main_music = pygame.mixer.Sound("Sounds/main_music.mp3")
        self.pause_background_music = self.main_music
        self.start_background_music = pygame.mixer.Sound("Sounds/start_music.wav")
        self.end_background_music = pygame.mixer.Sound("Sounds/end_music.mp3")
        self.crash_sound = pygame.mixer.Sound("Sounds/crash_sound.wav")
        self.get_item_sound = pygame.mixer.Sound("Sounds/get_item_sound.wav")
        self.counting_sound = pygame.mixer.Sound("Sounds/counting_sound.wav")

        self.main_music.set_volume(0.3)
        self.start_background_music.set_volume(0.3)
        self.end_background_music.set_volume(0.3)

        self.player = PlayerCar()


    @staticmethod
    def event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def show_backgroud(self):
        self.window.fill((54, 168, 50))


class Game(Window):

    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.backgroung_img = pygame.image.load("Images/backgrounds/backgroung.png")
        self.x_point = self.width - self.backgroung_img.get_width()
        self.y_point = 0
        self.speed_of_scrolling = 0
        self.fps_count = 0
        self.fps_count_cars = 0
        self.fps_count_item = 0
        self.fps_count_fuel = 0
        self.oponents = []
        self.items = []

        self.font = pygame.font.Font('Fonts/RetroGaming.ttf', 30)
        self.font2 = pygame.font.Font('Fonts/VIDEOPHREAK.ttf', 48)
        self.font3 = pygame.font.Font('Fonts/VIDEOPHREAK.ttf', 70)
        self.font4 = pygame.font.Font('Fonts/RetroGaming.ttf', 24)


    def counting_fx(self, loop):
        self.counting_sound.play(loops=loop)

    def play_music(self):
        self.main_music.play()

    def stop_music(self):
        self.main_music.stop()

    def backgroung_draw(self):

        self.window.fill((54, 168, 50))
        y_point2 = self.y_point - self.backgroung_img.get_height()
        self.window.blit(self.backgroung_img, (self.x_point, self.y_point))
        self.window.blit(self.backgroung_img, (self.x_point, y_point2))
        if y_point2 > 0:
            self.y_point = 0
        self.y_point += self.speed_of_scrolling

        # Game scrolling at start
        if self.fps_count > 20:
            if self.speed_of_scrolling < 10:
                self.speed_of_scrolling += 1
                self.fps_count = 0

        self.fps_count += 1
        self.fps_count_item += 1
        self.fps_count_cars += 1
        self.fps_count_fuel += 1

    def text_draw(self):

        title = self.font2.render("THE SPEEDEST", False, (0, 0, 0))
        self.window.blit(title, (10, 100))

        title2 = self.font3.render("CAR", False, (0, 0, 0))
        self.window.blit(title2, (110, 150))

        points = self.font.render(f"Points: {self.player.have_point}", False, (0, 0, 0))
        self.window.blit(points, (90, 400))

        fuel = self.font.render(f"Fuel: {self.player.get_fuel()}", False, (0, 0, 0))
        self.window.blit(fuel, (90, 500))

        life = self.font.render(f"Life: {self.player.get_lifes()}", False, (0, 0, 0))
        self.window.blit(life, (90, 600))

        pause = self.font4.render("Press (P) to pause game", False, (0, 0, 0))
        self.window.blit(pause, (15, 750))

    def player_draw(self):
        self.player.show(self.window)

    def cars_draw(self):
        if self.speed_of_scrolling > 7:

            if self.fps_count_cars > 80:
                self.oponents.append(Cars())
                self.fps_count_cars = 0

            for oponent in self.oponents:
                oponent.show(self.window)

                if oponent.get_pos()[1] > 1000:
                    self.oponents.remove(oponent)
                    del oponent

    def item_draw(self):

        if self.speed_of_scrolling > 7:

            if self.fps_count_item > 1000:
                self.items.append(choice([Fuel(), Life()]))
                self.fps_count_item = 0

            for item in self.items:
                item.show(self.window)

                if item.get_pos()[1] > 1000:
                    self.items.remove(item)
                    del item

    def game_logic(self):

        for oponent in self.oponents:
            self.player.point_count(oponent)
            oponent.change_position(self.player)

        for item in self.items:
            if item.interact(self.player):
                self.items.remove(item)
                del item

        for oponent in self.oponents:
            if oponent.interact(self.player):

                oponent.car_turn = "None"
                oponent.image = pygame.image.load("Images/various/explosion.png")
                oponent.width = oponent.image.get_width()
                oponent.height = oponent.image.get_height()
                oponent.taking_life = 0
                oponent.point = 0

        self.fps_count_fuel += 1
        if self.fps_count_fuel > 20:
            self.player.increase_fuel(-1)
            self.fps_count_fuel = 0
        if self.player.fuel <= 0:
            self.player.fuel = 100
            self.player.life -= 1


class Start(Window):
    def __init__(self):
        super().__init__()
        self.text = "START"
        self.text2 = "Press space bar to play"
        self.text3 = "The Speedest Car"
        self.font = pygame.font.Font('Fonts/RetroGaming.ttf', 30)
        self.font2 = pygame.font.Font('Fonts/RetroGaming.ttf', 24)
        self.font3 = pygame.font.Font('Fonts/VIDEOPHREAK.ttf', 70)
        self.text = self.font.render(self.text, False, (0, 0, 0))
        self.text2 = self.font2.render(self.text2, False, (0, 0, 0))
        self.text3 = self.font3.render(self.text3, False, (0, 0, 0))
        self.text_fps = 0

        self.entry_img = pygame.image.load("Images/backgrounds/Entry_pic.jpg")

    def show_backgroud(self):
        self.window.fill((54, 168, 50))
        self.window.blit(self.entry_img, (350, 300))


    def text_draw(self):
        self.window.blit(self.text, (490, 614))
        self.window.blit(self.text3, (220, 100))
        # Condition for blinking
        self.text_fps += 1
        if self.text_fps < self.blinking_value/2:
            self.window.blit(self.text2, (370, 690))
        elif self.text_fps > self.blinking_value:
            self.text_fps = 0


    def play_music(self):
        self.start_background_music.play()

    def stop_music(self):
        self.start_background_music.stop()


class Pause(Window):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('Fonts/RetroGaming.ttf', 30)
        self.text = self.font.render("PAUSE", False, (0, 0, 0))
        self.text2 = self.font.render("Press ESC to resume", False, (0, 0, 0))
        self.text_fps = 0

    def text_draw(self):
        self.window.blit(self.text, (500, 314))

        # Condition for blinking
        self.text_fps += 1
        if self.text_fps < self.blinking_value/2:
            self.window.blit(self.text2, (370, 690))
        elif self.text_fps > self.blinking_value:
            self.text_fps = 0

    def play_music(self):
        self.pause_background_music.play()

    def stop_music(self):
        self.pause_background_music.stop()


class End(Window):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font('Fonts/RetroGaming.ttf', 30)
        self.text = self.font.render("END", False, (0, 0, 0))
        self.text2 = self.font.render("Press (y) to play again", False, (0, 0, 0))
        self.text3 = self.font.render("Press (n) to end game", False, (0, 0, 0))

        self.text_fps = 0

    def text_draw(self):

        self.text4 = self.font.render(f"Best result: {self.player.read_high_score().split()[0]} ----"
                                      f" {self.player.read_high_score().split()[1]}", False, (0, 0, 0))

        self.window.blit(self.text, (520, 400))
        self.window.blit(self.text4, (270, 150))

        self.text_fps += 1
        if self.text_fps < self.blinking_value / 2:

            self.window.blit(self.text2, (340, 590))
            self.window.blit(self.text3, (350, 690))
        elif self.text_fps > self.blinking_value:
            self.text_fps = 0

    def play_music(self):
        self.end_background_music.play()

    def stop_music(self):
        self.end_background_music.stop()
