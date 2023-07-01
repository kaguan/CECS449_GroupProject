from OpenGL.GL import *
import pygame
import pyrr
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

vertices = [
    -1.0, -1.0, 1.0,
    1.0, -1.0, 1.0,
    1.0, -1.0, -1.0,
    -1.0, -1.0, -1.0,
    -1.0, 1.0, 1.0,
    1.0, 1.0, 1.0,
    1.0, 1.0, -1.0,
    -1.0, 1.0, -1.0
]

indices = [
    #right
    1, 2, 6,
    6, 5, 1,
    #left
    0, 4, 7,
    7, 3, 0,
    #top
    4, 5, 6,
    6, 7, 4,
    #bottom
    0, 3, 2,
    2, 1, 0,
    #back
    0, 1, 5,
    5, 4, 0,
    #front
    3, 7, 6,
    6, 2, 3
]
'''
vao, vbo, ebo = GL_UNSIGNED_INT
glGenVertexArrays(1, vao)
glGenBuffers(1, vbo)
glGenBuffers(1, ebo)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), 0)
'''
class skyBox:
    def __init__(self, model):
        self.model = model

    def draw(self,position):
        self.model.draw(position)

    def destroy(self):
        self.model.destroy()

shader3DCubemap = glCreateShader('shaders/vertex_3d_cubemap.txt',
                                 'shaders/fragment_3d_cubemap.txt')

glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_CONSTANT_ALPHA)
projection_transform = pyrr.matrix44.create_perspective_projection(45, SCREEN_WIDTH/SCREEN_HEIGHT, 0.1,
                                                                   10, dtype=np.float32)

glUseProgram(shader3DCubemap)
glUniformMatrix4fv(glGetUniformLocation(shader3DCubemap, 'projection'), 1, GL_FALSE, projection_transform)
glUniform1i(glGetUniformLocation(shader3DCubemap, 'skyBox'), 0)

class CubeMapMaterial:
    def __init__(self):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #load textures
        image = pygame.image.load('cubemap/left.jpg').convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, 0, GL_RGBA8, image_width, image_height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, img_data)

        image = pygame.image.load('cubemap/right.jpg').convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Y, 0, GL_RGBA8, image_width, image_height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, img_data)

        image = pygame.image.load('cubemap/up.jpg').convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_Z, 0, GL_RGBA8, image_width, image_height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, img_data)

        image = pygame.image.load('cubemap/down.jpg').convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_Z, 0, GL_RGBA8, image_width, image_height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, img_data)

        image = pygame.image.load('cubemap/back.jpg').convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_NEGATIVE_X, 0, GL_RGBA8, image_width, image_height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, img_data)

        image = pygame.image.load('cubemap/front.jpg').convert_alpha()
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_CUBE_MAP_POSITIVE_X, 0, GL_RGBA8, image_width, image_height, 0, GL_RGBA8, GL_UNSIGNED_BYTE, img_data)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)

    def destory(self):
        glDeleteTextures(1, (self.texture,))

class CubeMapModel:
    def __init__(self, shader, l, w, h, r, g, b, material):
        self.material = material
        self.shader = shader
        glUseProgram(shader)
        # x, y, z, r, g, b
        self.vertices = (
                -l/2, -w/2, -h/2, r, g, b,
                -l/2,  w/2, -h/2, r, g, b,
                 l/2,  w/2, -h/2, r, g, b,

                 l/2,  w/2, -h/2, r, g, b,
                 l/2, -w/2, -h/2, r, g, b,
                -l/2, -w/2, -h/2, r, g, b,

                 l/2,  w/2,  h/2, r, g, b,
                -l/2,  w/2,  h/2, r, g, b,
                -l/2, -w/2,  h/2, r, g, b,

                -l/2, -w/2,  h/2, r, g, b,
                 l/2, -w/2,  h/2, r, g, b,
                 l/2,  w/2,  h/2, r, g, b,

                -l/2, -w/2,  h/2, r, g, b,
                -l/2,  w/2,  h/2, r, g, b,
                -l/2,  w/2, -h/2, r, g, b,

                -l/2,  w/2, -h/2, r, g, b,
                -l/2, -w/2, -h/2, r, g, b,
                -l/2, -w/2,  h/2, r, g, b,

                 l/2, -w/2, -h/2, r, g, b,
                 l/2,  w/2, -h/2, r, g, b,
                 l/2,  w/2,  h/2, r, g, b,

                 l/2,  w/2,  h/2, r, g, b,
                 l/2, -w/2,  h/2, r, g, b,
                 l/2, -w/2, -h/2, r, g, b,

                 l/2, -w/2,  h/2, r, g, b,
                -l/2, -w/2,  h/2, r, g, b,
                -l/2, -w/2, -h/2, r, g, b,

                -l/2, -w/2, -h/2, r, g, b,
                 l/2, -w/2, -h/2, r, g, b,
                 l/2, -w/2,  h/2, r, g, b,

                 l/2,  w/2, -h/2, r, g, b,
                -l/2,  w/2, -h/2, r, g, b,
                -l/2,  w/2,  h/2, r, g, b,

                -l/2,  w/2,  h/2, r, g, b,
                 l/2,  w/2,  h/2, r, g, b,
                 l/2,  w/2, -h/2, r, g, b
            )
        self.vertex_count = len(self.vertices)//6
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def draw(self, position):
        glUseProgram(self.shader)
        self.material.use()
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
        model_transform = pyrr.matrix44.multiply(model_transform, pyrr.matrix44.create_from_translation(vec=position,dtype=np.float32))
        glUniformMatrix4fv(glGetUniformLocation(self.shader,"model"),1,GL_FALSE,model_transform)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))