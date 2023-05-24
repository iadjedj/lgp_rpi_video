import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import os
import fcntl

BUTTON_PIN = 40
FBIO_WAITFORVSYNC = 1074021920 # TODO: Make it nicer

# This code assumes all your videos are using the same framerate
# Could be easily improved but your get the idea!
FPS = 0

def check_sensor_state():
	# Wait 25ms to mock a slow sensor
	# time.sleep(0.025)

	return (GPIO.input(BUTTON_PIN) == GPIO.LOW)

def load_video(path):
	global FPS

	my_video = cv2.VideoCapture(path, cv2.CAP_FFMPEG)

	frameCount = int(my_video.get(cv2.CAP_PROP_FRAME_COUNT))
	frameWidth = int(my_video.get(cv2.CAP_PROP_FRAME_WIDTH))
	frameHeight = int(my_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

	FPS = int(my_video.get(cv2.CAP_PROP_FPS))

	buf = np.empty((frameCount, frameHeight, frameWidth, 2), np.dtype('uint8'))

	cur_frame = 0
	ret = True

	print(f"Loading video: {path}")
	while cur_frame < frameCount and ret:
		ret, frame = my_video.read()
		cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)
		buf[cur_frame] = cvt_frame
		cur_frame += 1

	my_video.release()
	
	print(f"Video {path}, fully loaded\n")

	return buf

def main():
	# GPIO init
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	print("Loading videos:\n")

	video1 = load_video("video1.mp4")
	video2 = load_video("video2.mp4")

	# This was not explained in the video, but without this
	# you will see the blinking cursor of the terminal
	os.system('sudo sh -c "TERM=linux setterm -foreground black -clear all > /dev/tty0"')

	# I know, opening twice the file is ugly, but I need a file descriptor for ioctl
	# You could open it once using os.open() and use mmap.mmap() instead of
	# the numpy implementation of mmap
	fb_fd = os.open("/dev/fb0", os.O_RDWR)
	fb_map = np.memmap("/dev/fb0", dtype='uint8',mode='r+', shape=(1080,1920,2))

	current_video = video1
	current_frame = 0

	last_frame_ts = 0

	while True:
		triggered = check_sensor_state()

		if triggered and current_video is video1:
			current_frame = 0
			current_video = video2
		elif not triggered and current_video is video2:
			current_frame = 0
			current_video = video1

		fcntl.ioctl(fb_fd, FBIO_WAITFORVSYNC)
		fb_map[:] = current_video[current_frame]

		since_last = time.perf_counter() - last_frame_ts
		to_wait = (1/FPS) - since_last

		if to_wait > 0:
			time.sleep(to_wait)
		else:
			print(f"Player lagging behind by: {(to_wait * -1000):.2f}ms")

		last_frame_ts = time.perf_counter()

		current_frame += 1
		if current_frame == len(current_video):
			current_frame = 0

if __name__ == '__main__':
	main()