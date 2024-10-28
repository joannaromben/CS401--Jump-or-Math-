import pygame
pygame.init() #initialize pygame

win = pygame.display.set_mode((800, 500)) #create the surface

pygame.display.set_caption("DISSAPEAR PLATFORM") #I MAY NOT NEED THIS LINE

x = 200 #object coordinates
y = 200

width = 20 #dimensions of the object
height = 20

velocity = 5 #speed of the movement
direction = 1 #1 for right, -1 for left

run = True # confirms python is running
timer = 0 #ADDED A TIMER
# timer that keeps track for random dissapearance
#****************************************************

while run:
	pygame.time.delay(30) 
	#30 for smooth 

	for event in pygame.event.get(): #iterate the list of event objects
		if event.type == pygame.QUIT: #if window close event
			run =  False #Exit the loop

	x += velocity * direction # for the platform to move

	if x > 800 - width: #if reaches the boundaries(im assuming it means the edges)
		direction = -1 #change the direction to left
	elif x < 0: #if it reaches the left edge
		direction = 1 #change direction to right

	timer += 1
	if timer >= 100: #checks every 100 frames(frames???)
		if random.choice([True, False]): #Random decides to dissapear
			#I think we need to change it bc it can be a platfom it hasnt jumped in into
			visible = not visible 
		timer = 0 #reset timer
	###################################
	# this is important piece of code #
	#	^^^^^^^^^^^^^^^^^			  #
	###################################

	win.fill((0, 0, 0)) #fill the surface object with black
	#I DONT THINK WE NEED THIS EITHER.
	if visible:
		pygame.draw.rect(win, (255, 192, 203), (x, y, width, height))#drawing 
	#I DONT THINK WE NEED THIS EITHER.

	pygame.display.update() #refreshes the window


pygame.quit() #closes the window






