#
# by Kristin Henry, 2014 @KristinHenry
# created  Jan, 2014
# Generative Art sketch
# quick and dirty experiment: generate tilted ellipses
#


import random, math

import PIL
from PIL import Image, ImageDraw


imgSizeX = 1000
imgSizeY = 1000	# set default size of image
backgroundColor = "white" 
backgroundColorAlpha = "white" 

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


def drawRing(origin, thickness, numPoints, size, rot, color):

	rot = rot * math.pi/180

	rx = size[0] 
	ry = size[1] 
	slice = 2 * math.pi/numPoints
	
	for ring in range(0,thickness):
		rx = rx - 1
		ry = ry - 1
		
		# plot and rotate first point in ellipse
		x0 = (rx) * math.cos(0) 
		y0 = (ry) * math.sin(0) 
		x = (x0 * math.cos(rot)) - (y0 * math.sin(rot)) + origin[0]
		y = (x0 * math.sin(rot)) + (y0 * math.cos(rot)) + origin[1]

		for t in range(1, numPoints + 1):
			# plot ellipse
			x1 = (rx)* math.cos(t*slice) 
			y1 = (ry) * math.sin(t*slice) 
			# shift into rotated position
		 	x2 = (x1 * math.cos(rot)) - (y1 * math.sin(rot)) + origin[0]
		 	y2 = (x1 * math.sin(rot)) + (y1 * math.cos(rot))  + origin[1]

		 	draw.line((x,y, x2, y2), color)

			# update for next arc
			x = x2
			y = y2
		

def drawDress(pos):

	for i in range(0, 10):
		points = 40

		origin = (pos[0], random.randrange(100, 800)) 
		
		color = colors[random.randrange(0, len(colors) -1)]
		
		thickness = random.randrange(10,20)
		
		dx = random.randrange(100, 400)
		dy = random.randrange(40, 100)
		size = (dx, dy)

		rotation = random.randrange(-20, 20)

		drawRing(origin, thickness, points, size, rotation, color)
		draw.ellipse((origin[0], origin[1], origin[0] + 10, origin[1] + 10), fill='red')


#-------------------------------------------------------
print "this may take a while ..."

minX = 300 
minY = 300
maxX = imgSizeX - minX 
maxY = imgSizeY - minY 

# I made this a loop, so I can draw multiple "dresses"
for i in range(0, 1):
	pos = (random.randrange(minX, maxX), random.randrange(minY, maxY))
	drawDress(pos)
	
	
bkg.paste(im, (0,0), im)

# save image with jpg suffix
bkg.save("jupiterDress.jpg")

