import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

wall1_x = 480
wall1_y = 100
wall2_x = 780
wall2_y = 100
wall_width = 1  # Initial wall width
init_pos = pygame.Vector2((wall1_x + wall2_x) // 2, (wall1_y + wall2_y) // 2 + 200)
ball_speed = 130
dt = 0
collision_count = 0

collision_sound = pygame.mixer.Sound('Funny-game-hit-sound-effect.wav')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
   
    
    pygame.draw.rect(screen, "grey", pygame.Rect(wall1_x, wall1_y, wall_width, 720))
    pygame.draw.rect(screen, "grey", pygame.Rect(wall2_x, wall2_y, wall_width, 720))
    font = pygame.font.Font(None, 36)

    init_pos.x += ball_speed * dt
    pygame.draw.circle(screen, "red", (int(init_pos.x), int(init_pos.y)), 20)

    if init_pos.x - 22 <= wall1_x or init_pos.x + 22 >= wall2_x:
        ball_speed = -ball_speed
        if init_pos.x < 640 :
            init_pos.x+=3
        if init_pos.x > 640 :
            init_pos.x-=3
        collision_sound.play()
        collision_count +=1
        collision_occur = False

        if wall2_x - wall1_x < 30:
            break
            
        if not collision_occur:
            wall1_x += 2  # Move the left wall
            wall2_x -= 2  # Move the right wall
            collision_occur = True

        

    text = font.render("Collision : " + str(collision_count), True, (85, 255, 85) )
    screen.blit(text, (80,300))
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
