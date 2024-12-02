import pygame # module pour l'affichage
from random import randint, random
from boid import Boid

class BoidManager: # class gérant tous les boids 
	def __init__(self, boid_count, screen_size, screen):
		self.screen = screen
		self.screen_size = screen_size
		self.boids = [Boid([randint(0, screen_size[0]), randint(0, screen_size[1])], i) for i in range(boid_count)]
		# list des boids, créer avec une position aléatoire et une id
	
	def _get_other_boid_pos(self): # function to get boids position and velocity
		pos_vel = []
		for boid in self.boids:
			pos_vel.append((boid.pos, boid.velocity)) 
		return pos_vel

	def update(self): # function to update boid and display them in the window
		boid_pos = self._get_other_boid_pos()
		for boid in self.boids:
			boid.update(boid_pos, self.screen_size) # update the boid with all the positions of the boids
			
			self.screen.blit(boid.gfx, [boid.pos.x - (boid.width//2), boid.pos.y - (boid.height//2)])
			# add the boid graphics on the screen 
			
class App:
	def __init__(self, boid_count) -> None:         
		self.width = 800
		self.height = 400
		self.screen_size = [self.width, self.height]

		self.clock = pygame.time.Clock()
		self.fps = 60

		self.bg = [0,0,0] # background represented as a list (for RGB)
		self.win = pygame.display.set_mode(self.screen_size) # create a Surface object that will be rendered on the window

		self.boid_count = boid_count
		self.boid_manager = BoidManager(self.boid_count, self.screen_size, self.win)


		self.run = True
		self.mainloop()
		
		
	def mainloop(self):
		
		while self.run: # gameloop
			self.clock.tick(self.fps) # set the frame rate of the game
			
			self.win.fill(self.bg) # reset the window display
			
			self.boid_manager.update() 
						
			for event in pygame.event.get(): # event loop
				if event.type == pygame.QUIT: # detect if you close the window
					self.run = False
					
			pygame.display.update() # update all the diplay changes
			
		self.close_app()
		
	def close_app(self):
		pygame.quit()

if __name__ == '__main__':
    boid_count = 25 # Can be changed
    app = App(boid_count)