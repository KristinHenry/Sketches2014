#
# by Kristin Henry, 2014 @KristinHenry
# created  Jan, 2014
# Generative Art sketch
# quick and dirty experiment: generate paw print tracks
#

import os
import random
import math

from PIL import Image, ImageChops


imgSizeX = col = 3000
imgSizeY = row = 3000
background = "white" 

# create new image to paste files into
size = (col, row)
im2 = Image.new("RGBA", size, background)

xmax = im2.size[0]
ymax = im2.size[1]

tries = 0

col = 0
row = 0


def makeNewFolder(foldername):
    try:
        return os.makedirs(foldername)
    except OSError:
        pass



# got code for trimming here: http://stackoverflow.com/questions/10615901/trim-whitespace-using-pil
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -4)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    
    
def whiteToAlpha(im):
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)



def whiteToAlphaFast(im):
    #print "convert white to alpha fast", im
   
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0) #(100, 0, 0, 255)   
            else:
                break
        for x in reversed(xrange(im.size[0])):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0) #(100, 0, 0, 255)   
            else:
                break
                
                             
def processFiles(filesToTrim, src, dest):
    for img in filesToTrim:
        im = Image.open(src + "//" + img)
        
        scaleby = .5 #1.0 #0.75 #0.2 #0.5
        im = im.resize( [int(scaleby * s) for s in im.size] )
        
        im = trim(im)        
        im.save(dest + "//" + img)


def checkIfOutOfBounds(xbox, ybox, xbuf, ybuf):
    maxX = xmax - xbuf
    maxY = ymax - ybuf
    minX = xbuf
    minY = ybuf
    
    if xbox > maxX:
        return True
    elif xbox < minX:
        return True
    elif ybox > maxY:
        return True
    elif ybox < minY:
        return True
    else:
        return False


def checkOverlap(x1, y1, x2, y2):
    
    testpoint = [(x2 + x2) / 2, (y1 + y2) / 2]
    pix = im2.load()
   
    if testpoint[0] > im2.size[0]:
        return True
    elif testpoint[1] > im2.size[1]:
        return True
    else:
        print "test" #pix[test[0], test[1]]
   
    return False
        
    

def findPosition(im, last):
    # bounding box location for pasting into
    buf = 20
    xbuf = buf + im.size[0]
    ybuf = buf + im.size[1]

    xdir = ydir = -1
    if random.randrange(0,2) == 0:
        xdir = 1
    if random.randrange(0,2) == 0:
        ydir = 1
    print "xdir,ydir: " , xdir, ",", ydir

    xbox = last[0] + xdir * im.size[0] + random.randrange(0, 10)
    ybox = last[1] + ydir * im.size[1] + random.randrange(0, 10)
    
    return (xbox, ybox)
         
    


def makeTracks():

    mx = 500
    last = (imgSizeX/2, imgSizeY/2)
    for a in range(0, mx):

        im = Image.open(dest + "/" + tempfiles[random.randint(0, len(tempfiles)-1)])

        box = findPosition(im, last)
        
        im = im.convert("RGBA")
        whiteToAlphaFast(im)
        r, g, b, alpha = im.split()

        im2.paste(im, box, mask=alpha)

        last = box
        a += 1
        
    return im2

    
        

#------------------------------------------------------------------------------------------

src = "paws"
dest = "temp"
files = os.listdir(src)


try:
    tempfiles = os.makedirs(dest)
except OSError:
    tempfiles = os.listdir(dest)

# trim and replace background with alpha
processFiles(files, src, dest)

tempfiles = os.listdir(dest)

print "This can take a little while..."

#makeMosaic()
im2 = makeTracks()
im2.save("pawTracks.jpg")



# possible references
# info on cropping from here: http://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil
# info on edge detection from here: http://stackoverflow.com/questions/9319767/image-outline-using-python-pil
    




