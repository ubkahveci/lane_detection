import cv2 as cv
import numpy as np


def process_frame():
	ret, frame = video.read()
	global h
	global w
	h,w = int(frame.shape[0]//3), int(frame.shape[1]//3)
	frame = cv.resize(frame,(w,h))
			
	copy = np.copy(frame)
	grey = cv.cvtColor(copy, cv.COLOR_BGR2GRAY)
	gauss = cv.GaussianBlur(grey, (5,5), 0)
	edges = cv.Canny(grey,20,150)
	isolated = region(edges)
	lines = cv.HoughLinesP(isolated, rho = 1, theta = np.pi/180, threshold = 75, lines = np.array([]), minLineLength=1, maxLineGap=25)
	#average_lines = average(copy, lines)
	image_with_lines = display_lines(copy, lines)
	cv.imshow("lanes", image_with_lines)
	cv.waitKey(1)

def display_lines(image, lines):
	copied_image = np.copy(image)
	blank_image = np.zeros((h, w, 3), dtype=np.uint8)

	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line[0]
			cv.line(blank_image, (x1,y1), (x2,y2), color = (0,255,0), thickness = 2)
	else:
		pass

	image = cv.addWeighted(image, 0.8, blank_image, 1, 0)
	return image


def region(image):

	triangle = [
		(100, h), (w//2, h*2/3), (w-100,h)
	]

	mask = np.zeros_like(image)
	mask = cv.fillPoly(mask, np.int32([triangle]), color=(255,255,255))
	mask = cv.bitwise_and(image, mask)

	return mask

def average(image, lines):
	left = []
	right = []
	if lines is not None:    	
		for line in lines:
			x1, y1, x2, y2 = line.reshape(4)
			parameters = np.polyfit((x1, x2), (y1, y2), 1)
			slope = parameters[0]
			y_int = parameters[1]
			if slope < 0:
				left.append((slope, y_int))
			else:
				right.append((slope, y_int))
	else:
		pass

	right_avg = np.average(right, axis=0)
	left_avg = np.average(left, axis=0)
    
	return np.array([left_line, right_line])

#capturing the video and saving it to an object
video= cv.VideoCapture('driving_video_samples\\citydriving3.mp4')

while video.isOpened():
	process_frame()	
video.release()
cv.destroyAllWindows()