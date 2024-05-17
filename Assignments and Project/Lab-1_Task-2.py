from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

W_Width, W_Height = 500, 500

ballx = bally = 0
speed = 0.01
ball_size = 3

balls = [(-50, -50, (0, 0, 0)), (50, 50, (0, 0, 0)), (0, 0, (0, 0, 0)),
         (30, -30, (0, 0, 0)), (-30, 30, (0, 0, 0)), (20, 20, (0, 0, 0))]



class point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

def crossProduct(a, b):
    result = point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x
    return result

def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y 
    return a, b

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def keyboardListener(key, x, y):
    global ball_size
    if key == b'w':
        ball_size += 1
        print("Size Increased")
    if key == b's':
        ball_size -= 1
        print("Size Decreased")
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    if key == GLUT_KEY_DOWN:
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global ballx, bally, original_colors,balls

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        c_X, c_y = convert_coordinate(x, y)
        ballx, bally = c_X, c_y

        balls = [(-50, -50, (1, 0, 0)), (50, 50, (0, 1, 0)), (0, 0, (0, 0, 1)),
         (30, -30, (1, 1, 0)), (-30, 30, (0, 1, 1)), (20, 20, (1, 0, 1))]
        
        original_colors = [ball[2] for ball in balls]


    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        for i in range(len(balls)):
            balls[i] = (balls[i][0], balls[i][1], (0, 0, 0)) #black

        glutTimerFunc(1000, reset_color, 0) #color reset after 1 seconds 

def reset_color(value):
    global balls, original_colors
    for i in range(len(balls)):
        balls[i] = (balls[i][0], balls[i][1], original_colors[i])  # Reset to original color

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    global ball_size

    for x, y, color in balls:
        glColor3f(*color)
        draw_points(x, y, ball_size)

    glutSwapBuffers()

def animate(value):
    global balls, speed, W_Width

    for i in range(len(balls)):
        balls[i] = (balls[i][0] + speed, balls[i][1]+speed, balls[i][2]) #movement of balls

    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutTimerFunc(0, animate, 0)

glutMainLoop()