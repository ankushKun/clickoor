from picamera2 import Picamera2
from libcamera import controls
from gpiozero import Button
import pygame
import sys
import time
import os
from signal import pause


shutter = Button(5, hold_time=3)

pygame.init()
res = (720, 480)
pres = (720, 480)
ires = (1920, 1080)
screen = pygame.display.set_mode(res)

screen.fill((0, 0, 0))
pygame.display.update()

cam = Picamera2()
cam.preview_configuration.main.size = pres
cam.preview_configuration.main.format = 'BGR888'
capture_config = cam.create_still_configuration({"size": ires})
cam.configure("preview")
cam.start()
cam.set_controls({"AfMode": controls.AfModeEnum.Continuous})


def capture_img():
    global previewing
    if previewing:
        previewing = False
        return
    print("capturing image")
    cam.switch_mode_and_capture_file(capture_config, "img.png")
    time.sleep(1)


def start_preview():
    global previewing
    previewing = True


shutter.when_released = capture_img
shutter.when_held = start_preview

running = True
previewing = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("quitting")
                running = False
            elif event.key == pygame.K_SPACE:
                capture_img()
            elif event.key == pygame.K_p:
                previewing = True

    if previewing:
        img = pygame.image.load("img.png")
        iw, ih = img.get_size()
        sf = min(screen.get_width() / iw, screen.get_height() / ih)
        img = pygame.transform.scale(img, (iw*sf, ih*sf))
    else:
        array = cam.capture_array()
        img = pygame.image.frombuffer(array.data, pres, 'RGB')

    screen.fill((0, 0, 0))
    screen.blit(img, (0, 0))
    pygame.display.update()

cam.close()
pygame.quit()
sys.exit()
