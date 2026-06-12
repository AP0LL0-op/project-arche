# Pygame/Pymunk spike physics Project Arche Efference PoC
import pygame
import pymunk
import pymunk.pygame_util

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
running = True

# pymunk setup
world = pymunk.Space()
world.gravity = (0, 900)
dt = 1/60
elapsed = 0

# shapes
draw_options = pymunk.pygame_util.DrawOptions(screen)

box_mass = 1
box_moment = pymunk.moment_for_box(box_mass, (50, 50))
box_body = pymunk.Body(box_mass, box_moment)
box_body.position =(450,100)
box_shape = pymunk.Poly.create_box(box_body, (50, 50))
box_shape.color = (255, 0, 0, 255)

arm_anchor = world.static_body
arm_anchor.position = (300, 300)
arm_anchor_shape = pymunk.Circle(arm_anchor, radius=10)
arm_anchor_shape.sensor = True

wall = pymunk.Body(body_type=pymunk.Body.STATIC)
wall_segment = pymunk.Segment(body=wall, a=(200,100), b=(200,500), radius=5)

arm_mass = 1
arm_moment = pymunk.moment_for_box(arm_mass, (200,20))
arm_body = pymunk.Body(arm_mass, arm_moment)
arm_shape = pymunk.Poly.create_box(arm_body,  (200, 20))
arm_body.position = (400,300)
arm_joint = pymunk.PivotJoint(arm_anchor, arm_body, (300, 300))

# arm2_mass = 1
# arm2_moment = pymunk.moment_for_box(arm2_mass, (100, 20))
# arm2_body = pymunk.Body(arm2_mass, arm2_moment)
# arm2_shape = pymunk.Poly.create_box(arm2_body, (100, 20))
# arm2_body.position = (450,300)
# arm2_joint = pymunk.PivotJoint(arm_body, arm2_body, (400,300))

motor = pymunk.SimpleMotor(arm_anchor, arm_body, rate=2)
motor.max_force = 1000000
# motor2 = pymunk.SimpleMotor(arm_body, arm2_body, rate=0)

# add shapes to world
world.add(box_body, box_shape)
world.add(arm_anchor_shape)
world.add(wall, wall_segment)
world.add(arm_body, arm_shape, arm_joint) 
# world.add(arm2_shape, arm2_body, arm2_joint)
world.add(motor)

# render loop
while running: 
    # poll for events
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False
    
    # advance physics/world
    world.step(dt)
   
    # fill screen to wipe last frame
    screen.fill("white")

    # draw shapes
    world.debug_draw(draw_options)

    # push to monitor
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    # independent physics
    dt = clock.tick(60) / 1000
    
    # oscillate the arm motor
    elapsed += dt
    if elapsed > 4:
        motor.rate = -motor.rate
        elapsed = 0

# quit
pygame.quit()