import os, sys
import numpy as np
import ctypes
import glfw
import pygame as pg
from glfw.GLFW import *
from OpenGL.GL import *

class Program():
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.gl_init()

    def gl_init(self):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        self.window = glfwCreateWindow(1280, 720, 'buffer test', None, None)
        glfwSetKeyCallback(self.window, self.key_callback)
        self.context = glfw.make_context_current(self.window)

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

        self.vao = 1
        glGenVertexArrays(1, self.vao)
        self.b = 1
        glGenBuffers(1, self.b)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.b)
        glBufferData(GL_ARRAY_BUFFER, 4 * 9, np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0], dtype = np.float32), GL_STATIC_DRAW)
        glVertexAttribPointer(self.location['a_position'], 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0 * 4))
        glEnableVertexAttribArray(self.location['a_position'])
        glViewport(0, 0, 1280, 720)

        self.a = 0.0

    def run(self):
        while not glfw.window_should_close(self.window):
            self.clock.tick
            self.a += 0.01
            glClearColor(1.0, 1.0, 1.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glUseProgram(self.program)
            glEnableVertexAttribArray(self.location['a_position'])
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.b)
            glBufferData(GL_ARRAY_BUFFER, 4 * 9, np.array([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0 - self.a, 0.0], dtype = np.float32), GL_STATIC_DRAW)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            glfwSwapBuffers(self.window)
            glfw.poll_events()
        glfw.terminate()

    def key_callback(self, window, key, scancode, action, mods):
        print(f"key: {key} action: {action}")
        if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
            glfwSetWindowShouldClose(self.window, GLFW_TRUE)

if __name__ == '__main__':
    Program().run()
