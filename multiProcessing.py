from detectionFunction import fingerCount
import thread,threading,time,cv2

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=1)

cap = cv2.VideoCapture(0)
# cap = 1
async_result = pool.apply_async(fingerCount, (cap,1, )) # tuple of args for foo

# do some other stuff in the main process

return_val = async_result.get()  # get the return value from your function.
print return_val
ori = time.time()
clk = time.time()
ptime =clk

while clk-ori<10.0:
	# pass
	clk = time.time()

	if clk-ptime>1:
		ptime = clk
		async_result = pool.apply_async(fingerCount, (cap,1, ))
		print async_result.get()
 