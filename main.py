#Imports
import pygame,time,random,cv2,pyttsx,pygame.camera
from detectionFunction import fingerCount
from multiprocessing.pool import ThreadPool
from collections import Counter
from voice import callRPS

#Threading and Camera Initialisation
pool = ThreadPool(processes=1)
pygame.camera.init()
cap = pygame.camera.Camera(pygame.camera.list_cameras()[0],(400,300))

#
#Pygame Initialisation and Macros
sampleTime = 3.0
stScore = 5
imageWidth = 400
imageHeight = 300 

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

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Rock Paper Scissor")

pygame.display.toggle_fullscreen()
#

#Icon
# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

#Images
backImage = pygame.image.load("pun.png")
whitebg = pygame.image.load("white-background.png")

paperImage = pygame.image.load("paper.png")
fistImage = pygame.image.load("fist.png")
scissorImage = pygame.image.load("scissor.png")

#Fonts
smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",85)
#

#Clock
clock = pygame.time.Clock()
#
num2show = ['rock', 'paper','scissor']

#Main Defs
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

def button(text,x,y,width,height,inactive_color,active_color,action,flag,toggle=1):

	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x+width > cur[0] > x and y+height> cur[1] > y:
		pygame.draw.rect(gameDisplay,active_color,(x,y,width,height))
		if click[0] and action != None:
			flag = action
			toggle = not toggle

	else:
		pygame.draw.rect(gameDisplay,inactive_color,(x,y,width,height))

	textButton(text,black,x,y,width,height)

	return flag,toggle

def call_on_click(action):
	if action == "play":
		Play()
	elif action == "instructions":
		Instructions()
	elif action == "credits":
		Credits()
	elif action == "quit":
		pygame.quit()
		quit()
	elif action == "game_intro":
		game_intro()	

def message_to_screen(msg,color, y_displace = 0, size = "small",x_displace=0,called=[]):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2)+x_displace, int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)
    if msg in called:
    	pass
    else:
	    pool.apply_async(callRPS, (msg,))
	    called.append(msg)

def scoreIncrement(playerShow,cpuShow):

	if playerShow==cpuShow or playerShow == -1:
		return 0

	if playerShow == 0 and cpuShow == 1:
		return -1
	elif playerShow == 1 and cpuShow == 2:
		return -1
	elif playerShow == 2 and cpuShow == 0:
		return -1
	else:
		return 1

def scores(playerScore,cpuScore):
	message_to_screen("Player Score: %d"%(playerScore),black,-250,"medium",140)
	message_to_screen("CPU Score: %d"%(cpuScore),black,-250,"medium",display_width - 140)

def genRandHand(cpuShow = random.randint(0,2),xOffset=0,yOffset=0):

	if cpuShow == 0:
		gameDisplay.blit(fistImage,(display_width/2-fistImage.get_size()[0]+xOffset,display_height/2+yOffset))
	elif cpuShow == 1:
		gameDisplay.blit(paperImage,(display_width/2-paperImage.get_size()[0]+xOffset,display_height/2+yOffset))
	elif cpuShow == 2:
		gameDisplay.blit(scissorImage,(display_width/2-scissorImage.get_size()[0]+xOffset,display_height/2+yOffset))

	return cpuShow

def pause_screen():
	message_to_screen("Game Paused",black,0,"Large")


def splash_screen(time):
	gameDisplay.blit(backImage,(0,-35))
	pygame.display.update()
	pygame.time.wait(time)
	clock.tick(5)

def game_intro():

	called = []
	click = "True"

	while click == "True":

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_t:
					pygame.display.toggle_fullscreen()

		gameDisplay.blit(whitebg,(0,0))

		message_to_screen("The classical game of -",black,-125,size="large",called=called)
		message_to_screen("ROCK PAPER SCISSORS!",black,-40,size="large",called=called)
		message_to_screen("Press T to toggle fullscreen.",black,60,size="small",called=called)
		message_to_screen("or Q to quit anytime in the game.",black,90,size="small",called=called)

		click,_ = button("Play",display_width*0.15,display_height*0.75,100,50,green,light_green,"play",click)
		click,_ = button("Instructions",display_width*0.35+5,display_height*0.75,120,50,red,light_red,"instructions",click)
		click,_ = button("Credits",display_width*0.55,display_height*0.75,120,50,blue,light_blue,"credits",click)
		click,_ = button("Quit",display_width*0.75,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()
		clock.tick(60)

	call_on_click(click)

def Play():
	called = []

	cap.start()
	click = "True"

	curClock = time.time()
	startClock = 0
	shows = []
	verdict  = 0

	score = stScore
	showTime = 0

	debug = 0
	while click == "True":
		#To avoid registration of multiple clicks
		pygame.time.wait(30)
		curClock = time.time()

		try:
			fingCount = fingerCount (5)
		except:
			print "Error in detectionFunction.py"

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_t:
					pygame.display.toggle_fullscreen()

		gameDisplay.fill(white)

		click,_ = button("Main Menu", (display_width*0.8)/5,(display_height*7)/8,100,50, green, light_green, "game_intro",click)
		click,_ = button("Start", (display_width*2.33)/5,(display_height*7)/8,100,50, green, light_green, "start",click)
		click,debug = button("Debug", (display_width*4)/5,(display_height*7)/8,100,50, green, light_green, "True",click,debug)


		if click=="start":
			click = "True"
	
			print "Rock..."
			pool.apply_async(callRPS, ("Rock",)) #multiprocessing works wonders
			print "Paper..."
			pool.apply_async(callRPS, ("Paper",)) #multiprocessing works wonders
			print "Scissors."
			pool.apply_async(callRPS, ("Scissor",)) #multiprocessing works wonders
			startClock = time.time()
			shows = []
			verdict  = 1 
			showTime = 0
			# count = pool.apply_async(fingerCount, (cap,5, ))
			# print count.get()

		if curClock-startClock<sampleTime:
			frame = cap.get_image()
			pygame.image.save(frame, "input.png")
			# message_to_screen("Show hands for %d secs"%(int(sampleTime)-int(curClock-startClock)),black,-180,size="large")
			genRandHand(xOffset=25,cpuShow = random.randint(1,3))
			shows.append(fingCount)

		elif verdict: 
			called = []

			showTime = 1
			verdict = 0
			counteredShows = Counter(shows)
			cpuShow = random.randint(0,2)
			plShow = -1

			if counteredShows.most_common(1)[0][0]==4 or counteredShows.most_common(1)[0][0]==5:
				plShow = 1
				print "paper"
			elif counteredShows.most_common(1)[0][0]==3 or counteredShows.most_common(1)[0][0]==1:
				plShow = 0
				print "fist"
			elif counteredShows.most_common(1)[0][0]==2:# or counteredShows.most_common(1)[0][0]==2:
				plShow = 2
				print "scissor"
			else:
				print "INVALID MOVE!"

			print counteredShows.most_common(1)[0][0],cpuShow
			print scoreIncrement(plShow,cpuShow)
			score += scoreIncrement(plShow,cpuShow)

		if showTime:
			# cap.stop()
			genRandHand(cpuShow,-220)
			genRandHand(plShow,280)
			called.append("Your Show")
			message_to_screen("Your Show",black,x_displace=250,y_displace=100,size="small",called=called)
			called.append("CPU Show")
			message_to_screen("CPU Show",black,x_displace=-250,y_displace=100,size="small",called=called)

 
		if debug:

			frame = cap.get_image()
			pygame.image.save(frame, "input.png")

			outputImage = pygame.image.load("output.png")
			inputImage = pygame.image.load("input.png")
			
			inputImage = pygame.transform.scale(inputImage, (imageWidth,imageHeight))
			outputImage = pygame.transform.scale(outputImage, (imageWidth,imageHeight))

			gameDisplay.blit(inputImage,(0,0))
			gameDisplay.blit(outputImage,(display_width-imageWidth,0))

		message_to_screen("Score: %d"%(score),black,200,size="medium",called=called)

		pygame.display.update()
		clock.tick(60)

	cap.stop()
	call_on_click(click)

def Instructions():

	click = "True"
	called = []

	while click == "True":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_t:
					pygame.display.toggle_fullscreen()

		gameDisplay.blit(whitebg,(0,0))

		message_to_screen("The winner is decided by the show of hands.",black,-160,size="medium",called=called)
		message_to_screen("Rock beats scissors",black,-80,size="large",called=called)
		message_to_screen("Scissor cut paper",black,0,size="large",called=called)
		message_to_screen("Paper subdue rock",black,80,size="large",called=called)

		click,_ = button("Main",display_width*0.2,display_height*0.75,100,50,yellow,light_yellow,"game_intro",click)
		click,_ = button("Quit",display_width*0.7,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()
		clock.tick(60)


	call_on_click(click)

def Credits():
	click = "True"
	
	while click == "True":

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
				elif event.key == pygame.K_t:
					pygame.display.toggle_fullscreen()

		gameDisplay.blit(whitebg,(0,0))

		message_to_screen("This game is based on the idea invoked by",black,-180,size="medium")
		message_to_screen("Ranjan Purbey in Java using Javafx,",black,-90,size="medium")
		message_to_screen("and then further extended to Python using pygame.",black,0,size="medium")
		
		click,_ = button("Main Menu",display_width*0.2,display_height*0.75,100,50,yellow,light_yellow,"game_intro",click)
		click,_ = button("Quit",display_width*0.7,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()
		clock.tick(60)

	call_on_click(click)

splash_screen(1500)
game_intro()