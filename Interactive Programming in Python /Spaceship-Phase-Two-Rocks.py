# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2013.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [135, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos = [(self.pos[0] + self.vel[0]) % WIDTH, (self.pos[1] + self.vel[1]) % HEIGHT]

        # calculate forward
        forward =  angle_to_vector(self.angle)

        # apply thrust
        if self.thrust:
            self.vel[0] += forward[0] * 0.9
            self.vel[1] += forward[1] * 0.9

        # friction update
        self.vel[0] *= 0.94
        self.vel[1] *= 0.94

    def tip_position(self):
        return [self.radius * math.cos(self.angle), self.radius * math.sin(self.angle)]

    def shoot(self):
        global a_missile
        direction = angle_to_vector(self.angle)
        tip = self.tip_position()
        missile_pos = [self.pos[0] + tip[0], self.pos[1] + tip[1]]
        missile_vel = [self.vel[0] + direction[0] * 3, self.vel[1] + direction[1] * 3]
        a_missile = Sprite(missile_pos, missile_vel, 0, 0, missile_image, missile_info, missile_sound)
            
    def toggle_thrust(self, active):
        self.thrust = active
        
    def rotate_left(self):
        if self.angle_vel == 0 or self.angle_vel > 0:
            self.angle_vel = -0.05
    def rotate_right(self):
        if self.angle_vel == 0 or self.angle_vel < 0:
            self.angle_vel = 0.04
    def rotate_stop(self):
        self.angle_vel = 0

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        self.angle += self.angle_vel

        # calculate forward
        pos_angle =  angle_to_vector(self.angle)
        
        #update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        pass        

           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    # draw live and scores
    canvas.draw_text('Lives', (30, 50), 25, 'White')
    canvas.draw_text(str(lives), (30, 75), 25, 'White')
    canvas.draw_text('Score', [WIDTH-100, 50], 25, 'White')
    canvas.draw_text(str(score), [WIDTH-100, 75], 25, 'White')
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    radius = asteroid_info.get_radius()
    # random position
    pos = [random.randrange(0, WIDTH - radius), random.randrange(0, HEIGHT - radius)]
    # random velocity
    vel_x = 2 + 2 * random.random()
    vel_y = 2 * (random.random() - 0.5) 
    if random.randrange(0, 2) == 1:
        vel_x = - vel_x
    vel = [vel_x, vel_y]
    # random angle
    angle_lower = -0.15
    angle_upper = 0.15
    angle_range_width = angle_upper - angle_lower
    angle = random.random() * angle_range_width + angle_lower
    a_rock = Sprite(pos, vel, 0, angle, asteroid_image, asteroid_info)


def keydown_handler(key):
    if simplegui.KEY_MAP['left'] == key:
        my_ship.rotate_left()
    if simplegui.KEY_MAP['right'] == key:
        my_ship.rotate_right()
    if simplegui.KEY_MAP['up'] == key:
        my_ship.toggle_thrust(True)
        ship_thrust_sound.play()
    if simplegui.KEY_MAP['space'] == key:
        my_ship.shoot()
        
def keyup_handler(key):
    if simplegui.KEY_MAP['left'] == key or simplegui.KEY_MAP['right'] == key:
        my_ship.rotate_stop()
    if simplegui.KEY_MAP['up'] == key:
        my_ship.toggle_thrust(False)
        ship_thrust_sound.rewind()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 2, HEIGHT / 2], [1, 1], 0, 0.1, asteroid_image, asteroid_info)
a_missile = Sprite([0, 0], [0,0], 0, 0, missile_image, missile_info, None)

# register handlers
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
