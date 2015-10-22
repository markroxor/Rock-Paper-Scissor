from detectionFunction import fingerCount
import thread,threading,time,cv2
def k():
	print "thread starting..."
	
	try:
	   # global k
	   thread.start_new_thread( fingerCount, (2) )
	except:
	   print "Error: unable to start thread"

	print "thread running, I'm out..."

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)

async_result = pool.apply_async(fingerCount, (2, )) # tuple of args for foo

# do some other stuff in the main process

# return_val = async_result.get()  # get the return value from your function.
# print return_val
ori = time.time()
clk = time.time()
ptime =clk

while clk-ori<10.0:
	# pass
	clk = time.time()

	if clk-ptime>5:
		ptime = clk
		async_result1 = pool.apply_async(fingerCount, (2, ))


print async_result.get()
 