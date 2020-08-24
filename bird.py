# bird.py
import pygame
import os


class Bird:
    BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
                   pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
                   pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.frames_since_last_jump = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.BIRD_IMAGES[0]

    def jump(self):
        self.vel = -10.5
        self.frames_since_last_jump = 0
        self.height = self.y

    def move(self):
        self.frames_since_last_jump += 1
        displacement = min(16, ((self.vel * self.frames_since_last_jump) + (1.5 * self.frames_since_last_jump ** 2)))

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -70:
                self.tilt -= self.ROTATION_VEL

    def draw(self, window):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.BIRD_IMAGES[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.BIRD_IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.BIRD_IMAGES[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.BIRD_IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.BIRD_IMAGES[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.BIRD_IMAGES[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rectangle = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        window.blit(rotated_image, new_rectangle.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
