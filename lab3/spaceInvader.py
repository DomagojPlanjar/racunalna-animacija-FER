import os.path
import random
import shootingGame
import pygame

pygame.font.init()
pygame.mixer.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

GAME_CAPTION = "Space Wars"
WIDTH, HEIGHT = 900, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_CAPTION)

SHIP_WIDTH, SHIP_HEIGHT = 60, 45

# enemies
RED_SPACE_SHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "red-ship.png")), (SHIP_WIDTH, SHIP_HEIGHT)), 180)
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "green-ship.png")), (SHIP_WIDTH, SHIP_HEIGHT))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "blue-ship.png")), (SHIP_WIDTH, SHIP_HEIGHT))

# player
PLAYER_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "arcade-game.png")), (60, 45))

# bullets
BULLET_WIDTH, BULLET_HEIGHT = 25, 30

PLAYER_BULLET = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bullet-player.png")), (BULLET_WIDTH, BULLET_HEIGHT))
ENEMY_BULLET_RED = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bullet-black.png")), (BULLET_WIDTH, BULLET_HEIGHT)), 180)
ENEMY_BULLET_GREEN = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bullet-yellow.png")), (BULLET_WIDTH, BULLET_HEIGHT)), 180)
ENEMY_BULLET_BLUE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bullet-blue.png")), (BULLET_WIDTH, BULLET_HEIGHT)), 180)

# background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.jpg")), (WIDTH, HEIGHT))
MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "menu-space.jpg")), (WIDTH, HEIGHT))

# sounds
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser.wav'))
BACKGROUND_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'backgroundSound.wav'))


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y > height or self.y <= 0

    def collision(self, obj):
        return collide(obj, self)

class Ship:
    COOLDOWN = 30
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def move_bullets(self, vel, obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT): # bullet off-screen
                self.bullets.remove(bullet)
            elif bullet.collision(obj): # bullet-player collision
                obj.health -= 10
                self.bullets.remove(bullet)
            for bullet_player in obj.bullets: # bullet-bullet collision
                if bullet.collision(bullet_player):
                    self.bullets.remove(bullet)
                    obj.bullets.remove(bullet_player)


    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x+self.get_width()//2-BULLET_WIDTH//2, self.y-BULLET_HEIGHT//2, self.bullet_img)
            if not bullet.off_screen(HEIGHT):
                BULLET_FIRE_SOUND.play()
            self.bullets.append(bullet)
            self.cool_down_counter = 1

        

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACE_SHIP
        self.bullet_img = PLAYER_BULLET
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_bullets(self, vel, objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        BULLET_HIT_SOUND.play()
                        objs.remove(obj)
                        self.bullets.remove(bullet)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)


    def health_bar(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y+self.ship_img.get_height()+10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, GREEN,
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()*(self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, ENEMY_BULLET_RED),
                "green": (GREEN_SPACE_SHIP, ENEMY_BULLET_GREEN),
                "blue": (BLUE_SPACE_SHIP, ENEMY_BULLET_BLUE)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x+self.get_width()//2-BULLET_WIDTH//2, self.y+self.get_height()//2 + 20, self.laser_img)
            self.bullets.append(bullet)
            if not bullet.off_screen(HEIGHT):
                BULLET_FIRE_SOUND.play()
            self.cool_down_counter = 1

def collide(obj_one, obj_two):
    offset_x = obj_two.x - obj_one.x
    offset_y = obj_two.y - obj_one.y
    return obj_one.mask.overlap(obj_two.mask, (offset_x, offset_y)) != None

def main():
    running = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 7

    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    BACKGROUND_SOUND.play(-1)

    # draw scene
    def redraw_window():
        WINDOW.blit(BACKGROUND, (0, 0))
        # draw text
        lives_label = main_font.render(f"Life count: {lives}", 1, WHITE)
        level_label = main_font.render(f"Level: {level}", 1, WHITE)

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH-level_label.get_width()-10, 10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)


        if lost:
            lost_label = lost_font.render("You lost!", 1, WHITE)
            WINDOW.blit(lost_label, (WIDTH//2 - lost_label.get_width()//2, 350))


        pygame.display.update()

    while running:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 4:
                running = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.init()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 20 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_bullets(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            # check if enemies are below player level, if so then remove that enemy
            if collide(enemy, player):
                BULLET_HIT_SOUND.play()
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_bullets(-laser_vel, enemies)


def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)

    running = True
    while running:
        WINDOW.blit(MENU_BACKGROUND, (0, 0))
        title_label_first = title_font.render("single-player", 1, WHITE)
        title_width_first = title_label_first.get_width()
        title_height_first = title_label_first.get_height()
        title_first_x = WIDTH//2-title_width_first//2
        title_first_y = 350-title_height_first
        WINDOW.blit(title_label_first, (title_first_x, title_first_y))


        title_label_second = title_font.render("multi-player", 1, WHITE)
        title_width_second = title_label_second.get_width()
        title_height_second = title_label_second.get_height()
        title_second_x = WIDTH // 2 - title_width_second // 2
        title_second_y = 350 + title_height_second

        WINDOW.blit(title_label_second, (title_second_x, title_second_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if (mouse[0] >= title_first_x and mouse[0] <= title_first_x + title_width_first) and (mouse[1] >= title_first_y and mouse[1] <= title_first_y + title_height_first):
                    main()
                elif (mouse[0] >= title_second_x and mouse[0] <= title_second_x + title_width_second) and (mouse[1] >= title_second_y and mouse[1] <= title_second_y + title_height_second):
                    shootingGame.main()


    pygame.quit()

main_menu()