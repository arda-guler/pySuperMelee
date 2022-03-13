import math
M_PI = math.pi

import numpy as np
import pygame as g

class spaceship:
    def __init__(self, name, model, size, sprite, max_crew, max_energy,
                 accel_rate, turn_rate, energy_generation, projectile, attack_energy,
                 sounds, max_speed, attack_cooldown):
        self.name = name
        self.model = model
        self.size = size
        self.sprite = sprite
        self.max_crew = max_crew
        self.max_energy = max_energy
        self.accel_rate = accel_rate
        self.crew = max_crew
        self.energy = max_energy
        self.turn_rate = turn_rate
        self.energy_generation = energy_generation
        self.projectile = projectile
        self.attack_energy = attack_energy
        self.sounds = sounds
        self.max_speed = max_speed
        self.attack_cooldown = attack_cooldown
        self.current_cooldown = 0
        self.pos = np.array([0.0,0.0])
        self.vel = np.array([0.0,0.0])
        self.orient = 0
        self.orient_matrix = np.array([[1,0],[0,1]])

        self.textures = []
        for i in range(16):
            textures_path = "data/img/ships/" + sprite + "/" + sprite + "_" + str(i+1) + ".png"
            new_texture = g.image.load(textures_path)
            self.textures.append(new_texture)

    def get_texture(self):
        index = int((self.orient * 16) / (2 * M_PI) + 0.5)
        index = max(min(index, 15), 0)
        return self.textures[index]

    def set_pos(self, pos):
        self.pos = pos

    def update_pos(self, dt):
        self.pos += self.vel * dt

    def accel(self, dt):
        self.vel += np.array(self.orient_matrix[1]) * self.accel_rate * dt

        # limit velocity to max allowed
        if np.linalg.norm(self.vel) > self.max_speed:
            self.vel = (self.vel/np.linalg.norm(self.vel)) * self.max_speed

    def rotate(self, direction, dt):
        self.orient += direction * self.turn_rate * dt
        
        if self.orient > 2 * M_PI:
            self.orient = self.orient - (2 * M_PI)
        elif self.orient < 0:
            self.orient = self.orient + 2 * M_PI

        x_rad = (self.orient - M_PI * 0.5)
        if x_rad < 0:
            x_rad = x_rad + 2 * M_PI
        elif x_rad > 2 * M_PI:
            x_rad = x_rad - 2 * M_PI
            
        x = np.array([math.cos(x_rad), math.sin(x_rad)])
        y = np.array([-math.sin(self.orient), math.cos(self.orient)])

        self.orient_matrix = np.array([x, y])

    def set_orient(self, orient):
        self.orient = orient

        if self.orient > 2 * M_PI:
            self.orient = self.orient - (2 * M_PI)
        elif self.orient < 0:
            self.orient = self.orient + 2 * M_PI

        x_rad = (self.orient - M_PI * 0.5)
        if x_rad < 0:
            x_rad = x_rad + 2 * M_PI
        elif x_rad > 2 * M_PI:
            x_rad = x_rad - 2 * M_PI
            
        x = np.array([math.cos(x_rad), math.sin(x_rad)])
        y = np.array([-math.sin(self.orient), math.cos(self.orient)])

        self.orient_matrix = np.array([x, y])

    def update_energy(self, dt):
        self.energy += self.energy_generation * dt

        if self.energy > self.max_energy:
            self.energy = self.max_energy

        if self.current_cooldown > 0:
            self.current_cooldown -= dt

    def attack(self):
        self.energy -= self.attack_energy
        self.current_cooldown = self.attack_cooldown

    def damage(self, damage):
        self.crew -= damage

    def check_collision(self, obj):
        if np.linalg.norm(self.pos - obj.pos) < self.size + obj.size:
            return True
        else:
            return False
