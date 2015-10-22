import pygame,time,random,cv2
from detectionFunction import fingerCount
from multiprocessing.pool import ThreadPool

#threading and opencv
pool = ThreadPool(processes=1)

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

def button(text,x,y,width,height,inactive_color,active_color,action,flag):

	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x+width > cur[0] > x and y+height> cur[1] > y:
		pygame.draw.rect(gameDisplay,active_color,(x,y,width,height))
		if click[0] and action != None:
			flag = action

	else:
		pygame.draw.rect(gameDisplay,inactive_color,(x,y,width,height))

	textButton(text,black,x,y,width,height)

	return flag

def call_on_click(action):
	if action == "play":
		Play()
	elif action == "instructions":
		Instructions()
	elif action == "about":
		About()
	elif action == "quit":
		pygame.quit()
		quit()
	elif action == "game_intro":
		game_intro()	

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
	click = "True"

	while click == "True":

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = 0
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.blit(whitebg,(0,0))

		message_to_screen("The classical game of -",black,-125,size="large")
		message_to_screen("ROCK PAPER SCISSORS!",black,-40,size="large")

		click = button("Play",display_width*0.15,display_height*0.75,100,50,green,light_green,"play",click)
		click = button("Instructions",display_width*0.35+5,display_height*0.75,120,50,red,light_red,"instructions",click)
		click = button("About",display_width*0.55,display_height*0.75,120,50,blue,light_blue,"about",click)
		click = button("Quit",display_width*0.75,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()

	print click
	call_on_click(click)

def Play():
    cap = cv2.VideoCapture(0)

    click = "True"
    
    while click == "True":
        for event in pygame.event.get():
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

        gameDisplay.fill(white)

        click = button("Main", 350,500,100,50, green, light_green, "game_intro",click)
        click = button("START", 550,500,100,50, green, light_green, "start",click)

        if click=="start":
        	click = "True"
        	count = async_result = pool.apply_async(fingerCount, (cap,1, ))
        	print count.get()

        pygame.display.update()

        clock.tick(15)

    call_on_click(click)

def Instructions():
	click = "True"
	
	while click == "True":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					Intruc = "False"
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.blit(whitebg,(0,0))
		# gameDisplay.blit(paperImage,(0,0))
		message_to_screen("The winner is decided by the show of hands.",black,-250,size="medium")
		message_to_screen("Rock beats scissors",black,0,size="large")
		message_to_screen("Scissor cut paper",black,-90,size="large")
		message_to_screen("Paper subdue rock",black,-180,size="large")

		click = button("Main",display_width*0.2,display_height*0.75,100,50,yellow,light_yellow,"game_intro")
		click = button("Quit",display_width*0.45,display_height*0.75,100,50,yellow,light_yellow,"quit")

		pygame.display.update()

	call_on_click(click)

def About():
	pass

# splash_screen()
game_intro()