import pygame
import random
import string

class ButtonP(pygame.sprite.Sprite):

    def __init__(self, imagen, imagen1 , x, y):
        super(ButtonP, ButtonP).__init__(self)
        self.normal = imagen
        self.seleccion = imagen1
        self.actual = self.normal
        self.rect = self.actual.get_rect()
        self.rect.left , self.rect.top = (x,y)
        self.x = x
        self.y = y

    def update(self, vetana, cursor, agregar):
        if cursor.colliderect(self.rect):
            self.actual = self.seleccion
        else:
            self.actual = self.normal
        vetana.blit(self.actual, self.rect)
        vetana.blit(agregar, (self.x + 20, self.y + 25))
