import pymunk

class World:
    def __init__(self):
        self.space = pymunk.Space()

        # gravity is zero to simulate a top down simulation, rather than risk motion dying
        self.space.gravity = (0, 0)

        # the ball - the object that moves
        ball_mass = 1
        ball_moment = pymunk.moment_for_circle(ball_mass, inner_radius=0, outer_radius=30)
        self.ball_body = pymunk.Body(ball_mass, ball_moment)
        self.ball_body.position = (450, 200)
        ball_shape = pymunk.Circle(body=self.ball_body, radius=30)
        ball_shape.elasticity = 0.9
        ball_shape.friction = 0.3
        ball_shape.color = (255, 0, 0, 255)
        self.space.add(self.ball_body, ball_shape)