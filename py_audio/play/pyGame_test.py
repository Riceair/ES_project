import time
import pygame

filepath="D:/..music_data/J-Pop/ClariS-ClariS - Single Best 1st-09-Click.mp3"

pygame.mixer.init()

track = pygame.mixer.music.load(filepath)

#開始播放
pygame.mixer.music.play()

input("To pause")
pygame.mixer.music.pause()

input("To play")
pygame.mixer.music.unpause()

input("To pause")
pygame.mixer.music.stop()

#停止
# pygame.mixer.music.stop()