'''
Created on Jan 2, 2014

@author: Kristin
'''

import os
import random
import math

from PIL import Image, ImageChops


col = 3000
row = 3000
background = "white" # "black"
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
        
    

def findPosition(im, imgID):
    # bounding box location for pasting into
    buf = 20
    xbuf = buf + im.size[0]
    ybuf = buf + im.size[1]

    xbox = random.randrange(buf, ymax - xbuf, 1)
    ybox = random.randrange(buf, ymax - ybuf, 1)
    
    return (xbox, ybox, imgID)
         
    


def makeMosaic():
    box = None
    last = None

    boxes = []

    a = 0
    mx = 500
    while a < mx:
        # print a
        a += 1

        i = random.randint(0, len(tempfiles)-1)
        
        im = Image.open(dest + "/" + tempfiles[i])
        im = im.convert("RGBA")
        whiteToAlphaFast(im)
        r, g, b, alpha = im.split()
        
        box = findPosition(im, i)
        boxes.append(box)
        

        

    # sorting, so that trees lower in the image are drawn last
    boxes.sort(key=lambda tup: tup[1])

    a = 0
    while a < mx:
        box = boxes[a]

        im = Image.open(dest + "/" + tempfiles[box[2]])
        im = im.convert("RGBA")
        whiteToAlphaFast(im)
        r, g, b, alpha = im.split()

        box = (box[0], box[1])
        im2.paste(im, box, mask=alpha)

        a += 1
        
    return im2

    
        

#------------------------------------------------------------------------------------------

src = "treeImgs"
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
im2 = makeMosaic()
im2.save("happyTrees.jpg")



# possible references
# info on cropping from here: http://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil
# info on edge detection from here: http://stackoverflow.com/questions/9319767/image-outline-using-python-pil
    




