import math
M_PI = math.pi

import numpy as np

class projectile:
    def __init__(self, name, model, size, sprite, damage, pos, orient, orient_matrix, speed,
                 target, homing, sounds, expire_time):
        self.name = name
        self.model = model
        self.size = size
        self.sprite = sprite
        self.damage = damage
        self.pos = pos
        self.orient = orient
        self.orient_matrix = orient_matrix
        self.speed = speed
        self.target = target
        self.homing = homing
        self.sounds = sounds
        self.expire_time = expire_time

    def get_texture(self):
        return self.sprite

    def update_pos(self, dt):
        self.pos += self.orient_matrix[1] * self.speed * dt

    def update_expiration(self, dt):
        if not self.expire_time:
            return False
        
        self.expire_time -= dt

        # return true when expired
        if self.expire_time <= 0:
            return True
        else:
            return False

    def home_on_target(self):
        if self.homing and self.target:
            move_dir = self.target.pos - self.pos
            
            self.orient = np.arctan2(move_dir[1], move_dir[0]) - (M_PI * 0.5)

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

    def check_collision(self, obj):
        if np.linalg.norm(self.pos - obj.pos) < self.size + obj.size:
            return obj
        else:
            return False
