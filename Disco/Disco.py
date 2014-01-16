#
# by Kristin Henry, 2014 @KristinHenry
# created  Jan, 2014
# Generative Art sketch
# quick and dirty experiment: generate random disco floor pattern
#

import random, math

import PIL
from PIL import Image, ImageFont, ImageDraw


imgSizeX = imgSizeY = 5000	# set default size of image
backgroundColor = "black"
backgroundColorAlpha = "black"

# some disco colors
colors = [(236, 33, 141, 150), (106, 185, 215, 150), (252, 246, 10, 150),
          (255, 91, 2, 150), (195, 231, 35, 150)]

# create background 
bkg = Image.new("RGB", (imgSizeX, imgSizeY), backgroundColor)

# create new image to draw into
im = Image.new("RGBA", (imgSizeX, imgSizeY), backgroundColorAlpha)

# Do the drawing
draw = ImageDraw.Draw(im)


def getXY(i, cols, dx, dy, gap, xy):
	
	row = i/cols
	col = int(math.fmod(i, cols))

	x = (col * dx) + (col * gap) + xy[0]
	y = (row * dy) + (row * gap) + xy[1]
	
	return (x,y)


def getColor():
	return colors[random.randrange(0, len(colors) - 1)]


def drawTile(x, y, dx, dy, color):
	draw.polygon([(x,y), (x+dx, y), (x+dx, y+dy), (x, y+dy)], fill=color)


def getStartXY():
	#ToDo: make this relative to image size and such
	return (140, 140)

#-------------------------------------------------------
print "this may take a while ..."

xyOffsets = getStartXY()
dx = dy = 300 
gap = 40
cols = 14
for i in range(0, 196):
	xy = getXY(i, cols, dx, dy, gap, xyOffsets)

	# light up random squares, like a disco dance floor
	if random.randrange(0, 2) == 0:
		drawTile(xy[0], xy[1], dx, dy, getColor())
	

bkg.paste(im, (0,0), im)

# save image with jpg suffix
bkg.save("disco.jpg")

