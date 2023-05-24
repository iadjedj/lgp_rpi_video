import cv2
import numpy as np
import time

def load_video(path):
	my_video = cv2.VideoCapture(path, cv2.CAP_FFMPEG)

	# Need to cast these values to int to pass them as parameters for numpy
	frameCount = int(my_video.get(cv2.CAP_PROP_FRAME_COUNT))
	frameWidth = int(my_video.get(cv2.CAP_PROP_FRAME_WIDTH))
	frameHeight = int(my_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

	buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

	cur_frame = 0
	ret = True

	print(f"Loading video: {path}")
	while cur_frame < frameCount and ret:
	    # read() returns two values
	    # - ret: False if there was a problem getting a new frame
	    #		(end of file or an error)
	    # - frame: A new frame
		ret, frame = my_video.read()
		buf[cur_frame] = frame
		cur_frame += 1

	# Release the VideoCapture since we don't need it anymore
	my_video.release()
	
	print(f"Video {path}, fully loaded\n")

	return buf

def main():
	print("Loading videos:\n")

	video1 = load_video("video1.mp4")
	video2 = load_video("video2.mp4")

	print("All videos loaded.")

	print("Pausing a bit so you can read the memory usage :'D")
	time.sleep(5)
	print("Bisous, bbye!\n")

if __name__ == '__main__':
	main()