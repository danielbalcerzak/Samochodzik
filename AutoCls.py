import datetime

import pygame
import random
import os


class Auto:
    x_left_border = 550
    x_right_border = 935
    y_top_border = 100
    y_down_border = 700
    crash_image = "Images/various/explosion.png"
    cars_images = ["Images/cars/samochod (1).png", "Images/cars/samochod (2).png", "Images/cars/samochod (3).png",
                   "Images/cars/samochod (4).png", "Images/cars/samochod (5).png", "Images/cars/samochod (6).png",
                   "Images/cars/samochod (7).png", "Images/cars/samochod (8).png", "Images/cars/samochod (9).png",
                   "Images/cars/samochod (10).png", "Images/cars/samochod (11).png", "Images/cars/samochod (12).png",
                   "Images/cars/samochod (13).png", "Images/cars/samochod (14).png", "Images/cars/samochod (15).png",
                   "Images/cars/samochod (16).png", "Images/cars/samochod (17).png", "Images/cars/samochod (18).png",
                   "Images/cars/samochod (19).png"]

    def __init__(self):
        self.x_pos = 700
        self.y_pos = 700
        self.max_fuel = 100
        self.fuel = 100
        self.max_lifes = 3
        self.life = 1
        self.speed = 6
        self.image = pygame.image.load("Images/cars/samochod (17).png")
        self.image.convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.point = 1
        self.shape = None

    def show(self, window):
        self.y_pos += self.speed - 2

        self.shape = pygame.Rect(self.get_pos()[0], self.get_pos()[1], self.width, self.height)
        window.blit(self.image, (self.x_pos, self.y_pos))

    def get_pos(self):
        return [self.x_pos, self.y_pos]

    def change_position(self, player):
        if abs(self.y_pos - player.y_pos) < 100:
            self.x_pos += 1


class PlayerCar(Auto):
    car_stoping_value = 3

    def __init__(self):
        super().__init__()
        self.life = 3
        self.have_point = 0

    def get_point(self):
        return self.have_point

    def set_point(self, value):
        self.have_point = value

    def increase_point(self, value):
        self.have_point += value

    points = property(get_point, set_point)

    def control_car(self, keys):
        if keys[pygame.K_RIGHT]:
            if self.x_pos <= self.x_right_border:
                self.x_pos += self.speed
        if keys[pygame.K_LEFT]:
            if self.x_pos >= self.x_left_border:
                self.x_pos -= self.speed
        if keys[pygame.K_UP]:
            if self.y_pos >= self.y_top_border:
                self.y_pos -= self.speed
        if keys[pygame.K_DOWN]:
            if self.y_pos <= self.y_down_border:
                self.y_pos += self.speed

    def save_high_score(self):
        if os.path.exists("highscore.txt"):
            file = open("highscore.txt", "r")
            score = file.readline()
            file.close()
            if int(score.split()[0]) < self.get_point():
                outfile = open("highscore.txt", "w")
                now = datetime.datetime.now()
                outfile.write(str(self.get_point())+" "+now.strftime("%m/%d/%Y, %H:%M:%S"))
                outfile.close()
        else:
            outfile = open("highscore.txt", "w")
            now = datetime.datetime.now()
            outfile.write(str(self.get_point())+" "+now.strftime("%m/%d/%Y, %H:%M:%S"))
            outfile.close()

    def read_high_score(self):
        file = open("highscore.txt", "r")
        score = file.readline()
        file.close()
        return score

    def show(self, window):
        keys = pygame.key.get_pressed()
        self.control_car(keys)
        if self.y_pos <= self.y_down_border:
            self.y_pos += self.speed / self.car_stoping_value

        self.shape = pygame.Rect(self.get_pos()[0], self.get_pos()[1], self.width, self.height)
        window.blit(self.image, (self.x_pos, self.y_pos))

    def get_speed(self):
        return self.speed

    def set_speed(self, value):
        self.speed = value

    def increase_speed(self, value):
        self.speed += value

    def decrease_speed(self, value):
        self.speed -= value

    speed_func = property(get_speed, set_speed)

    def get_fuel(self):
        return self.fuel

    def set_fuel(self, value):
        self.fuel = value
        if self.fuel > self.max_fuel:
            self.fuel = self.max_fuel

    def increase_fuel(self, value):
        self.fuel += value
        if self.fuel > self.max_fuel:
            self.fuel = self.max_fuel

    fuel_func = property(get_fuel, set_fuel)

    def get_lifes(self):
        return self.life

    def set_lifes(self, value):
        self.life += value
        if self.life > self.max_lifes:
            self.life = self.max_lifes

    def increase_lifes(self, value):
        self.life += value
        if self.life >= self.max_lifes:
            self.life = self.max_lifes

    life_func = property(get_lifes, set_lifes)

    def point_count(self, oponent):
        if oponent.get_pos()[1] == self.y_down_border:
            self.increase_point(oponent.point)
            self.save_high_score()

    def reset_car_progress(self):
        self.fuel = self.max_fuel
        self.points = 0
        self.life = self.max_lifes


class Cars(Auto):

    def __init__(self):
        super().__init__()
        self.x_pos = random.randint(self.x_left_border, self.x_right_border)
        self.y_pos = -100
        self.image = pygame.image.load(random.choice(self.cars_images))
        self.image.convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.taking_life = -1
        self.car_turn = random.choice(["Left", "Right", "None"])
        self.crash_sound = pygame.mixer.Sound("Sounds/crash_sound.wav")

    def play_music(self, loop=0):
        self.crash_sound.play(loops=loop)

    def interact(self, player):
        if self.shape.colliderect(player.shape):
            player.increase_lifes(self.taking_life)
            self.play_music(loop=0)
            return True

    def change_position(self, player):
        if abs(self.y_pos - player.y_pos) < random.randint(30, 100):
            if self.car_turn == "Right":
                if self.x_pos <= self.x_right_border:
                    self.x_pos += self.speed
            elif self.car_turn == "Left":
                if self.x_pos >= self.x_left_border:
                    self.x_pos -= self.speed
            else:
                pass


class CrashCar(Cars):

    def __init__(self):
        super().__init__()
        self.car_turn = "None"
        self.image = pygame.image.load("Images/various/explosion.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.taking_life = 0
