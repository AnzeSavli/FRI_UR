#!/usr/bin/env python
import cv2 as cv
import numpy as np
import math
import random
import json
import sys

file = open("/home/pi/Desktop/Matura/output.txt", "w")
 
def zaznaj():
	
	nbr = random.randint(1,7)
	
	string = "/home/pi/Desktop/Matura/slike/slika" + str(nbr) + ".jpg"
	
	img = cv.imread(string)
	# cv.imshow("img",img)	
	# cv.waitKey(0)
	hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
	
	lower = np.array([0,140,140], dtype = "uint8")
	upper = np.array([255,255,255], dtype = "uint8")
	
	mask = cv.inRange(hsv,lower,upper)
	
	ret, thresh = cv.threshold(mask,127,255,cv.THRESH_BINARY_INV)
	contours, hierarchy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
	
	posX = []
	posY = []
	
	for c in contours:
		M = cv.moments(c)
		cX = int(M["m10"] / M["m00"])
		cY = int(M["m01"] / M["m00"])
	
		print(cX,cY)
		posX.append(cX)
		posY.append(cY)
	
	mat_cx = np.asarray(posX)
	mat_cy = np.asarray(posY)
	vals = np.column_stack((mat_cx, mat_cy))
	
	div = 319 / 9
	dist = []
	
	for i in range(len(vals)):
	    tmp = math.pow(vals[i][0] - 319, 2)
	    tmp2 = math.pow(vals[i][1] - 319, 2)
	    dist.append(int(math.sqrt(tmp + tmp2)))
	
	dist.pop(0)
	print(dist)
	score = []
	for i in range(len(dist)):
	    score.append(9-(dist[i]/div))
	
	for i in range(len(score)):
		if score[i] < 0:
			score[i] = 0
	
	print(score)
	
	score2 = json.dumps(score)
	
	# cv.imshow("newImg", thresh)
	# cv.waitKey(0)
	
	# cv.destroyAllWindows()
	
	file.write(score2)

#for i in range(5):
zaznaj()

file.close()
