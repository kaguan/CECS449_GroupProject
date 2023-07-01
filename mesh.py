from skyboxVAO import VAO
from textures import Texture


class Mesh:
    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)

    def destroy(self):
        self.vao.destroy()
        self.texture.destroy()