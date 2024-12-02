import pygame
from utilities import Vec2, is_in_sector
from math import atan2, degrees

class Boid:
    def __init__(self, pos, boid_id):
        self.pos = Vec2(*pos) # create a 2D vector to represente the position
        
        self.GFX = pygame.image.load("assets/boid.png").convert_alpha() # load the base asset of the boid
        self.gfx = self.GFX # the displayed asset with the boid rotation

        self.id = boid_id
        self.speed = 3 # the speed of the boid
        
        self.width = self.GFX.get_width()
        self.height = self.GFX.get_height() 
        
        self.MAX_STEARING = 0.3 # the max lenght of a stearing force
        
        self.velocity = Vec2().random_vector().normalized() * self.speed # set a random velocity
        
        self.min_range = 16 # circle around the boids where other boids shouldn't be 
        self.max_range = 40 # max_range where two boids consider each other
        self.field_of_view = 115 
        
        self.target = Vec2(400, 200) # target base position

    def update(self, boids, screen_size):
        self._check_others(boids) # function to apply the rules
        
        mouse_pos = pygame.mouse.get_pos() # get the mouse cursor 
        self.target = Vec2(mouse_pos[0], mouse_pos[1]) # set the mouse cursor as a target 
        
        self._find_target()
        
        self.velocity = self.velocity.set_magnitude(self.speed) # set the length of the velocity vector to 3
        
        self._check_borders(screen_size) # set the position of the boid other side the screen if they go outside

        self._apply_movement()

    def _check_others(self, boids):
        POS_INDEX = 0 
        VEl_INDEX = 1
        ANGLE_INDEX = 1
        
        fleeing_force = Vec2() 
        avg_angle = self.velocity
        center_force = Vec2()
        
        for boid in boids: # loop through all the boids position and velocity to calculate each force 
            min_angle = self.velocity.to_polar()[ANGLE_INDEX] - self.field_of_view
            max_angle = self.velocity.to_polar()[ANGLE_INDEX] + self.field_of_view
            
            if is_in_sector(boid[POS_INDEX], min_angle, max_angle, self.pos, self.max_range): # check if the position of the current boid is not the one who check and is in the field of view
                fleeing_force += self._calculate_fleeing_force(boid[POS_INDEX])
                avg_angle += boid[VEl_INDEX]
                center_force += (boid[POS_INDEX] - self.pos)//2

        force = fleeing_force.set_magnitude(0.8) + center_force.set_magnitude(0.7) + avg_angle.set_magnitude(0.5)
        
        noise = Vec2().random_vector().set_magnitude(0.05)
        
        force += noise      
        
        force = force.clamp_norm(self.MAX_STEARING) # clamp the norm lenght (the norm can't be > then 0.3) 
        
        self.velocity += force
    
    def _find_target(self):
        vec_to_target = self.target - self.pos # get the vector from the boid to the target
        vec_to_target = vec_to_target.set_magnitude(0.1) # set the magnetude so it's not too strong
        
        self.velocity += vec_to_target
        
    def _calculate_fleeing_force(self, other_pos):
        force = self.pos - other_pos # calculate the vector from the other boids to this one
        dist = Vec2.distance(self.pos, other_pos) - (self.min_range * 2) # calculate the distance
        if dist <= 0:  # avoid DivisionByZero error
            dist = 0.001
        
        force *= 1/dist # the force is bigger when the boids are close
        return force
                              
    def _check_borders(self, screen_size): # move the boid to the other side of the screen if the next position is outside of the window
        x_mov = self.pos.x + self.velocity.x
        y_mov = self.pos.y + self.velocity.y
        if  x_mov > screen_size[0]:
            self.pos.x = 0
            
        if  y_mov > screen_size[1]:
            self.pos.y = 0
        
        if  x_mov < 0:
            self.pos.x = screen_size[0]
                        
        if  y_mov < 0:
            self.pos.y = screen_size[1]

    def _apply_movement(self): 
        self.pos += round(self.velocity) # apply the velocity to the position 
        
        angle = degrees(atan2(self.velocity.y, self.velocity.x)) # calculate the angle between the x axis and the velocity vector
        
        self.gfx = pygame.transform.rotate(self.GFX, -angle) # apply a rotation to the displayed graphics