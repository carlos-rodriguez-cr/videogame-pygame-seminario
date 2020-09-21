import pygame


SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1280
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("images/player.png").convert()

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()   # Posicionar sprite
        self.rect.x = int(SCREEN_WIDTH/2)   # Centro de pantalla eje x
        self.rect.y = int(SCREEN_HEIGHT/2)  # Centro de pantalla eje y

        self.speed_x = 0
        self.speed_y = 0

    def changespeedx(self, x):
        self.speed_x += x


    def changespeedy(self, y):
        self.speed_y += y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


class Game(object):
    def __init__(self):
        self.game_over = False
        self.background = pygame.image.load("images/background.png").convert()

        self.score = 0  # Puntaje del pj

        self.all_sprite_list = pygame.sprite.Group()

        self.player = Player() #Se genera la instancia Jugador
        self.all_sprite_list.add(self.player)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()  # Click derecho para reiniciar el juego si game_over es True

            if event.type == pygame.KEYDOWN: #apretar tecla
                if event.key == pygame.K_LEFT:
                    self.player.changespeedx(-3)

                if event.key == pygame.K_RIGHT:
                    self.player.changespeedx(3)

                if event.key == pygame.K_UP:
                    self.player.changespeedy(-3)

                if event.key == pygame.K_DOWN:
                    self.player.changespeedy(3)


            if event.type == pygame.KEYUP: #soltar tecla
                if event.key == pygame.K_LEFT:
                    self.player.changespeedx(3)
                if event.key == pygame.K_RIGHT:
                    self.player.changespeedx(-3)
                if event.key == pygame.K_UP:
                    self.player.changespeedy(3)
                if event.key == pygame.K_DOWN:
                    self.player.changespeedy(-3)
        return False

    def run_logic(self):
        if not self.game_over:
            self.all_sprite_list.update()

    def display_frame(self, screen):
        screen.blit(self.background, [0, 0])

        if self.game_over:
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, Click To Continue", True, WHITE)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprite_list.draw(screen)

        pygame.display.flip()


def main():  # Clase principal
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    done = False
    clock = pygame.time.Clock()
    pygame.display.set_caption("Nombre del juego")
    game = Game()  # Reiniciar juego

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(60)  # FPS
    pygame.quit()


if __name__ == "__main__": #Llama a la funcion principal
    main()
