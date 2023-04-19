import pygame
from math import floor ,sqrt
from random import randint
from main import *
from pygame import mixer
resolution = (1280,720)




class Fizyka:
    def __init__(self,x,y,szerokosc,wysokosc,przyspieszenie,max_przyspieszenie ):
        self.x_cord = x
        self.y_cord = y
        self.Pozioma_Predkosc = 0
        self.Pionowa_Predkosc = 0
        self.przyspieszenie = przyspieszenie
        self.max_przyspieszenie = max_przyspieszenie
        self.szerokosc = szerokosc
        self.wysokosc = wysokosc
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.szerokosc, self.wysokosc)
        self.wczesniej_x = x
        self.wczesniej_y = y
        self.skakanie = False
        self.slidowanie = False
        self.cieszenie_sie = False
        self.gravity = 0.7
        self._start = 0
        self.smierc_postaci = False
        self.music = False
        self.uderzanie = False


    def hity(self, belki):
        self.Pionowa_Predkosc += self.gravity
        self.x_cord += self.Pozioma_Predkosc
        self.y_cord += self.Pionowa_Predkosc
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.szerokosc, self.wysokosc)
        for belka in belki:
            if belka.hitbox.colliderect(self.hitbox):
                if self.x_cord + self.szerokosc >= belka.x_cord + 1 > self.wczesniej_x + self.szerokosc:
                    self.x_cord = self.wczesniej_x
                    self.Pozioma_Predkosc = 0

                if self.x_cord <= belka.x_cord + belka.width - 1 < self.wczesniej_x:
                    self.x_cord = self.wczesniej_x
                    self.Pozioma_Predkosc = 0

                if self.y_cord + self.wysokosc >= belka.y_cord+ 1 > self.wczesniej_y:
                    self.y_cord = self.wczesniej_y
                    self.Pionowa_Predkosc = 0
                    self.skakanie = False
                if self.y_cord <= belka.x_cord + belka.width- 1 < self.wczesniej_y:
                    self.y_cord = self.wczesniej_y
                    self.Pionowa_Predkosc = 0

        self.wczesniej_x = self.x_cord
        self.wczesniej_y = self.y_cord

class Button:
    def __init__(self,x_cord, y_cord,file_name):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.button_image = pygame.image.load(f"{file_name}.png")
        self.hovered_button_image = pygame.image.load(f"{file_name}_2.png")
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.button_image.get_width(), self.button_image.get_height())

    def tick(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                return True

    def draw(self,screen):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.hovered_button_image,(self.x_cord, self.y_cord))
        else:
            screen.blit(self.button_image, (self.x_cord, self.y_cord))


class Health:
    def __init__(self, max_health=100):
        self.health = max_health
        self.max_health = max_health
        self.alive = True
        self.last_dmg = 0

    def health_tick(self,delta_tm):
        self.last_dmg += delta_tm

    def dealt_damage(self,damage, hit_speed):
        if self.last_dmg > hit_speed:
            self.health -= damage/2
            self.last_dmg = 0
            if self.health <=0:
                self.health = 0
                self.alive = False

    def draw_health(self, okno, x, y, max_width, height):
        percent_width = self.health / self.max_health
        width = round(max_width * percent_width)
        pygame.draw.rect(okno, (30,30,30), (x, y , max_width, height))
        pygame.draw.rect(okno, (30, 255, 30), (x, y, width, height))

class Bullet(Fizyka):
    def __init__(self, gun, speed, damage, x_side, y_side):
        super().__init__(gun.x_cord,gun.y_cord, 3,2,0,speed)
        self.gravity = 0.1
        c_side = sqrt(x_side**2 + y_side**2) # predkosc pocisuku w pionie i w poziomie
        step = c_side / speed
        x_speed = x_side /step
        y_speed = y_side /step
        self.Pozioma_Predkosc = x_speed
        self.Pionowa_Predkosc = y_speed
        self.damage = damage
        self.clock = 0
        self.exists = True

    def tick(self, belki,delta,enemies):
        self.hity(belki)
        self.clock += delta
        if self.clock > 5:
            self.exists = False
        for enemy in enemies:
            if enemy.hitbox.colliderect(self.hitbox):
                enemy.dealt_damage(self.damage,0)
                self.exists = False



    def draw(self, win, world_x):
        pygame.draw.rect(win,(5,5,5), (self.x_cord+world_x, self.y_cord, 20,6))

class Weapon:
    def __init__(self, speed, damage):
        self.x_cord = 0
        self.y_cord = 0
        self.speed = speed
        self.damage = damage
        self.bullets = []
        self.image = pygame.image.load("ak47.png")
        self.x_screen = 0
        self.world_x = 0
        self.clock = 1

    def shoot(self):
        if self.clock > 0.1:
            self.clock = 0
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x_side = x_mouse - self.x_screen - self.world_x
            y_side = y_mouse - self.y_cord
            self.bullets.append(Bullet(self, self.speed, self.damage, x_side, y_side))

    def tick(self, beams, player, delta, enemies):
        self.clock += delta
        self.x_cord = player.x_cord
        self.y_cord = player.y_cord
        for bullet in self.bullets:
            bullet.tick(beams, delta, enemies)
            if not bullet.exists:
                self.bullets.remove(bullet)

    def draw(self, win, x_screen, world_x):
        self.x_screen = x_screen
        self.world_x = world_x
        for bullet in self.bullets:
            bullet.draw(win, world_x)
        win.blit(self.image, (x_screen+ world_x, self.y_cord))

# Klasa Gracza

class Gracz(Fizyka, Health):
   def __init__(self):
       self.stand_img = (pygame.image.load("female_stand.png"))

       self.stand_left_img = pygame.transform.flip(pygame.image.load("female_stand.png") ,True, False)
       width = self.stand_img.get_width()
       height = self.stand_img.get_height()
       Health.__init__(self,100)
       Fizyka.__init__(self,55, 240, width, height, 0.2, 15)

       self.skakanie_right_img = pygame.image.load("female_jump.png")
       self.skakanie_left_img = pygame.transform.flip(pygame.image.load("female_jump.png"),True,False)

       self.slide_right_img = pygame.image.load("female_slide.png")
       self.slide_left_img = pygame.transform.flip(pygame.image.load("female_slide.png"),True,False)

       self.walk__right_img =[pygame.image.load("female_walk1.png"), pygame.image.load("female_walk2.png")]
       self.walk__left_img =[pygame.transform.flip(pygame.image.load("female_walk1.png"),True,False), pygame.transform.flip(pygame.image.load("female_walk2.png"),True, False)]

       self.bicie_right_img = pygame.image.load("female_hold1.png")
       self.bicie_left_img = pygame.transform.flip(pygame.image.load("female_hold1.png"),True, False)

       self.cieszenie= [pygame.image.load("female_cheer1.png"), pygame.image.load("female_cheer2.png")]

       self.smierc = pygame.image.load("female_hurt.png")

       self.cieszenie_index = 0
       self.walk_index = 0
       self.direction = 1
       self.running = 1
       self.slidowanie_music = mixer.Sound("footstep02.mp3")
       self.slidowanie_music_1 = mixer.Sound("footstep03.mp3")
       self.skakanie_music = mixer.Sound("Mario-jump-sound.mp3")
       self.smierc_music= mixer.Sound("Smierc.mp3")
       self.weapon = Weapon(20,20)

   def tick(self,keys,belki,delta_tm,enemies):
       self.hity(belki)
       self.health_tick(delta_tm)
       self.weapon.tick(belki,self, delta_tm,enemies)

       if not self.alive:
           self.smierc_postaci = True
           self.smierc_music.play()
           self.Pozioma_Predkosc = 0
           return

       if pygame.mouse.get_pressed(3)[0]:
           self.weapon.shoot()

       if keys[pygame.K_a]:
           self.Pozioma_Predkosc -=self.przyspieszenie
           if keys[pygame.K_a] and keys[pygame.K_d]:
               self.Pozioma_Predkosc +=self.przyspieszenie

       if keys[pygame.K_h]:
           self.uderzanie= True
        #  if self.hitbox.colliderect(player.hitbox):

       if keys[pygame.K_d]:
           self.Pozioma_Predkosc +=self.przyspieszenie
           if keys[pygame.K_d] and keys[pygame.K_a]:
               self.Pozioma_Predkosc -= self.przyspieszenie

       if keys[pygame.K_SPACE] and self.skakanie is False:
           self.Pionowa_Predkosc = -15
           self.skakanie = True
           self.skakanie_music.play()

       if self.Pozioma_Predkosc >0:
           self.direction = 1
       elif self.Pozioma_Predkosc <0:
           self.direction = 0
       if not (keys[pygame.K_d] or keys[pygame.K_a]):
           if self.Pozioma_Predkosc > 0:
               self.Pozioma_Predkosc = 0
           elif self.Pozioma_Predkosc < 0:
               self.Pozioma_Predkosc=0

       if keys[pygame.K_d] and keys[pygame.K_LCTRL] and self.skakanie is False:
           self.slidowanie = True
       if keys[pygame.K_a] and keys[pygame.K_LCTRL] and self.skakanie is False:
           self.slidowanie = True

       if keys[pygame.K_m]:
           self.cieszenie_sie = True



   def draw(self,okno, background):
       if background.width - resolution[0] / 2 > self.x_cord >= resolution[0] / 2:
           x_screen = resolution[0] / 2
       elif self.x_cord >= background.width - resolution[0] / 2:
           x_screen = self.x_cord - background.width + resolution[0]
       else:
           x_screen = self.x_cord


       self.draw_health(okno, x_screen, self.y_cord -15, self.szerokosc,10)
       self.weapon.draw(okno, self.x_cord,background.x_cord)

       # if self.slidowanie:
       #     self.music = True
       #     if self.music == True:
       #          self.slidowanie_music.play(1)
       #          self.slidowanie_music_1.play(1)

       if self.skakanie:
           if self.direction == 0:
               okno.blit(self.skakanie_left_img, (x_screen, self.y_cord))
           elif self.direction == 1:
               okno.blit(self.skakanie_right_img, (x_screen, self.y_cord))
       # if self.skakanie:
       #      self.skakanie_music.play(1)
       elif self.slidowanie:
          if self.direction== 0:
              okno.blit(self.slide_left_img, (x_screen, self.y_cord))
              self.slidowanie = False
          if self.direction == 1:
              okno.blit(self.slide_right_img, (x_screen, self.y_cord))
              self.slidowanie = False

       elif self.Pozioma_Predkosc != 0:
           if self.direction == 0:
               okno.blit(self.walk__left_img[floor(self.walk_index)], (x_screen, self.y_cord))
           elif self.direction == 1:
               okno.blit(self.walk__right_img[floor(self.walk_index)], (x_screen, self.y_cord))
           self.walk_index += 0.2
           if self.walk_index > 2:
               self.walk_index = 0

       elif self.cieszenie_sie:
           okno.blit(self.cieszenie[floor(self.cieszenie_index)], (x_screen, self.y_cord))
           self.cieszenie_index += 0.2
           if self.cieszenie_index > 2:
               self.cieszenie_index = 0
           self.cieszenie_sie = False

       elif self.uderzanie:
           if self.direction ==0:
                okno.blit(self.bicie_left_img,(x_screen,self.y_cord))
                self.uderzanie = False
           if self.direction ==1:
               okno.blit(self.bicie_right_img, (x_screen,self.y_cord))
               self.uderzanie = False

       elif self.smierc_postaci:
            okno.blit(self.smierc,(x_screen,self.y_cord))
       else:
           if self.direction == 0:
               okno.blit(self.stand_left_img, (x_screen, self.y_cord))
           elif self.direction == 1:
               okno.blit(self.stand_img, (x_screen, self.y_cord))


class Ghost(Fizyka,Health):
    def __init__(self, x,y):
        self.image = pygame.image.load("zombie_cheer1.png")
        width, height = self.image.get_size()
        Fizyka.__init__(self,x, y, width, height, 1, 3)
        Health.__init__(self, 100)
        self.gravity = 0.2

    def go_left(self):
        if -self.Pozioma_Predkosc < self.max_przyspieszenie:
            self.Pozioma_Predkosc -= self.przyspieszenie
    def go_right(self):
        if self.Pozioma_Predkosc < self.max_przyspieszenie:
            self.Pozioma_Predkosc += self.przyspieszenie
    def go_up(self):
        if -self.Pionowa_Predkosc < self.max_przyspieszenie:
            self.Pionowa_Predkosc -= self.gravity + self.przyspieszenie

    #def current(self):
     #   return (pygame.time.get_ticks() - self._start) / 1000
    def tick(self,belki,player,delta):
        self.hity(belki)
        self.health_tick(delta)
        if self.hitbox.colliderect(player.hitbox):
            player.dealt_damage(20,0.5)

        if not self.hitbox.colliderect(player.hitbox):
            if self.x_cord > player.x_cord:
                self.go_left()
            elif self.x_cord < player.x_cord:
                self.go_right()
            if randint(0,30) == 15:
                self.go_up()
                self.go_left()

    def draw(self,okno,world_x):
        okno.blit(self.image, (self.x_cord + world_x, self.y_cord))
        self.draw_health(okno, self.x_cord+ world_x, self.y_cord - 15, self.szerokosc, 10)



class Belka:
    def __init__(self, x, y, width, height):
        self.x_cord = x
        self.y_cord = y
        self.width = width
        self.height = height
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, win, background_x):
        pygame.draw.rect(win, (200, 200, 200), (self.x_cord + background_x, self.y_cord, self.width, self.height))


class BackGround:
    def __init__(self):
        self.x_cord = 0
        self.y_cord = 0
        self.image = pygame.image.load("grafika_Las41.jpg")
        self.width  = self.image.get_width()
    def tick(self,player):
        if self.width - resolution[0] / 2 > player.x_cord >= resolution[0] / 2:
            self.x_cord = -player.x_cord + resolution[0] / 2
        elif player.x_cord >= self.width - resolution[0] / 2:
            self.x_cord = - self.width + resolution[0]
        else:
            self.x_cord =0


    def draw(self,okno):
        okno.blit(self.image, (self.x_cord, self.y_cord))