# by Kristin Henry, 2014 @KristinHenry
# created  Jan 3, 2014
# Generative Art sketch
# quick and dirty experiment: generate random rainbow patterns
#

import random, math

import PIL
from PIL import Image, ImageDraw


imgSizeX = imgSizeY = 5000	# set default size of image
backgroundColor = "white"
backgroundColorAlpha = "white"

red = (255, 0, 0, 150)
orange = (255, 140, 0, 150)
yellow = (255, 255, 0, 150)
green = (0, 255, 0, 150)
blue = (0, 0, 255, 150)
purple = (140, 0, 255, 150)


# create background 
bkg = Image.new("RGB", (imgSizeX, imgSizeY), backgroundColor)

# create new image to draw into
im = Image.new("RGBA", (imgSizeX, imgSizeY), backgroundColorAlpha)

# Do the drawing
draw = ImageDraw.Draw(im)


def drawBow(x1, y1, x2, y2, startArc, stopArc):
	# ToDo: refactor this!
	mn = 0
	mx = gap = 100
	for i in range(mn,mx):
		draw.arc((x1, y1+i, x2+i, y2+i), startArc, stopArc, fill=red)
	mn += gap
	mx += gap
	for i in range(mn,mx):
		draw.arc((x1, y1+i, x2+i, y2+i), startArc, stopArc, fill=orange)
	mn += gap
	mx += gap
	for i in range(mn,mx):
		draw.arc((x1, y1+i, x2+i, y2+i), startArc, stopArc, fill=yellow)
	mn += gap
	mx += gap
	for i in range(mn,mx):
		draw.arc((x1, y1+i, x2+i, y2+i), startArc, stopArc, fill=green)
	mn += gap
	mx += gap
	for i in range(mn,mx):
		draw.arc((x1, y1+i, x2+i, y2+i), startArc, stopArc, fill=blue)
	mn += gap
	mx += gap
	for i in range(mn,mx):
		draw.arc((x1, y1+i, x2+i, y2+i), startArc, stopArc, fill=purple)


def getStartStop():
	start = random.randrange(0, 300)
	stop = random.randrange(start + 10, 360)
	return (start, stop)


def getBoundingBox():
	buf = 200
	x1 = random.randrange(buf, imgSizeX- 2*buf)
	y1 = random.randrange(buf, imgSizeY- 2*buf)
	x2 = random.randrange(x1 + buf, imgSizeX -buf)
	y2 = random.randrange(y1 + buf, imgSizeY - buf)
	return (x1, y1, x2, y2)

#-------------------------------------------------------
print "this may take a while ..."

for i in range(0, 100):
	bb = getBoundingBox()
	arc = getStartStop()
	drawBow(bb[0], bb[1], bb[2], bb[3], arc[0], arc[1])


bkg.paste(im, (0,0), im)

# save image with jpg suffix
bkg.save("rainbows.jpg")


