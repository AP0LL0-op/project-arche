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
world.gravity = (0, 0)
dt = 1/60
elapsed = 0

# print the current arbiter contact value
def print_contact(arbiter):
    print(arbiter.total_impulse.length)

# shapes
draw_options = pymunk.pygame_util.DrawOptions(screen)

ball_mass = 1
ball_moment = pymunk.moment_for_circle(ball_mass, inner_radius=0, outer_radius=30)
ball_body = pymunk.Body(ball_mass, ball_moment)
ball_body.position = (450, 200)
ball_shape = pymunk.Circle(body=ball_body, radius=30)
ball_shape.elasticity = 0.9
ball_shape.friction = 0.3
ball_shape.color = (255, 0, 0, 255)

# box_mass = 1
# box_moment = pymunk.moment_for_box(box_mass, (50, 50))
# box_body = pymunk.Body(box_mass, box_moment)
# box_body.position =(450,100)
# box_shape = pymunk.Poly.create_box(box_body, (50, 50))
# box_shape.color = (255, 0, 0, 255)

arm_anchor = pymunk.Body(body_type=pymunk.Body.STATIC)
arm_anchor.position = (300, 300)
arm_anchor_shape = pymunk.Circle(arm_anchor, radius=10)
arm_anchor_shape.sensor = True

wall = pymunk.Body(body_type=pymunk.Body.STATIC)
wall_segment = pymunk.Segment(body=wall, a=(200,200), b=(100,200), radius=5)
wall_segment.elasticity = 1.0
wall_segment.friction = 0.3

wall_top = world.static_body
wall_segment_top = pymunk.Segment(body=wall_top, a=(0,0), b=(600,0), radius=5)
wall_segment_top.elasticity = 1.0
wall_segment_top.friction = 0.3

wall_left = world.static_body
wall_segment_left = pymunk.Segment(body=wall_left, a=(0,0), b=(0,600), radius=5)
wall_segment_left.elasticity = 1.0
wall_segment_left.friction = 0.3

wall_right = world.static_body
wall_segment_right = pymunk.Segment(body=wall_right, a=(600,0), b=(600,600), radius=5)
wall_segment_right.elasticity = 1.0
wall_segment_right.friction = 0.3

wall_bottom = world.static_body
wall_segment_bottom = pymunk.Segment(body=wall_bottom, a=(0,600), b=(600,600), radius=5)
wall_segment_bottom.elasticity = 1.0
wall_segment_bottom.friction = 0.3

arm_mass = 1
arm_moment = pymunk.moment_for_box(arm_mass, (250,20))
arm_body = pymunk.Body(arm_mass, arm_moment)
arm_shape = pymunk.Poly.create_box(arm_body,  (250, 20))
arm_body.position = (425,300)
arm_joint = pymunk.PivotJoint(arm_anchor, arm_body, (300, 300))
arm_shape.elasticity = 1.0
arm_shape.friction = 0.3

# arm2_mass = 1
# arm2_moment = pymunk.moment_for_box(arm2_mass, (100, 20))
# arm2_body = pymunk.Body(arm2_mass, arm2_moment)
# arm2_shape = pymunk.Poly.create_box(arm2_body, (100, 20))
# arm2_body.position = (450,300)
# arm2_joint = pymunk.PivotJoint(arm_body, arm2_body, (400,300))

motor = pymunk.SimpleMotor(arm_anchor, arm_body, rate=2)
motor.max_force = 100000

# add shapes to world
# world.add(box_body, box_shape)
world.add(ball_body, ball_shape)
world.add(arm_anchor, arm_anchor_shape)
world.add(wall, wall_segment)
world.add(wall_segment_top)
world.add(wall_segment_left)
world.add(wall_segment_right)
world.add(wall_segment_bottom)
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

    # # limits FPS to 60
    # # dt is delta time in seconds since last frame, used for framerate
    # # independent physics
    # dt = clock.tick(60) / 1000
    
    # oscillate the arm motor
    elapsed += dt
    if elapsed > 4:
        motor.rate = -motor.rate
        elapsed = 0    

    # call print_contact function with each_arbiter
    arm_body.each_arbiter(print_contact)

# quit
pygame.quit()