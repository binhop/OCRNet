import os
import cv2

wSize, hSize = 100, 100
charSize = (64, 64)

marginX = 10
marginY = 10

saveDir = "dataClean/train/"
dir = "data/train/"
for f in os.listdir(dir):
    img = cv2.imread(dir + f, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
    
        if w == wSize and h == hSize or h < 20:
            continue
        
        newXl = x - marginX
        if newXl < 0:
            newXl = 0
        newYr = y + h+ marginY
        if newYr > hSize:
            newYr = 100
        newXr = x + w + marginX
        if newXr > wSize:
            newXr = 100
        img = img[y: newYr, newXl : newXr]

        img = cv2.resize(img, charSize)
        cv2.imwrite(saveDir + f, img)

        break

saveDir = "dataClean/test/"
dir = "data/test/"
for f in os.listdir(dir):
    img = cv2.imread(dir + f, cv2.IMREAD_GRAYSCALE)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
    
        if w == wSize and h == hSize or h < 20:
            continue
        
        newXl = x - marginX
        if newXl < 0:
            newXl = 0
        newYr = y + h+ marginY
        if newYr > hSize:
            newYr = 100
        newXr = x + w + marginX
        if newXr > wSize:
            newXr = 100
        img = img[y: newYr, newXl : newXr]

        img = cv2.resize(img, charSize)
        cv2.imwrite(saveDir + f, img)

        break