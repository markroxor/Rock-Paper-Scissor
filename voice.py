import pyttsx

def callRPS(text):
	engine = pyttsx.init()
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate-50)
	engine.say(text)
	# engine.say('Rock')
	# engine.say('Paper')
	# engine.say('Scissors.')
	engine.runAndWait()