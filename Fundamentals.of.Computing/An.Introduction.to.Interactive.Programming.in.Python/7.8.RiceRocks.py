# http://www.codeskulptor.org/

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
angle_vel = 0.05
forward_thrust = 0.1
friction = 0.99
missile_speed = 6
num_rocks = 12
rock_spawn_buffer = 50
draw_missile = False
started = False

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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

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
        self.set_thrust(False)
        self.angle = angle
        self.angle_vel = 0.0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self, canvas):
        if (self.thrust == False):
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            image_thrust = (self.image_center[0] + self.image_size[0], self.image_center[1])
            canvas.draw_image(self.image, image_thrust, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        # Update angle
        self.angle += self.angle_vel
        
        # Update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
        # Update thrust
        forward = angle_to_vector(self.angle)
        if (self.thrust == True):
            self.vel[0] += forward[0] * forward_thrust
            self.vel[1] += forward[1] * forward_thrust
        
        # Update friction
        self.vel[0] *= friction
        self.vel[1] *= friction
        
    def update_angle_vel(self, angle_vel):
        self.angle_vel += angle_vel
        
    def set_thrust(self, thrust):
        self.thrust = thrust
        if (thrust == True):
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
        
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def shoot(self):
        global missile_group
        
        forward = angle_to_vector(self.angle)
        pos = [self.pos[0] + (forward[0] * self.radius), self.pos[1] + (forward[1] * self.radius)]
        vel = [self.vel[0] + missile_speed * forward[0],
               self.vel[1] + missile_speed * forward[1]]
        missile = Sprite(pos,
                         vel,
                         self.angle,
                         0,
                         missile_image,
                         missile_info,
                         missile_sound)
        missile_group.add(missile)

    
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
        if self.animated:
            center = [self.image_center[0] + (self.age * self.image_size[0]), self.image_center[1]]
            canvas.draw_image(self.image,
                              center,
                              self.image_size,
                              self.pos,
                              self.image_size,
                              self.angle)
        else:
            canvas.draw_image(self.image,
                              self.image_center,
                              self.image_size,
                              self.pos,
                              self.image_size,
                              self.angle)
    
    def update(self):
        # Update angle
        self.angle = self.angle + self.angle_vel
        
        # Update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Update age
        self.age += 1
        if (self.age > self.lifespan):
            return True
        else:
            return False

    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        if (dist(self.pos, other_object.get_pos()) <= (self.radius + other_object.get_radius())):
            return True
        else:
            return False
        
def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # Process collisions
    score += group_group_collide(missile_group, rock_group)
    if group_collide(rock_group, my_ship):
        lives -= 1
        
    # draw ship and sprites
    my_ship.update()
    my_ship.draw(canvas)
    if started:
        process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    # Check game end
    if (lives <= 0):
        setup_game()
        
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    

def keydown(key):
    global my_ship, started
    
    if started:
        if key == simplegui.KEY_MAP["left"]:
            my_ship.update_angle_vel(-angle_vel)
        elif key == simplegui.KEY_MAP["right"]:
            my_ship.update_angle_vel(angle_vel)
        elif key == simplegui.KEY_MAP["up"]:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP["space"]:
            my_ship.shoot()
        elif key == simplegui.KEY_MAP["s"]:
            soundtrack.play()
        elif key == simplegui.KEY_MAP["q"]:
            soundtrack.pause()
            soundtrack.rewind()
   
        
def keyup(key):
    global my_ship
    
    if started:
        if key == simplegui.KEY_MAP["left"]:
            my_ship.update_angle_vel(angle_vel)
        elif key == simplegui.KEY_MAP["right"]:
            my_ship.update_angle_vel(-angle_vel)
        elif key == simplegui.KEY_MAP["up"]:
            my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        score = 0
        lives = 3
        soundtrack.play()
       
        
# timer handler that spawns a rock    
def rock_spawner():
    global started, rock_group, my_ship, rock_spawn_buffer, score

    if (len(rock_group) < num_rocks) and started:
        pos = [random.randrange(WIDTH), random.randrange(HEIGHT)]
        vel = [(random.random() + (random.random() * score / 10.0)) * random.choice([-1, 1]),
               (random.random() + (random.random() * score / 10.0)) * random.choice([-1, 1])]
        rock = Sprite(pos,
                      vel,
                      0,
                      (random.random() / 10.0) * random.choice([-1, 1]),
                      asteroid_image,
                      asteroid_info)

        if (dist(rock.pos, my_ship.get_pos()) > (rock.radius + my_ship.get_radius() + rock_spawn_buffer)):
            rock_group.add(rock)

        
# timer handler that speeds up the rocks    
def rock_speed_incrementer():
    global rock_group, rock_speed_multiplier, rock_speed_increment
    
    rock_speed_multiplier += rock_speed_increment
    
    
# Process a sprite group
def process_sprite_group(canvas, group):
    remove_group = set()
    for sprite in group:
        if sprite.update():
            remove_group.add(sprite)
        else:
            sprite.draw(canvas)
    group.difference_update(remove_group)
        
# Check for a collision for all sprites in a group with an object
def group_collide(group, other_object):
    global explosion_group
    
    result = False
    remove_group = set()
    for g in group:
        if (g.collide(other_object)):
            explosion = Sprite(g.get_pos(),
                               [0, 0],
                               0,
                               0,
                               explosion_image,
                               explosion_info,
                               explosion_sound)
            explosion_group.add(explosion)
            remove_group.add(g)
            result = True
    group.difference_update(remove_group)
    return result
        
# Check for collisions between two groups
def group_group_collide(group_one, group_two):
    result = 0
    remove_group = set()
    for g in group_one:
        if (group_collide(group_two, g)):
            remove_group.add(g)
            result += 1
    group_one.difference_update(remove_group)
    return result

# Start or reset the game
def setup_game():
    global started, my_ship, rock_group, missile_group, explosion_group
    
    started = False
    soundtrack.pause()
    soundtrack.rewind()
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    
    # initialize ship and two sprites
    rock_group = set()
    missile_group = set()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# Setup the game
explosion_group = set()
setup_game()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
