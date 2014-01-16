#
# by Kristin Henry, 2014 @KristinHenry
# created  Jan, 2014
# Generative Art sketch
# quick and dirty experiment: generate tarsiers inspired patterns
#
# In case you didn't already know this, tarsiers are very cute and have huge eyes. 
#

import random, math

import PIL
from PIL import Image, ImageDraw


imgSizeX = 9000
imgSizeY = 4000	# set default size of image
backgroundColor = "black"
backgroundColorAlpha = "black"

# some blue colors
colors = [(73, 48, 173, 150), (30, 28, 119, 150),
		  (43, 38, 91, 150), (20, 22, 84, 150),
		  (17, 33, 81, 150), (45, 0, 142, 150), 
		  (43, 17, 102, 150), (0, 114, 198, 150),
          (0, 40, 104, 150), (0, 91, 153, 150),
          (10, 10, 10, 150), (20, 20, 20, 150)]
         
          

# create background 
bkg = Image.new("RGB", (imgSizeX, imgSizeY), backgroundColor)

# create new image to draw into
im = Image.new("RGBA", (imgSizeX, imgSizeY), backgroundColorAlpha)

# Do the drawing
draw = ImageDraw.Draw(im)


def getColor():
	return colors[random.randrange(0, len(colors) - 1)]


def drawEye(x, y, dx, dy, color):
	draw.ellipse( (x, y, x+dx, y+dy), color)


def drawTarsier(pos):
	x1 = pos[0]
	y1 = pos[1]
	x2 = x1 + 1100
	y2 = y1
	dx = dy = 1000 
	dxMin = random.randrange(100, 250)

	# draw background
	midX = x1 + dx/2
	midY = y1 + dy/4
	span = 500
	color = (20, 20, 20, 10)
	draw.ellipse( (midX - span, midY - span, midX + dx + span, midY + dy + span/2), color)

	# draw eyes
	for i in range(0, 50):

		color = getColor()
		drawEye(x1, y1, dx, dy, color)
		drawEye(x2, y2, dx, dy, color)

		if dx > dxMin:
			x1 += 10
			y1 += 10
			x2 += 10
			y2 += 10
			dx -= 20
			dy -= 20
		else:
			color = (0,0,0,150)
			drawEye(x1, y1, dx, dy, color)
			drawEye(x2, y2, dx, dy, color)


#-------------------------------------------------------
print "this may take a while ..."

minX = 600
minY = 600
maxX = imgSizeX - 3000
maxY = imgSizeY - 2000

for i in range(0, 20):
	pos = (random.randrange(minX, maxX), random.randrange(minY, maxY))
	drawTarsier(pos)
	
	
bkg.paste(im, (0,0), im)

# save image with jpg suffix
bkg.save("tarsiers.jpg")

