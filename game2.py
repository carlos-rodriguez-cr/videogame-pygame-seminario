# -*- coding: utf-8 -*-

import pygame

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)





def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_health_bar(surface, x, y, percentage):  # Barra de salud
    BAR_WIDTH = 200
    BAR_HEIGHT = 15
    fill = (percentage / 100) * BAR_WIDTH
    border = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('images/kate.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.frame = 0
        #Arrays para animaciones
        self.animar_izquierda = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) } # (pos x, pos y, tam x, tam y)
        self.animar_derecha = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.animar_arriba = { 0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76) }
        self.animar_abajo = { 0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76) }
        self.health = 100

    def get_frame(self, frame_set): # Metodo para recorrer el array de sprites para la animacion en bucle (0,1,2,0,1,2,0,1,2)
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect): # Implementacion del metodo get_frame en la imagen
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self, direction):
        if direction == 'left':
            self.clip(self.animar_izquierda)
            self.rect.x -= 10
        if direction == 'right':
            self.clip(self.animar_derecha)
            self.rect.x += 10
        if direction == 'up':
            self.clip(self.animar_arriba)
            self.rect.y -= 10
        if direction == 'down':
            self.clip(self.animar_abajo)
            self.rect.y += 10
        if direction == 'left' and direction == 'down':
            self.rect.x -= 10
            self.rect.y += 10

        if direction == 'stand_left':
            self.clip(self.animar_izquierda[0])
        if direction == 'stand_right':
            self.clip(self.animar_derecha[0])
        if direction == 'stand_up':
            self.clip(self.animar_arriba[0])
        if direction == 'stand_down':
            self.clip(self.animar_abajo[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())


        #Colisiones con los bordes de la ventana
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT



    def process_events(self, event):
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                self.update('up')
            if event.key == pygame.K_DOWN:
                self.update('down')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')

def main():
    pygame.init()

    pygame.mixer.music.load("music/musica.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load("images/background.png").convert()

    pygame.display.set_caption("Prueba")
    clock = pygame.time.Clock()
    player = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) #Se genera jugador en el centro
    score = 0
    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        player.process_events(event)

        screen.blit(background, [0, 0])

        screen.blit(player.image, player.rect)
        draw_text(screen, "Score:", 25, SCREEN_WIDTH // 2.15, 10)
        draw_text(screen, str(score), 25, SCREEN_WIDTH // 2, 10)
        draw_health_bar(screen, 10, 15, player.health)







        pygame.display.flip()
        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":  #Llama a la funcion main para el arranque del juego
    main()
