import pygame,time
import pygame.camera

pygame.camera.init()

# print pygame.camera.list_cameras()[0]

cap = pygame.camera.Camera(pygame.camera.list_cameras()[0],(640,480))
cap.start()

ori = time.time()
clk = time.time()

while clk-ori<5:
	clk = time.time()
	surf = cap.get_image()
	pygame.image.save(surf, "image121221.jpg")
cap.stop()
pygame.time.wait(5000)