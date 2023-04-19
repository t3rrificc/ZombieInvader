
from game_module import *
from pygame import mixer
import random
pygame.init()
resolution = (1280,720)


screen = pygame.display.set_mode(resolution)



#Pętla gry
def lvl_one():
    gracz = Gracz()
    ghost = Ghost(300, 100)
    ghost1 = Ghost(700,200)
    ghost2 = Ghost(500,200)
    ghost3 = Ghost(900,200)
    background = BackGround()
    clock = 0
    belki =[

        Belka(0, 690, 5000, 40),
        Belka(1200,600,30,120),
        Belka(0,600,30,120)
    ]





    Okno_Gry= True
    while Okno_Gry:
        delta = pygame.time.Clock().tick(60) / 1000
        clock += delta
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Okno_Gry = False



        keys = pygame.key.get_pressed()

        gracz.tick(keys, belki, delta,[ghost,ghost1,ghost2,ghost3])

        ghost.tick(belki, gracz, delta)
        ghost1.tick(belki, gracz, delta)
        ghost2.tick(belki, gracz, delta)
        ghost3.tick(belki, gracz, delta)

        background.tick(gracz)
        if not ghost.alive:
            ghost = Ghost(random.randint(300,1200), random.randint(200,600))
        elif not ghost1.alive:
            ghost1 = Ghost(random.randint(300,1200), random.randint(200,600))
        elif not ghost2.alive:
            ghost2 = Ghost(random.randint(300,1200), random.randint(200,600))
        elif not ghost3.alive:
            ghost3 = Ghost(random.randint(300,1200), random.randint(200,600))


        background.draw(screen)

        ghost.draw(screen,background.x_cord)
        ghost1.draw(screen, background.x_cord)
        ghost2.draw(screen, background.x_cord)
        ghost3.draw(screen, background.x_cord)
        gracz.draw(screen,background)

        for belka in belki:
            belka.draw(screen,background.x_cord)
        pygame.display.update()

def main():
    Okno_Gry = True
    clock = 0
    background = pygame.image.load("Menu1.png")
    play_button = Button(460,220,"Graj")
    while Okno_Gry:
        mixer.music.load("LOL.mp3")
        mixer.music.play(-1)
        clock += pygame.time.Clock().tick(60) / 1000  # maksymalnie 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # jeśli gracz zamknie okienko
                Okno_Gry = False

        if play_button.tick():
            lvl_one()


        screen.blit(background, (0,0))
        play_button.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
