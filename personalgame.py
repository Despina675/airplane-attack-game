import pygame
import random

#screen of game
pygame.init()
screen_size = pygame.display.Info()
screen_width = screen_size.current_w - 100
screen_height = screen_size.current_h - 100

screen = pygame.display.set_mode((screen_width,screen_height))

#gia dio othones: paixnidi - game over.
running = True
gameover = False

#metvlites gameplay
hp = 3 #zoes
points = 0 #points
r_dg = 0 #rockets dodged
r_term = 0 #enemies terminated
starttime = pygame.time.get_ticks() #gia sinoliko xrono (simio enarxis)

#genikes leitourgies
font = pygame.font.SysFont("Tahoma", 25)
font_large = pygame.font.SysFont("Tahoma", 40)
pressed = pygame.key.get_pressed()

#Class a: paixtes - 1 - aeroplano (plane):
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player,self).__init__() #
        self.surf = pygame.image.load('airplane1.png').convert()
        self.surf.set_colorkey((255,255,255),pygame.RLEACCEL) #afairo to aspro background tis eikonas me ti methodo RLEACCEL
        self.rect = self.surf.get_rect() #tou leei oti siberiferetai san orthogonio
#to kouname me velakia i wasd
    def update(self, pressed):
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.rect.move_ip(0, -5)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.rect.move_ip(0, 5)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.rect.move_ip(5, 0)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.rect.move_ip(-5, 0)
#ti kanei an ftasei sto orio tis othonis:
#pros to paron, vgainei apo tin alli
        if self.rect.top < 0:
            self.rect.bottom = screen_height
        if self.rect.left < 0:
            self.rect.right = screen_width
        if self.rect.right > screen_width:
            self.rect.left = 0
        if self.rect.bottom > screen_height:
            self.rect.top = 0

#Class b: sinefa (clouds) - apira - cloud/newcloud:
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud,self).__init__()
        self.surf = pygame.image.load('cloud1.png').convert()
        self.surf.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(screen_width+30, screen_width+80), random.randint(40, screen_height - 40)))
        #proxora pros aristera me rithmo 1
    def update(self):
        self.rect.move_ip(-1,0)
        if self.rect.right < 0:
            self.kill() #to katastrefo

#Class c: rouketes (rockets) (enemies) - apira - rocket/newrocket:
class Rocket(pygame.sprite.Sprite):
    def __init__(self):
        super(Rocket,self).__init__()
        self.image = pygame.image.load('rocket1.png')
        self.image = pygame.transform.scale(self.image, (40,20))
        self.surf = self.image.convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(random.randint(screen_width+20, screen_width+70), random.randint(30, screen_height - 30)))
#metakinoude pros ta aristera me rithmo 2 kai taladevodai (os astathi pirinika)
#mas dinoun podo an ta apofigoume
    def update(self):
        self.rect.move_ip(-2, random.randint(-1, 1))
        if self.rect.right < 0:
            global points, r_dg
            points += 1
            r_dg += 1
            self.kill() #to katastrefo

#Class d: piravloi (missiles)- osa dimiourgiso - missile/new missile:
class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super(Missile,self).__init__()
        self.image = pygame.image.load('missile.png')
        self.image = pygame.transform.scale(self.image, (225/3,225/3))
        self.surf = self.image.convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(plane.rect.x, plane.rect.y))
    def update(self):
        self.rect.move_ip(2,0) #meta isos na afxano tin taxitita ton missiles?
        #paei dexia gia na xtipisei ta rockets
        #an petixei rouketa skotonetai, ti skotonei kai dinei 2 podous
        if pygame.sprite.spritecollideany(self, rockets):
            global points, r_term
            points += 2
            r_term += 1
            colr = pygame.sprite.spritecollideany(self, rockets) #i rouketa pou xtipise
            colr.kill()
            self.kill() #na pethanei kai o piravlos

plane = Player()
clock = pygame.time.Clock()

#events
ENEMY = pygame.USEREVENT + 1
CLOUD = pygame.USEREVENT + 2
#poso sixna (se milliseconds) emfanizodai rockets kai clouds
pygame.time.set_timer(ENEMY, 3000)
pygame.time.set_timer(CLOUD, 1500) #i 2000

#Groups
rockets = pygame.sprite.Group() #group enemies
clouds = pygame.sprite.Group() #group sinefon
missiles = pygame.sprite.Group() #group piravlon
all_objects = pygame.sprite.Group() #group olon iptamenon adicimenon + player
all_objects.add(plane)

while running:
    pressed = pygame.key.get_pressed()
    if not gameover: # = me gameover == False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False

            elif event.type == ENEMY:
                newrocket = Rocket()
                rockets.add(newrocket)
                all_objects.add(newrocket)
                newrocket.update()
                screen.blit(newrocket.surf, newrocket.rect)

            elif event.type == CLOUD:
                newcloud = Cloud()
                clouds.add(newcloud)
                all_objects.add(newcloud)
                screen.blit(newcloud.surf, newcloud.rect)

            elif pressed[pygame.K_SPACE]:
                newmissile = Missile()
                missiles.add(newmissile)
                all_objects.add(newmissile)
                screen.blit(newmissile.surf, newmissile.rect)


        screen.fill((50, 190, 215))
        screen.blit(plane.surf, plane.rect)

        plane.update(pressed)
        clouds.update()
        rockets.update()
        missiles.update()

        #dimiourgise ta stin othoni
        for object in all_objects:
            screen.blit(object.surf, object.rect)

        #ama xtipiso rouketa
        if pygame.sprite.spritecollideany(plane, rockets):
            hp = hp - 1
            col = pygame.sprite.spritecollideany(plane, rockets)  # i rouketa pou xtipisa
            col.kill()


        #zoes 'animation'
        if (3 + 1 > hp) and (0 < hp):
            image = pygame.image.load(str(hp) + 'lives.png').convert_alpha()
            screen.blit(image, (screen_width - 300, -70))

        #deixne podous
        points_text = font.render("Score: " + str(points), True, (0, 0, 0))
        screen.blit(points_text, (10, 10))

        #deixne ora paixnidiou
        finishtime = pygame.time.get_ticks() - starttime
        global flighttime
        flighttime = (round(finishtime / 1000, 2))
        timer_text = font.render("Flight time: " + str(flighttime) + "s", True, (0, 100, 0))
        screen.blit(timer_text, (10, screen_height - 50))

        #lixe paixnidi
        if hp == 0:
            gameover = True
            plane.kill()

    #an xaso:
    elif gameover:
        screen.fill((0, 0, 0))
        gameovertext = font_large.render("GAME OVER.", True, (255, 0, 0))
        pointstext = font.render("Final Score: " + str(points), True, (0, 255, 0))
        r_dgtext = font.render(str(r_dg) + " enemies dodged,", True, (0, 180, 0))
        r_termtext = font.render(str(r_term) + " enemies terminated successfully (by missiles).", True, (0, 180, 0))
        timetext = font.render("Flight time, before signal loss: " + str(flighttime) + "s", True, (0, 120, 0))
        instructiontext = font.render("Press R to play again, E to escape (there is no escape from the enemy!)", True, (0,0,255))
        missiletext = font.render("Press Space to launch missile at your aircraft's altitude.", True, (0,0,255))
        screen.blit(gameovertext, ((screen_width-200)/2, 180))
        screen.blit(pointstext, (200, 320))
        screen.blit(r_dgtext, (200, 360))
        screen.blit(r_termtext, (200, 390))
        screen.blit(timetext, (200,440))
        screen.blit(instructiontext, (200, 540))
        screen.blit(missiletext, (200, 570))

        #afou xaso, gia na xanapexo i na kleiso to parathiro
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    running = False
                elif event.key == pygame.K_r:
                    plane = Player()
                    hp = 3
                    clouds.empty()
                    rockets.empty()
                    all_objects.empty()
                    all_objects.add(plane)
                    starttime = pygame.time.get_ticks()
                    points = 0
                    gameover = False

    pygame.display.flip()
    clock.tick(100)

