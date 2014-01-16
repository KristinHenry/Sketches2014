# by Kristin Henry, 2014 @KristinHenry
# created  Jan 4, 2014
# Generative Art sketch
# quick and dirty experiment: generate random faces
#
# NOTE: I developed this on linux. 
# !!!You may need to modify file path access for your OS.!!!
#

import os
import random
import math

from PIL import Image, ImageChops




# create new image to paste files into
size = (3000, 600)
background = 'white' 
im2 = Image.new("RGBA", size, background)

xmax = im2.size[0]
ymax = im2.size[1]


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
   
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)   
            else:
                break
        for x in reversed(xrange(im.size[0])):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)   
            else:
                break
                
                             


def processFiles(filesToTrim, src, dest):

    imgPath = str(src) + '/' + str(filesToTrim) 
    imgs = os.listdir(imgPath)

    destPath = str(dest) + '/' + str(filesToTrim)
    

    try:
        tempdest = os.makedirs(destPath)
        tempdest = os.listdir(destPath)
    except OSError:
        tempdest = os.listdir(destPath)


    for img in imgs:

        f = str(imgPath) + '/' + str(img)
        im = Image.open(f)

        scaleby = 3 #.5 
        im = im.resize( [int(scaleby * s) for s in im.size] )

        im = trim(im)
        savepath = str(destPath) + '/' + str(img)
        im.save(savepath)



def findPosition(im, imgID):
    # bounding box location for pasting into
    
    buf = 20
    xbuf = buf + im.size[0]
    ybuf = buf + im.size[1]

    xbox = random.randrange(buf, ymax - xbuf, 1)
    ybox = random.randrange(buf, ymax - ybuf, 1)
       
    return (xbox, ybox, imgID)
         
 

def getImg(dest, part, eyeIndex):

    path = str(dest) + '/' + part
    files = os.listdir(path)
    files.sort()

    if part == 'eyeRight':
        i = eyeIndex
    else:
        if len(files) == 1:
            i = 0
        else:
            i = random.randrange(0, (len(files) -1))
    

    file = files[i] 
    im = Image.open(path + "/" + file)

    return (im,i)


def makeFace(dest):
   
    hair = getImg(dest, 'hair', 0)
    eyeLeft = getImg(dest, 'eyeLeft', 0)
    eyeRight = getImg(dest, 'eyeRight', eyeLeft[1])
    nose = getImg(dest, 'nose', 0)
    mouth = getImg(dest, 'mouth', 0)

    return [hair[0], eyeLeft[0], eyeRight[0], nose[0], mouth[0]]


def pasteFacialFeature(im, pos):
    im = im.convert("RGBA")
    whiteToAlphaFast(im)
    #whiteToAlpha(im)
    r, g, b, alpha = im.split()
    im2.paste(im, (pos[0], pos[1]), mask=alpha)


def drawFace(face, pos):
    
    # hair
    im = face[0]
    pasteFacialFeature(im, pos)
    
    # mid positions, based on hair
    face_w = im.size[0]
    face_h = 300 # ToDo: make this dynamic
    minX = pos[0]
    minY = pos[1]
    maxX = pos[0] + face_w
    maxY = pos[1] + face_h
    midX = pos[0] + (maxX - minX)/3 
    midY = pos[1] + (maxY - minY)/4 
    

    # nose
    im = face[3]
    pos = (midX, midY) 
    pasteFacialFeature(im, pos)

    # for positioning mouth
    noseBottom = pos[1] + im.size[1]
    noseWidth = im.size[0]

    # eye left
    im = face[1]
    pos = (midX - im.size[0], midY)
    pasteFacialFeature(im, pos)


    # eye right
    im = face[2]
    pos = (midX + (im.size[0]), midY)
    pasteFacialFeature(im, pos)
       

    # mouth
    im = face[4]
    pos = (midX - (im.size[0]/2), noseBottom)
    pasteFacialFeature(im, pos)
    
    return im2

   

#------------------------------------------------------------------------------------------
print "this may take a while ..."

dest = 'temp'
src = os.listdir('faceImgs')
path = 'faceImgs'

try:
    tempfiles = os.makedirs(dest)
except OSError:
    tempfiles = os.listdir(dest)


# prepare input image files for project
processFiles('eyeLeft', path, dest) 
processFiles('eyeRight', path, dest) 
processFiles('mouth', path, dest) 
processFiles('nose', path, dest)
processFiles('hair', path, dest)

tempfiles = os.listdir(dest)

x = 0
y = 200
for i in range(0,13):
    x += (200 + random.randrange(-4, 4))
    y += random.randrange(-60, 60)
    initpos = (x, y)
    face = makeFace(dest)
    im2 = drawFace(face, initpos)


im2.save("faces.jpg")



# possible references
# info on cropping from here: http://stackoverflow.com/questions/14211340/automatically-cropping-an-image-with-python-pil
# info on edge detection from here: http://stackoverflow.com/questions/9319767/image-outline-using-python-pil
    




