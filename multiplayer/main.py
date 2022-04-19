import pygame
import os

from pygame.event import Event
pygame.font.init()
pygame.mixer.init()

width = 1920  
height = 1000
color = 0, 0, 0
border_color = 91, 128, 189
fps = 60
winner_font = pygame.font.SysFont('comicsans', 100)
font_color = 255, 255, 255
health = pygame.font.SysFont('comicsans', 50)
sound = pygame.mixer.Sound('multiplayer/gun.mp3')
end_sound = pygame.mixer.Sound('multiplayer/anthem.mp3')
background = pygame.transform.scale(pygame.image.load(os.path.join ('multiplayer/death.png')), (width, height))
border = pygame.Rect(width//2 - 5, 0, 0, height)
game = pygame.display.set_mode((width, height)) #pygame.FULLSCREEN(optional)
pygame.display.set_caption("Multiplayer")

ship_width = 80
ship_height = 50
ship_1 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join
    ('multiplayer/starwars.png')), (ship_width, ship_height)), 90)
ship_2 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join
    ('multiplayer/ship_2.png')), (100, 70)), -90 )
shifting = 7

my_ship_hit = pygame.USEREVENT + 2
enemy_ship_hit = pygame.USEREVENT + 1

bullet_color = 255, 0, 0
bullet_color_2 = 38, 255, 0
max_bullets = 5                              
bullet_shifting = 20

def window(my_ship, enemy_ship, my_bullets, enemy_bullets, my_ship_health, enemy_ship_health):
    """Wyświetlanie na ekranie"""
    game.blit(background, (0, 0))
    pygame.draw.rect(game, border_color, border)

    enemy_ship_health_text = health.render("Punkty życia: " + str(enemy_ship_health), 1, font_color)
    game.blit(enemy_ship_health_text, (1575,0))

    my_ship_health_text = health.render("Punkty życia: " + str(my_ship_health), 1, font_color)
    game.blit(my_ship_health_text, (0, 0))

    game.blit(ship_1, (my_ship.x, my_ship.y))
    game.blit(ship_2, (enemy_ship.x, enemy_ship.y))

    for bullet in my_bullets:
        pygame.draw.rect(game, bullet_color, bullet)
    
    for bullet in enemy_bullets:
        pygame.draw.rect(game, bullet_color_2, bullet)

    pygame.display.update()

def my_ship_movement(keys_pressed, my_ship):
    """Poruszanie się statkiem moim"""
    if keys_pressed[pygame.K_a] and my_ship.x - shifting > -5:
        my_ship.x -= shifting
    if keys_pressed[pygame.K_d] and my_ship.x + shifting + (ship_width/2) < border.x:
        my_ship.x += shifting
    if keys_pressed[pygame.K_w] and my_ship.y - shifting > -5:
        my_ship.y -= shifting
    if keys_pressed[pygame.K_s] and my_ship.y + shifting < 1005:
        my_ship.y += shifting

def enemy_ship_movement(keys_pressed, enemy_ship):
    """Poruszanie się statkiem wrogim"""
    if keys_pressed[pygame.K_LEFT] and enemy_ship.x - shifting > border.x:
        enemy_ship.x -= shifting
    if keys_pressed[pygame.K_RIGHT] and enemy_ship.x + shifting < width - 65:
        enemy_ship.x += shifting
    if keys_pressed[pygame.K_UP] and enemy_ship.y - shifting > -26:
        enemy_ship.y -= shifting
    if keys_pressed[pygame.K_DOWN] and enemy_ship.y + shifting < 1006:
        enemy_ship.y += shifting    

def handle_bullets(my_bullets, enemy_bullets, my_ship, enemy_ship):
    """Strzelanie pociskami moimi"""
    for bullet in my_bullets:
        bullet.x += bullet_shifting
        if enemy_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(enemy_ship_hit))
            my_bullets.remove(bullet)
        elif bullet.x > width:
            my_bullets.remove(bullet)

    """Strzelanie pociskami przez wroga"""
    for bullet in enemy_bullets:
        bullet.x -= bullet_shifting
        if my_ship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(my_ship_hit))
            enemy_bullets.remove(bullet)
        elif bullet.x < 0:
            enemy_bullets.remove(bullet) 

def draw_winner(text):

    draw_text = winner_font.render(text, 1, font_color)
    game.blit(draw_text, (width/2 - draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(21000)

def main():
    """Główna funkcja gry"""
    clock = pygame.time.Clock()
    my_ship = pygame.Rect(0 + ship_width, height/2, ship_width, ship_height)
    enemy_ship = pygame.Rect(width - ship_width, height/2, 100, 70)

    my_bullets = []
    enemy_bullets = []

    my_ship_health = 3
    enemy_ship_health = 3

    run_game = True
    while run_game:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run_game = False

                if event.key == pygame.K_SPACE and len(my_bullets) < max_bullets:
                    bullet = pygame.Rect(my_ship.x, my_ship.y + ship_height//2, 15, 5)
                    my_bullets.append(bullet)
                    sound.play()

                if event.key == pygame.K_RSHIFT and len(enemy_bullets) < max_bullets:
                    bullet = pygame.Rect(enemy_ship.x, enemy_ship.y + 35, 15, 5)
                    enemy_bullets.append(bullet)
                    sound.play()
                
                if event.key == pygame.K_r:
                    main()
                

            if event.type == enemy_ship_hit:
                enemy_ship_health -= 1
            if event.type == my_ship_hit:
                my_ship_health -= 1
                                                            
        if enemy_ship_health < 0:
            win = "Wygrał gracz Pierwszy"
            #end_sound.play()
            draw_winner(win)
            break

        if my_ship_health < 0:
            win = "Wygrał gracz drugi"
            #end_sound.play()
            draw_winner(win)
            break
            

        keys_pressed = pygame.key.get_pressed()
        my_ship_movement(keys_pressed, my_ship)
        enemy_ship_movement(keys_pressed, enemy_ship)

        handle_bullets(my_bullets, enemy_bullets, my_ship, enemy_ship)

        window(my_ship, enemy_ship, my_bullets, enemy_bullets, my_ship_health, enemy_ship_health)

    pygame.quit()

if __name__ == "__main__":
    main()    
