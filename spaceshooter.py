import pygame
from sys import exit
from random import randint, choice

pygame.init()

screen = pygame.display.set_mode((1000,500))
pygame.display.set_caption("Spaceship Game")

clock = pygame.time.Clock()

home_screen = True
game_active = False
game_over_screen = False
cut_scene = False

lives = 10
lives_remaining = lives

scoree = 0
scores = []
collisions = []

text = pygame.font.Font(None, 40)
title_font = pygame.font.Font('PixelifySans-SemiBold.ttf', 80)

class Laser(pygame.sprite.Sprite):
    def __init__(self, ship, x, y):
        super().__init__()
        self.ship = ship

        self.image = pygame.Surface((40, 5))
        self.rect = self.image.get_rect(center = (x,y))

        if self.ship == "player":
            pygame.draw.rect(self.image, "red", self.image.get_rect(), 2, 2)
        else:
            pygame.draw.rect(self.image, "blue", self.image.get_rect(), 2, 2)

    def update(self):
        if self.ship == "player":
            self.rect.x += 50
        else:
            self.rect.x -= 20

        if self.rect.x > 999 or self.rect.x < 0: self.kill()


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        ship_image = pygame.image.load("pixelrocket1.png").convert_alpha()
        ship_image = pygame.transform.rotozoom(ship_image, -90, 0.65)
        ship_image_2 = pygame.image.load("spaceshippixel2.png").convert_alpha()
        ship_image_2 = pygame.transform.rotozoom(ship_image_2, -90, 0.65)
        self.ship_image_list = [ship_image,ship_image_2]
        self.ship_image_index = 0

        self.image = self.ship_image_list[self.ship_image_index]
        self.rect = self.image.get_rect(center = (150,250))

    def ship_animation(self):
        self.ship_image_index += 0.1
        if self.ship_image_index > len(self.ship_image_list):
            self.ship_image_index = 0
        self.image = self.ship_image_list[int(self.ship_image_index)]

    def movement(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and game_active:
            self.rect.y += 5
            if self.rect.bottom > 500: self.rect.bottom = 500
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and game_active:
            self.rect.y -= 5
            if self.rect.top < 0: self.rect.top = 0

    def update(self):
        self.ship_animation()
        self.movement()

class Villian(pygame.sprite.Sprite):
    def __init__(self, skin):
        super().__init__()

        commander_image = pygame.image.load("commander.png").convert_alpha()
        commander_image = pygame.transform.rotozoom(commander_image, 90, 0.6)

        nuke_image = pygame.image.load("purplenuke.png").convert_alpha()
        nuke_image = pygame.transform.rotozoom(nuke_image, 90, 0.3)

        villian_skin_list = [commander_image, nuke_image]
        self.skin_index = skin

        self.image = villian_skin_list[self.skin_index]
        self.rect = self.image.get_rect(midleft = (1000, randint(100,400)))

        self.laser_cooldown = 0

    def shoot(self):
            if self.skin_index == 0:
                bad_laser = Laser("commander", self.rect.x, self.rect.centery)
                bad_lasers.add(bad_laser)
                

    def update(self):
            self.rect.x -= 10
            if self.skin_index == 0 and self.rect.centerx<=850: 
                self.rect.x += 8

            now = pygame.time.get_ticks()
            if now - self.laser_cooldown >= 1000:
                self.shoot()
                self.laser_cooldown = now
            
            if self.rect.x < 0: self.kill()

class Stars():
    def __init__(self, xcor, ycor):
        self.ycor = ycor
        self.xcor = xcor
stars = {}
for i in range(300):
    stars[f"{i}"] = Stars(randint(1, 999), randint(1,499))

def check_player_damage(current_lives):
    if pygame.sprite.spritecollide(player.sprite, villians, True):
        current_lives -= 2
    if pygame.sprite.spritecollide(player.sprite, bad_lasers, True):
        current_lives -= 1
    if current_lives < 0: current_lives = 0

    health_image = pygame.surface.Surface((int(current_lives)*30, 30))
    pygame.draw.rect(health_image, '#F08811', health_image.get_rect())
    screen.blit(health_image, health_image.get_rect(topleft = (80,50)))

    health_bar_outline = pygame.surface.Surface((lives*30, 30), pygame.SRCALPHA)
    pygame.draw.rect(health_bar_outline, 'grey', health_bar_outline.get_rect(), 5)
    screen.blit(health_bar_outline, health_bar_outline.get_rect(topleft = (80,50)))

    health_text = text.render('Health Bar', True, '#F08811')
    health_text_rect = health_text.get_rect(topleft = (160,20))
    screen.blit(health_text, health_text_rect)

    return current_lives

def update_score(current_score):
    collide = pygame.sprite.groupcollide(good_lasers, villians, True, True)
    if collide:
        for moment in collide:
            for place in collide:
                current_score += 1
                collisions.append((place.rect.centerx, place.rect.centery, pygame.time.get_ticks()))
    
    scoreboard = text.render('Score:' + str(current_score), True, "white")
    scoreboard_rect = scoreboard.get_rect(topright = (920,50))
    screen.blit(scoreboard, scoreboard_rect)
    
    return current_score
                

player = pygame.sprite.GroupSingle()
main_character = Spaceship()
player.add(main_character)

good_lasers = pygame.sprite.Group()
bad_lasers = pygame.sprite.Group()

villians = pygame.sprite.Group()

sprites = [player, good_lasers, bad_lasers, villians]
npc = [good_lasers, bad_lasers, villians]

villian_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(villian_spawn, 800)

while True:

    screen.fill("#0D0110")
    for i in stars:
        pygame.draw.circle(screen, "#fbf5b8", (stars[i].xcor, stars[i].ycor), 1)
        stars[i].xcor -= 0.5
        if stars[i].xcor < 0: stars[i].xcor = 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                good_lasers.add(Laser("player", main_character.rect.x + 80, main_character.rect.centery + 40))
                good_lasers.add(Laser("player", main_character.rect.x + 80, main_character.rect.centery - 40))

            if event.key == pygame.K_RETURN and home_screen:
                cut_scene = True
                home_screen = False
                cut_scene_time = pygame.time.get_ticks()
        if event.type == villian_spawn and game_active:
            enemy = Villian(choice([0,1,1,1]))
            villians.add(enemy)
            
    if game_active:
        for sprite in sprites:
            sprite.update()
            sprite.draw(screen)

        lives_remaining = check_player_damage(lives_remaining)
        scoree = update_score(scoree)
        
        for collision in collisions:
            x, y, collision_time = collision
            if pygame.time.get_ticks() - collision_time < 500:
                point_indicator = text.render('+1', True, 'white')
                point_indicator_rect = point_indicator.get_rect(center = (x,y))
                screen.blit(point_indicator, point_indicator_rect)
            else: collisions.remove(collision)
        

        
        if lives_remaining == 0:
            for group in npc:
                group.empty()
            game_active = False
            home_screen = False
            game_over_screen = True
            game_over_time = pygame.time.get_ticks()

            scores.append(scores)
        
    
    elif game_over_screen:
        over = title_font.render('GAME OVER', True, 'red')
        over_rect = over.get_rect(center = (500,250))
        screen.blit(over, over_rect)

        scoreboard = title_font.render('Score: '+ str(scoree), True, 'White')
        scoreboard_rect = scoreboard.get_rect(center = (500, 150))
        screen.blit(scoreboard, scoreboard_rect)

        if pygame.time.get_ticks() - game_over_time > 3000:
            game_over_screen = False
            home_screen = True

    elif cut_scene:

        
        for i in stars:
            stars[i].xcor -= 30
            if stars[i].xcor < 0: stars[i].xcor = 1000

        player.sprite.rect.x += 1
        player.update()
        player.draw(screen)

        if pygame.time.get_ticks() - cut_scene_time > 1200:
            lives_remaining = lives
            score = 0
            cut_scene = False
            game_active = True
            for i in range(300):
                stars[f'{i}'] = Stars(randint(1,999), randint(1,499))
        
    elif home_screen:
        title = title_font.render('Pixel Wars', True, 'White')
        title_rect = title.get_rect(center = (500,250))
        screen.blit(title,title_rect)

        scoreboard = title_font.render('Score: '+ str(scoree), True, 'White')
        scoreboard_rect = scoreboard.get_rect(center = (500, 150))
        screen.blit(scoreboard, scoreboard_rect)

        if scores:
            high_score = title_font.render('High Score: ' + str(max(scores)), True, 'Blue')
        else: 
            high_score = title_font.render('High Score: None', True, 'Blue')
        high_score_rect = high_score.get_rect(center= (500, 350))
        screen.blit(high_score, high_score_rect)

        player.sprite.rect.center = (100,250)
        player.draw(screen)
        
    pygame.display.update()
    clock.tick(60)