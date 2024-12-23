x = 2500
y = 200
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

from pygame import *

#create game window
window_width = 700
window_height = 500
window = display.set_mode( (window_width, window_height) )
display.set_caption( "My First Game" )

bg = transform.scale( image.load("background.jpg"), (window_width, window_height))

class Character():
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed):
        self.filename = filename
        self.img = transform.scale( image.load(filename), (size_x, size_y))
        self.size_x = size_x
        self.size_y = size_y
        self.speed = speed
        self.rect = self.img.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
    def draw(self):
        # draw.rect(window, (255, 0, 0), self.rect )
        window.blit(self.img, (self.rect.x, self.rect.y))
class Enemy(Character):
    def __init__(self, filename, size_x, size_y, pos_x, pos_y, speed, route_list):
        self.route_list = route_list
        self.route_id = 0
        self.ok_x = False
        self.ok_y = False
        super().__init__(filename, size_x, size_y, pos_x, pos_y, speed)
    def move(self):
        # Movement pattern
        target_x, target_y = self.route_list[self.route_id]
        distance_x = abs(target_x-self.rect.x)
        if (self.rect.x < target_x):
            self.rect.x += min(self.speed, distance_x)
        elif (self.rect.x > target_x):
            self.rect.x -= min(self.speed, distance_x)
        else:
            self.ok_x = True
        distance_y = abs(target_y-self.rect.y)
        if (self.rect.y < target_y):
            self.rect.y+=min(self.speed, distance_y)
        elif (self.rect.y > target_y):
            self.rect.y-=min(self.speed, distance_y)
        else:
            self.ok_y = True
        
        if self.ok_x and self.ok_y:
            self.route_id += 1
            if self.route_id == len(self.route_list):
                self.route_id=0
            self.ok_x = False
            self.ok_y = False

class Wall(Enemy):
    def __init__(self, size_x, size_y, pos_x, pos_y):
        self.size_x = size_x
        self.size_y = size_y
        self.img = Surface( (size_x, size_y) )
        self.R = 222
        self.G = 101
        self.B = 53
        self.img.fill( (self.R, self.G, self.B) )
        self.rect = self.img.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.route_list = [(pos_x, pos_y), (pos_x, pos_y+10)]
        self.route_id = 0
        self.ok_x = False
        self.ok_y = False
        self.speed = 1

wall_list = []
y = 0
for i in range(10):
    wall_list.append( Wall(10, 10, 250, y) )
    y+=55

y = 0
for i in range(5):
    wall_list.append( Wall(10, 10, 350, y) )
    y+=100

y = 0
for i in range(7):
    wall_list.append( Wall(10, 10, 450, y) )
    y+=80

hero = Character("ironman.png", 50, 50, 50, 50, 5)
hero.hp = 5

enemy_list = []
route = [(100, 100), (100, 400)]
enemy_list.append( Enemy("hero.png", 50, 50, 100, 100, 3, route) )
route = [(280, 400), (280, 50)]
enemy_list.append( Enemy("hero.png", 50, 50, 280, 400, 5, route) )
route = [(380, 400), (380, 50)]
enemy_list.append( Enemy("hero.png", 50, 50, 380, 400, 2, route) )
route = [(50, 200), (600, 200)]
enemy_list.append( Enemy("hero.png", 50, 50, 200, 200, 7, route) )
target = Character("treasure.png", 50, 50, 500, 400, 5)

# next time
# create walls and add some features (movement and collision)

font.init()
style = font.SysFont(None, 50)
mixer.init()
mixer.music.load("jungles.ogg")
# mixer.music.play()

clock = time.Clock()
fps = 60
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    clock.tick(fps)
    display.update()
    window.blit(bg, (0,0))
    hero.draw()
    for enemy in enemy_list:
        enemy.draw()
        enemy.move()
    target.draw()
    for wall in wall_list:
        wall.move()
        wall.draw()
    hp_box = style.render( str(hero.hp) , True, (219, 22, 68))
    window.blit(hp_box, (200, 300))

    if finish == False:
        # Collision
        for enemy in enemy_list:
            isCollide = sprite.collide_rect(hero, enemy)
            if (isCollide):
                print("You lose")
                effect = mixer.Sound("kick.ogg")
                effect.play()
                hero.hp -= 1
                hero.rect.x = 50
                hero.rect.y = 50
                
        for wall in wall_list:
            isCollide = sprite.collide_rect(hero, wall)
            if (isCollide):
                print("You hit the wall")
                effect = mixer.Sound("kick.ogg")
                effect.play()
                
        if hero.hp <= 0:
            isWin = False
            finish = True
        # Movement by key pressing
        keys = key.get_pressed()
        if (keys[K_w] and hero.rect.y > 0):
            hero.rect.y -= hero.speed
        if (keys[K_s]):
            hero.rect.y += hero.speed
        if (keys[K_d]):
            hero.rect.x += hero.speed
        # if (keys[K_DOWN] and sprite1.pos_y < window_height - sprite1.size_y)

        
    else:
        if isWin == False:
            text = style.render("You lose", True, (219, 22, 68))
            window.blit(text, (200, 300))