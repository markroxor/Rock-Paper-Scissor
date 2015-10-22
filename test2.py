import cv2,pygame
from detectionFunction import fingerCount

capture = cv2.VideoCapture(0)   

k = fingerCount(capture,2)
print k

pygame.time.wait(3000)   

k = fingerCount(capture,2)
print k

pygame.time.wait(3000)