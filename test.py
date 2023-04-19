import pygame, os, time
from Images import Images
from states import States
from player import Player
from level import Level
from text import Text

# centrowanbie okna
os.environ['SDL_VIDEO_CENTERED'] = '1'

# zainicjowanie gry
pygame.init()

clock = pygame.time.Clock()

Images.background_image = pygame.image.load(os.path.join('./Grafiki/space4.jpg')).convert()
Images.player_image = pygame.image.load(os.path.join("./Grafiki/spaceship2.png"))
Images.enemy_image = pygame.image.load(os.path.join("./Grafiki/enemy2.png"))
Images.bullet_enemy_image = pygame.image.load(os.path.join("./Grafiki/bullet2.png"))
Images.bullet_image = pygame.image.load(os.path.join("./Grafiki/Bullet1.png"))

# ustawienie wymiarow

# tytul okna
pygame.display.set_caption('spaceinvaders')

# ikona okna
window_icon = pygame.image.load("./Grafiki/logo.png")
pygame.display.set_icon(window_icon)

score = States.score
life = States.life
kills = States.kills
difficulty = States.difficulty
level = States.level
single_frame_rendering_time = States.single_frame_rendering_time
total_time = States.total_time
frame_count = States.frame_count
fps = States.fps

States.player = Player(Images.player_image)
States.player.rect.y = States.HEIGHT - 80
States.player.rect.x = 350

States.current_level = Level(States.player)
States.player.level = States.current_level
States.finish_text = Text("KONIEC GRY", States.LIGHTBLUE)


# petla gry
def level1():
    window_open = True
    active_game = True
    while window_open:
        start_time = time.time()
        States.screen.blit(Images.background_image, (0, 0))

        # petla zdarzen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    window_open = False
            elif event.type == pygame.QUIT:
                window_open = False

            if active_game:
                States.player.get_event(event)

        if active_game:
            if not States.player.lifes:
                window_open = False
                pygame.time.delay(500)
                States.screen.fill(States.LIGHTPURPLE)
                font = pygame.font.SysFont("freesansbold", 64)
                gameover_sprint = font.render("GAME OVER", True, (255, 255, 255))
                States.screen.blit(gameover_sprint, (260, 268))
                pygame.display.flip()
                pygame.time.delay(2000)
                States.current_level.update()

            # rysowanie i aktualizacja obiektow
            States.player.draw(States.screen)
            States.current_level.update()
            States.current_level.draw(States.screen)

        # aktualizacja okna pygame
        # scoreboard()
        pygame.display.flip()
        clock.tick(30)

        States.frame_count += 1
        States.end_time = time.time()
        States.single_frame_rendering_time = States.end_time - start_time
        States.total_time = States.total_time + States.single_frame_rendering_time
        if States.total_time >= 1.0:
            States.fps = frame_count
            States.frame_count = 0
            States.total_time = 0


def main():
    Okno_Gry = True
    clock = 0
    background = pygame.image.load("Menu1.png")
    play_button = Button(460, 220, "Graj")
    while Okno_Gry:
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                Okno_Gry = False

        if play_button.tick():
            lvl_one()

        screen.blit(background, (0, 0))
        play_button.draw(screen)
        pygame.display.update()


if name == "main":
    main()

pygame.quit()
