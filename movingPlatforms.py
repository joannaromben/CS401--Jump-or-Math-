import pygame
pygame.init() #initialize pygame

win = pygame.display.set_mode((800, 500)) #create the surface

pygame.display.set_caption("Moving platform") #I MAY NOT NEED THIS LINE

x = 200 #object coordinates
y = 200

width = 20 #dimensions of the object
height = 20

velocity = 5 #speed of the movement
direction = 1 #1 for right, -1 for left

run = True # confirms python is running

#****************************************************

while run:
	pygame.time.delay(30) #creates a delay of 10MS (WHYYYY)
	#30 for smooth it says

	for event in pygame.event.get(): #iterate the list of event objects
		if event.type == pygame.QUIT: #if window close event
			run =  False #Exit the loop

	x += velocity * direction # for the platform to move

	if x > 800 - width: #if reaches the boundaries(im assuming it means the edges)
		direction = -1 #change the direction to left
	elif x < 0: #if it reaches the left edge
		direction = 1 #change direction to right
	###################################
	# this is important piece of code #
	#	^^^^^^^^^^^^^^^^^			  #
	###################################

	win.fill((0, 0, 0)) #fill the surface object with black
	#I DONT THINK WE NEED THIS EITHER.

	pygame.draw.rect(win, (255, 192, 203), (x, y, width, height))#drawing 
	#I DONT THINK WE NEED THIS EITHER.

	pygame.display.update() #refreshes the window


pygame.quit() #closes the window






