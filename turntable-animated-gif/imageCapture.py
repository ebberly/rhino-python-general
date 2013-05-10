"""
Create an animated gif from a rhino model
written by Mark Wright
wright013@gmail.com

This script requires a companion script called animatedGif.py

It also uses:
RunCPythonScript.py:
    https://github.com/localcode/rhinopythonscripts/blob/master/RunCPythonScript.py
images2gif.py:
    https://code.google.com/p/visvis/source/browse/images2gif.py?spec=svnd82415598349aa47ba3d5b226124fc9b6ba72353&r=d82415598349aa47ba3d5b226124fc9b6ba72353

python 2.7 with numpy and PIL must be installed on the 
system for images2gif.py to run

"""

import rhinoscriptsyntax as rs
import os

externalSoftwareExists = False

if os.path.exists('C:\Python27') == True and os.path.exists("C:\Python27\Lib\site-packages\\" + "numpy")  == True and os.path.exists('C:\Python27\Lib\site-packages\PIL') == True :
    externalSoftwareExists = True
    import RunCPythonScript as rc

def captureAnimatedGif(objectsToCapture,numImg,frameDuration,WIDTH,HEIGHT):
    
    width = str(WIDTH)
    height = str(HEIGHT)
    
    #reset view to default perspective view
    rs.Command("-_Perspective")
    
    #select objects to image
    rs.SelectObjects(objectsToCapture)
    
    #hide everything else
    objsToHide = rs.InvertSelectedObjects()
    rs.HideObjects(objsToHide)
    
    #reselect objects to image
    rs.SelectObjects(objectsToCapture)
    
    #zoom into the objects to image
    rs.ZoomSelected()
    
    #zoom out slightly
    rs.Command("Zoom Out")
    
    #deselect those objects
    rs.UnselectAllObjects()
    
    #determine the rotation angle for each image
    rotateAngle = 360/50
    
    #draw each frame and rotate
    for i in range(numImg):
        
        imgDrop = '"' + fileFolder + "\image" + str(i) + '.png"'
        rs.Command("-_ViewCaptureToFile " + imgDrop + " _Width=" + width + " _Height=" + height + " _Enter")
        rs.RotateView(None,0,rotateAngle)
    
    #designate where to save new gif
    animateScriptPath = scriptPath + "\\animatedGif.py"
    
    #pass off work to external script
    arguments = ['"' + fileFolder + '"',numImg,frameDuration]
    runRtn = rc.run(animateScriptPath, arguments, 'python',False)
    print runRtn
    
    #delete temporary images
    for i in range(50):
        img2Del = fileFolder + "\image" + str(i) + ".png"
        os.remove(img2Del)
    
    #unhide all objects
    rs.ShowObjects(objsToHide)


if __name__ == "__main__":
    
    #Select objects to create image from
    objs = rs.GetObjects("select object to test image capture with")
    
    #locate the script's folder
    scriptPath = os.path.dirname(os.path.realpath(__file__))
    
    #designate an output folder
    fileFolder = rs.BrowseForFolder()
    
    #designate how many images to create / frames in a gif
    numImg = rs.GetInteger("how many frames",50)
    width = rs.GetInteger("how large is the image (width)",800)
    height = rs.GetInteger("how large is the image (height)",800)
    frameDuration = rs.GetReal("how long does each frame last?",.1)
    
    #RUN
    if externalSoftwareExists == True:
        captureAnimatedGif(objs,numImg,frameDuration,width,height)
    else: print "external software error"