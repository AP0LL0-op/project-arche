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

        # the arm anchor
        self.arm_anchor = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.arm_anchor.position = (300, 300)
        arm_anchor_shape = pymunk.Circle(self.arm_anchor, radius=10)
        arm_anchor_shape.sensor = True
        self.space.add(self.arm_anchor, arm_anchor_shape)

        # the arm
        arm_mass = 1
        arm_moment = pymunk.moment_for_box(arm_mass, (250, 20))
        self.arm_body = pymunk.Body(arm_mass, arm_moment)
        self.arm_body.position = (425, 300)
        arm_shape = pymunk.Poly.create_box(self.arm_body, (250, 20))
        arm_shape.elasticity = 1.0
        arm_shape.friction = 0.3
        arm_joint = pymunk.PivotJoint(self.arm_anchor, self.arm_body, (300, 300))
        self.space.add(self.arm_body, arm_shape, arm_joint)

        # the motor
        self.motor = pymunk.SimpleMotor(self.arm_anchor, self.arm_body, rate=0)
        self.motor.max_force = 100000
        self.space.add(self.motor)

        # the arena border
        borders = [
            # top 
            ((0, 0), (600, 0)), 
            # left
            ((0, 0), (0, 600)), 
            # right
            ((600, 0), (600, 600)), 
            # bottom
            ((0, 600), (600, 600))]
        for a, b in borders:
            wall_segment = pymunk.Segment(self.space.static_body, a, b, radius=5)
            wall_segment.elasticity = 1.0
            wall_segment.friction = 0.3
            self.space.add(wall_segment)

        # fixed wall
        fixed_wall_segment = pymunk.Segment(self.space.static_body, a=(200, 200), b=(100, 200), radius=5)
        fixed_wall_segment.elasticity = 1.0
        fixed_wall_segment.friction = 0.3
        self.space.add(fixed_wall_segment)

    # advance the physics by dt seconds
    def step(self, dt):
        self.space.step(dt)

    # SimpleMotor spins body b opposite to rate; flip so positive command = positive rotation
    def apply_motor(self, commands):
        self.motor.rate = -commands

    def read_sensors(self):
        contact_total = 0
        def add_contact(arbiter):
            nonlocal contact_total
            contact_total += arbiter.total_impulse.length
        self.arm_body.each_arbiter(add_contact)
        return {
            "angle": self.arm_body.angle, 
            "angular_velocity": self.arm_body.angular_velocity,
            "contact": contact_total}