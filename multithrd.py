#!/usr/bin/python

import thread,threading
import time

# Define a function for the thread
k = -1
def print_time( threadName, delay):
	count = 0
	while count < 5:

		# p = threading.activeCount()
		# print p
		time.sleep(delay)
		count += 1
		print "%s: %s" % ( threadName, time.ctime(time.time()) )
	return 10
# Create two threads as follows
try:
   # global k
   thread.start_new_thread( print_time, ("Thread-1", 0.4, ) )
   thread.start_new_thread( print_time, ("Thread-2", 0.4, ) )
except:
   print "Error: unable to start thread"

ori = time.time()
clk = time.time()
ptime =clk

while clk-ori<5.0:

	# global k
	# print k
	# clk = time.time()

	# if clk-ptime>1:
	# 	ptime = clk
	# 	p = threading.enumerate()
	# 	print p

# 	pass