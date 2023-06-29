from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from PIL import Image

def loadSkyBox():
    #up
    im1 = Image.open("file.jpg").rotate(180).transpose(Image.FLIP_LEFT_RIGHT).resize((512,512))
    texture1 = im1.tostring()
    #down
    im2 = Image.open("file.jpg").rotate(180).transpose(Image.FLIP_LEFT_RIGHT).resize((512,512))
    texture2 = im2.tostring()
    #left
    im3 = Image.open("file.jpg").rotate(180).resize((512,512))
    texture3 = im3.tostring()
    #right
    im4 = Image.open("file.jpg").rotate(180).transpose(Image.FLIP_LEFT_RIGHT).resize((512,512))
    texture4 = im4.tostring()
    #forward
    im5 = Image.open("file.jpg").rotate(180).transpose(Image.FLIP_LEFT_RIGHT).resize((512,512))
    texture5 = im5.tostring()
    #back
    im6 = Image.open("file.jpg").rotate(180).resize((512,512))
    texture6 = im6.tostring()

    glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, 1)