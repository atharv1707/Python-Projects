import math
import multiprocessing
import time
from tkinter import font
import pygame
import pymunk
import pymunk.pygame_util
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

pygame.init()

WIDTH, HEIGHT = 900, 800
velocity_data = []
window = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 36)


def draw(window, space, draw_options, line, force_text, velocity_text):
    window.fill("white")
    space.debug_draw(draw_options)
    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)
    if force_text:
        window.blit(force_text, (50,50))
    if velocity_text:
        window.blit(velocity_text, (50, 100))
    # if coord:
    #     window.blit(coord, (150, 100))
    space.debug_draw(draw_options)
    pygame.display.update()


def update_graph(frame):

    global ball
    

    # Update the velocity data
    if ball:
        velocity = math.sqrt(ball.body.velocity.x ** 2 + ball.body.velocity.y ** 2)
        velocity_data.append(velocity) 

    plt.clf()
    plt.plot(velocity_data, label = 'Velocity')
    plt.xlabel("Frame")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.draw()
    plt.pause(0.01)

def calculate_dist(p1,p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

def calculate_angle(p1,p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def create_boundary(space, width, height):
    rects = [
        [(width/2, height-10), (width, 20)], [(width/2, 10), (width, 20)], [(10, height/2), (20, height)], [(width-10, height/2), (20,height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.5
        shape.friction = 0.5
        space.add(body, shape)

# def create_structure():
    

def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100)
    shape.elasticity = 0.95
    shape.friction = 0.5
    space.add(body, shape)
    return shape

def run_mat():
    fig = plt.figure()
    ani = FuncAnimation(fig, update_graph, frames=100, repeat = False)
    plt.show()

def run(window, width, height):
    global velocity_data,ball
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    space = pymunk.Space()
    space.gravity = (0, 981)

    create_boundary(space, width, height)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    

    pressed_pos = None
    ball = None
    force = 0

    while run:
        line = None
        
        if ball and pressed_pos:
            line = [ pygame.mouse.get_pos(), pressed_pos]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                elif pressed_pos and line:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force  =  calculate_dist(*line) *50 #this is force built up
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force

                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0)) #this is force applied
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None
                    force = 0

        velocity = 0.0
        if ball:
           velocity = math.sqrt(ball.body.velocity.x ** 2 + ball.body.velocity.y ** 2)
           velocity_data.append(velocity) #append velocity of each time into the dataframe we have ,which will give it to update graph.


 
        force_text = font.render(f'Force: {(force/100):.2f} N', True, (0,0,0))
        velocity_text = font.render(f'Velocity: {velocity:.2f} m/s', True, (0, 0, 0))
        # coord = font.render(f'Coordinates: ({ball.body.position.x:.2f}, {ball.body.position.y:.2f})', True, (0, 0, 0))

        draw(window, space, draw_options, line, force_text ,velocity_text)
        space.step(dt)
        clock.tick(fps)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':

    matplotlib_process = multiprocessing.Process(target=run_mat)
    matplotlib_process.start()

    run(window, WIDTH, HEIGHT)
