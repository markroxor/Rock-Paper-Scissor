import cv2,pygame

capture = cv2.VideoCapture(0)   

ret,img = capture.read()

print ret
capture.release()
ret,img = capture.read()
capture.release()
del capture
print ret
pygame.time.wait(5000)                 # release it