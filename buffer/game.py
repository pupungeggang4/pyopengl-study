import os, sys
import numpy as np
import ctypes
import pygame as pg
from OpenGL.GL import *
import os

class Program():
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.surface = pg.display.set_mode([1280, 720], pg.OPENGL, vsync = 1)
        pg.display.set_caption('buffer test')
        self.clock = pg.time.Clock()
        self.gl_init()

    def gl_init(self):
        f = open('vertex.glsl')
        self.v_shader_source = f.read()
        f.close()
        f = open('fragment.glsl')
        self.f_shader_source = f.read()
        f.close()
        self.v_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.v_shader, self.v_shader_source)
        glCompileShader(self.v_shader)
        self.f_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.f_shader, self.f_shader_source)
        glCompileShader(self.f_shader)
        self.program = glCreateProgram()
        glAttachShader(self.program, self.v_shader)
        glAttachShader(self.program, self.f_shader)
        glLinkProgram(self.program)

        if not glGetShaderiv(self.v_shader, GL_COMPILE_STATUS):
            print(glGetShaderInfoLog(self.v_shader))
        if not glGetShaderiv(self.f_shader, GL_COMPILE_STATUS):
            print(glGetShaderInfoLog(self.f_shader))

        self.location = {}
        self.location['a_position'] = glGetAttribLocation(self.program, 'a_position')
        print(self.location)

        self.vao = 1
        glGenVertexArrays(1, self.vao)
        self.buffer = 1
        glGenBuffers(1, self.buffer)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, 4 * 9, np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0], dtype = np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(self.location['a_position'], 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0 * 4))
        glEnableVertexAttribArray(self.location['a_position'])

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.clock.tick(60)
            glClearColor(1.0, 1.0, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(self.program)
            glEnableVertexAttribArray(self.location['a_position'])
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            pg.display.flip()

if __name__ == '__main__':
    Program().run()