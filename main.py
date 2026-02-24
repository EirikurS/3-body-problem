import pygame
import time
from world_object import World

pygame.init()

display = pygame.display.set_mode((1200, 650))
target_fps = 60

white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 
black = (0, 0, 0) 
red = (255, 0, 0)
yellow = (0xFF, 0xF4, 0x4F)
grey = (0xEE, 0xEE, 0xEE)

running  = True

prev_time = time.time()

world = World()


def pos_to_display_coord(pos):
    x, y = display.get_size()
    
    x_coord = x/2 + pos[0]
    y_coord = y/2 - pos[1]

    return (x_coord, y_coord)

def display_coord_to_pos(coord):
     x, y = display.get_size()

     posx = -(x/2 - coord[0])
     posy = y/2 - coord[1]

     return [posx, posy]

world.create_mass(10**13, pos=[0, 0], immovable=True)

mouse_pressdown_pos = (0,0)

tracers = True
tracers_pos = {}

timestep = 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressdown_pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_release_pos = pygame.mouse.get_pos()
            xvel = (mouse_release_pos[0] - mouse_pressdown_pos[0]) / 100
            yvel = -(mouse_release_pos[1] - mouse_pressdown_pos[1]) / 100
            world.create_mass(10**10, display_coord_to_pos(mouse_pressdown_pos), [xvel, yvel])
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                timestep += 1
            elif event.key == pygame.K_LEFT:
                if timestep != 0:
                    timestep -= 1
            elif event.key == pygame.K_t:
                if tracers:
                    tracers = False
                    tracers_pos = {}
                else:
                    tracers = True
            elif event.key == pygame.K_BACKSPACE:
                removed_mass = world.masses.pop(-1)
                if removed_mass in tracers_pos:
                    del tracers_pos[removed_mass]
        
    
    world.update_world(timestep)

    display.fill((0, 0, 0))
    if tracers:
        for tracer in tracers_pos:
            if len(tracers_pos[tracer]) > 1000:
                tracers_pos[tracer] = tracers_pos[tracer][len(tracers_pos[tracer]) - 1000:]
            for i in range(len(tracers_pos[tracer])-1):
                pygame.draw.line(display, grey, tracers_pos[tracer][i], tracers_pos[tracer][i+1], 1)
    for mass in world.masses:
        coord = pos_to_display_coord(mass.pos)
        if mass.immovable == False:
            pygame.draw.circle(display, white, coord, 5, 0)
            if tracers:
                if mass in tracers_pos:
                    tracers_pos[mass].append(coord)
                else:
                    tracers_pos[mass] = [coord]
        else:
            pygame.draw.circle(display, yellow, coord, 8, 0)
    
    pygame.display.flip()

    pygame.display.update()


    curr_time = time.time()
    diff = curr_time - prev_time
    delay = max(1.0/target_fps - diff, 0)
    time.sleep(delay)
    fps = 1.0/(delay + diff)
    prev_time = curr_time
    pygame.display.set_caption(f"3BodyProblem timestep={timestep}")

pygame.quit()