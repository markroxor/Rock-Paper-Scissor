#Imports
import pygame,time,random,cv2,pyttsx
from detectionFunction import fingerCount
from multiprocessing.pool import ThreadPool
from collections import Counter
from voice import callRPS
#Threading and Opencv
pool = ThreadPool(processes=1)
cap = cv2.VideoCapture(0)
#
#Pygame Initialisation and Macros
sampleTime = 3.0
stScore = 5

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

# pygame.display.toggle_fullscreen()
#

#Icon
# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

#Images
backImage = pygame.image.load("img1.png")
paperImage = pygame.image.load("paper.png")
fistImage = pygame.image.load("fist.png")
scissorImage = pygame.image.load("scissor.png")
whitebg = pygame.image.load("white-background.png")

#Fonts
smallfont = pygame.font.SysFont("comicsansms",25)
medfont = pygame.font.SysFont("comicsansms",50)
largefont = pygame.font.SysFont("comicsansms",85)
#

#Clock
clock = pygame.time.Clock()
#

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
	elif action == "credits":
		Credits()
	elif action == "quit":
		pygame.quit()
		quit()
	elif action == "game_intro":
		game_intro()	

def message_to_screen(msg,color, y_displace = 0, size = "small",x_diplace=int(display_width / 2)):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (x_diplace, int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

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

def genRandHand(randm = random.randint(0,2)):

	if randm == 0:
		gameDisplay.blit(fistImage,(display_width/2,display_height/2))
	elif randm == 1:
		gameDisplay.blit(paperImage,(display_width/2,display_height/2))
	elif randm == 2:
		gameDisplay.blit(scissorImage,(display_width/2,display_height/2))

	return randm

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
		click = button("Credits",display_width*0.55,display_height*0.75,120,50,blue,light_blue,"credits",click)
		click = button("Quit",display_width*0.75,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()

	call_on_click(click)

def Play():
	click = "True"

	curClock = time.time()
	startClock = 0
	defects = []
	verdict  = 0

	cpuScore = stScore
	playerScore = stScore
	showTime = 0

	while click == "True":
		curClock = time.time()

		try:
			fcount = fingerCount (cap,5)
		except:
			print "No Shape"

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

		# scores(playerScore,cpuScore)

		click = button("Main", 350,500,100,50, green, light_green, "game_intro",click)
		click = button("START", 550,500,100,50, green, light_green, "start",click)


		if click=="start":
			click = "True"
			print "Rock..."
			pool.apply_async(callRPS, ("Rock",)) #multiprocessing works wonders
			print "Paper..."
			pool.apply_async(callRPS, ("Paper",)) #multiprocessing works wonders
			print "Scissors."
			pool.apply_async(callRPS, ("Scissor",)) #multiprocessing works wonders
			startClock = time.time()
			defects = []
			verdict  = 1 
			showTime = 0
			# count = pool.apply_async(fingerCount, (cap,5, ))
			# print count.get()

		if curClock-startClock<sampleTime:
			message_to_screen("Show hands for %d secs"%(int(sampleTime)-int(curClock-startClock)),black,-180,size="large")

			genRandHand(randm = random.randint(1,3))
			defects.append(fcount)

		elif verdict: 
			showTime = 1
			verdict = 0
			data = Counter(defects)
			randm = random.randint(0,2)
			plShow = -1

			if data.most_common(1)[0][0]==4 or data.most_common(1)[0][0]==5:
				plShow = 1
				print "paper"
			elif data.most_common(1)[0][0]==3 or data.most_common(1)[0][0]==1:
				plShow = 0
				print "fist"
			elif data.most_common(1)[0][0]==2:# or data.most_common(1)[0][0]==2:
				plShow = 2
				print "scissor"
			else:
				print "INVALID MOVE!"

			print data.most_common(1)[0][0],randm
			print scoreIncrement(plShow,randm)

		if showTime:
			genRandHand(randm)


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

		message_to_screen("The winner is decided by the show of hands.",black,-250,size="medium")
		message_to_screen("Rock beats scissors",black,0,size="large")
		message_to_screen("Scissor cut paper",black,-90,size="large")
		message_to_screen("Paper subdue rock",black,-180,size="large")

		click = button("Main",display_width*0.3,display_height*0.75,100,50,yellow,light_yellow,"game_intro",click)
		click = button("Quit",display_width*0.6,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()

	call_on_click(click)

def Credits():
	click = "True"
	
	while click == "True":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					click = "False"
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.blit(whitebg,(0,0))

		message_to_screen("This game is based on the idea invoked by",black,-180,size="medium")
		message_to_screen("Ranjan Purbey in Java using Javafx,",black,-90,size="medium")
		message_to_screen("and then further extended to Python using pygame.",black,0,size="medium")
		
		click = button("Main Menu",display_width*0.3,display_height*0.75,100,50,yellow,light_yellow,"game_intro",click)
		click = button("Quit",display_width*0.6,display_height*0.75,100,50,yellow,light_yellow,"quit",click)

		pygame.display.update()

	call_on_click(click)

# splash_screen()
game_intro()