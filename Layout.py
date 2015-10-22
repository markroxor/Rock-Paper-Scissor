import pygame,time,random,cv2,thread,threading
from detectionFunction import fingerCount

pygame.init()
display_width = 1366
display_height = 700

black = (0,0,0)
white = (255,255,255)

light_red = (255,0,0)
red = (200,0,0)

light_green = (0,255,0)
green = (0,200,0)

light_blue = (0,0,255)
blue = (0,0,175)

light_yellow = (255,255,0)
yellow = (200,200,0)

clock = pygame.time.Clock()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Rock Paper Scissor")

# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

backImage = pygame.image.load("img1.png")
paperImage = pygame.image.load("paper1.png")
whitebg = pygame.image.load("white-background.png")

smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",85)

def text_objects(text,color,size="small"):

	if size == "small":
		textSurface = smallfont.render(text,True,color)
	elif size == "medium":
		textSurface = medfont.render(text,True,color)
	elif size == "large":
		textSurface = largefont.render(text,True,color)

	return textSurface,textSurface.get_rect()

def textButton(msg,color,x,y,width,height,size="small"):
	textSurf , textRect = text_objects(msg,color,size)
	textRect.center = ((x+width/2),y+height/2)
	gameDisplay.blit(textSurf,textRect)

def button(text,x,y,width,height,inactive_color,active_color,action=None):
	flag = 1
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x+width > cur[0] > x and y+height> cur[1] > y:
		pygame.draw.rect(gameDisplay,active_color,(x,y,width,height))

		if click[0] and action != None:
			if action == "play":
				flag = 0
				Play()
			elif action == "instructions":
				flag = 0
				Instructions()
			elif action == "about":
				flag = 0
				About()
			elif action == "quit":
				flag = 0
				pygame.quit()
				quit()
	else:
		pygame.draw.rect(gameDisplay,inactive_color,(x,y,width,height))

	textButton(text,black,x,y,width,height)
	return flag

def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def splash_screen():
	gameDisplay.blit(backImage,(0,-35))
	pygame.display.update()
	pygame.time.wait(1500)
	clock.tick(15)

def game_intro():
	intro = True
	flag = 1
	while flag and intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.blit(whitebg,(0,0))
		# gameDisplay.blit(paperImage,(0,0))
		message_to_screen("The classical game of -",black,-125,size="large")
		message_to_screen("ROCK PAPER SCISSORS!",black,-40,size="large")

		intro = button("Play",display_width*0.15,display_height*0.75,100,50,green,light_green,"play")
		intro = button("Instructions",display_width*0.35+5,display_height*0.75,120,50,red,light_red,"instructions")
		intro = button("About",display_width*0.55,display_height*0.75,120,50,blue,light_blue,"about")
		intro = button("Quit",display_width*0.75,display_height*0.75,100,50,yellow,light_yellow,"quit")

		pygame.display.update()

def Play():
    intro = True
    k = -1
    while intro:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                        Play()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_t:
                    	print "fingerCount"
                        k,cap = fingerCount(2)
                        cap.release()
                        print k
                        # pygame.time.wait(3)
                elif event.type == pygame.KEYUP:
                	if event.key == pygame.K_t:
                		cap.release()
                        

        gameDisplay.fill(white)

        button("play,%d"%(k), 150,500,100,50, green, light_green, action="None")

        pygame.display.update()

        clock.tick(15)


def Instructions():
	Intruc = True
	# k,cap = fingerCount(2)
	print "thread starting..."
	
	try:
	   # global k
	   thread.start_new_thread( fingerCount, (2, ) )
	except:
	   print "Error: unable to start thread"

	print "thread running, I'm out..."
	print "in instructions"
	# while Intruc:
	# 	for event in pygame.event.get():
	# 		if event.type == pygame.QUIT:
	# 			pygame.quit()
	# 			quit()
	# 		elif event.type == pygame.KEYDOWN:
	# 			if event.key == pygame.K_c:
	# 				Intruc = False
	# 			elif event.key == pygame.K_q:
	# 				pygame.quit()
	# 				quit()

	# 	gameDisplay.blit(whitebg,(0,0))
	# 	# gameDisplay.blit(paperImage,(0,0))
	# 	message_to_screen("The winner is decided by the show of hands.",black,-250,size="medium")
	# 	message_to_screen("Rock beats scissors",black,0,size="large")
	# 	message_to_screen("Scissor cut paper",black,-90,size="large")
	# 	message_to_screen("Paper subdue rock",black,-180,size="large")

	# 	button("Quit",display_width*0.45,display_height*0.75,100,50,yellow,light_yellow,"quit")

	# 	pygame.display.update()

def About():
	pass

# splash_screen()
# print fingerCount(2)
game_intro()