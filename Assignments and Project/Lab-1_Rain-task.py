#Task-1

from OpenGL.GL import *
from OpenGL.GLUT import *
import random

rain_direction = 0
bg_color = (0.0, 0.0, 0.0)  # bg color is black

def init():
    glClearColor(*bg_color, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 600, 0, 600, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_raindrop(x, y): #just like draw_lines
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 1.0) #red,green,blue
    glVertex2f(x, y)
    glVertex2f(x, y+15)  # raindrop length
    glEnd()

def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    #glVertex2f(100,100)
    glEnd()

def draw_lines(x1,y1,x2,y2):
    glPointSize(2)
    glLineWidth(5)
    glBegin(GL_LINES)
    glVertex2f(x1,y1) 
    glVertex2f(x2,y2)

    glEnd()

raindrops = []

def animate_raindrops(value):
    global rain_direction
    for i in range(len(raindrops)):
        raindrops[i][1] -= 2  #raindrop speed, y-coordinate
        raindrops[i][0] += rain_direction * 0.3  #x-coordinate(left/right) based on rain direction
        if raindrops[i][1] < 0: 
            raindrops[i][1] = 600 + random.randint(10, 100) #resetting the raindrop position => 615,620,..random
            raindrops[i][0] = random.randint(0, 600)
    glutPostRedisplay() 
    glutTimerFunc(10, animate_raindrops, 0) #timer for continuous animation

#Day-Night effect
def change_bg_color(color):
    global bg_color
    bg_color = color
    glClearColor(*color, 1.0) #4th- alpha value for solid color
    glutPostRedisplay()

def keyboard(key, x, y):
    if key == b'B' or key == b'b':  #b=byte 
        change_bg_color((0.0, 0.0, 0.0))  #black
    elif key == b'W' or key == b'w':
        change_bg_color((1.0, 1.0, 1.0))  #white

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    
    

    #top triangle of house
    draw_lines(150,250,300,450)
    draw_lines(300,450,450,250)
    draw_lines(150,250,450,250)
    
    #rechtangle
    draw_lines(180,250,180,100)
    draw_lines(430,250,430,100)
    draw_lines(180,100,430,100)
    
    #door
    draw_lines(200,100,200,150)
    draw_lines(200,150,250,150)
    draw_lines(250,150,250,100)

    draw_points(230, 130)

    draw_lines(350,180,370,180)
    draw_lines(370,180,390,180)
    draw_lines(350,180,350,200)
    draw_lines(350,200,350,220)
    draw_lines(350,220,370,220)
    draw_lines(370,220,390,220)
    draw_lines(390,220,390,200)
    draw_lines(390,200,390,180)
    draw_lines(370,180,370,220)
    draw_lines(350,200,390,200)

    for raindrop in raindrops:
        draw_raindrop(raindrop[0], raindrop[1])
    glutSwapBuffers()

# New function to handle special key presses
def special_key_pressed(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction = -15
    elif key == GLUT_KEY_RIGHT:
        rain_direction = 15

def special_key_released(key, x, y):
    global rain_direction
    if key in (GLUT_KEY_LEFT, GLUT_KEY_RIGHT):
        rain_direction = 0  #when left or right key is not pressed

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Rain Simulation")
    glutDisplayFunc(display)
    glutSpecialFunc(special_key_pressed)  
    glutSpecialUpFunc(special_key_released)  
    init()

    glutKeyboardFunc(keyboard)
    
    for i in range(100):
        x = random.randint(0, 600)
        y = random.randint(0, 600)
        raindrops.append([x, y])
    glutTimerFunc(10, animate_raindrops, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()