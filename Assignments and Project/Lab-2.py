from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

score = 0

diamondX=250  #x-coordinate
diamondY=600  #y-coordinate
catcherX=250
catcherY=0
diamond_color = [1.0, 1.0, 1.0]  #color= White
animation_running = True



def midPointLine1(X1, Y1, X2, Y2): #Top-Right diagonal 
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    x, y = X1, Y1
    p = 2 * dy - dx #p=dinit

    points = []

    while x <= X2: #till ending point
        points.append((x, y))

        x += 1
        if p < 0: #east pixel=lower pixel selected 
            p += 2 * dy
        else:     #North East pixel=upper pixel
            p += 2 * (dy - dx)
            y -= 1  #decreasing y for top to right diagonal line  

    return points

def midPointLine2(X1, Y1, X2, Y2): #Left-top diagonal
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    x, y = X1, Y1
    p = 2 * dy - dx

    points = []

    while x <= X2: 
        points.append((x, y))

        x += 1
        if p < 0:
            p += 2 * dy
        else:
            p += 2 * (dy - dx)
            y += 1  #decreasing y for top to right diagonal line
    return points
def midPointLineLeftToRight(X1, Y1, X2, Y2):
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    x, y = X1, Y1
    p = 2 * dy - dx

    points = []

    while x <= X2:
        points.append((x, y))

        x += 1
        if p < 0:
            p += 2 * dy
        else:
            p += 2 * (dy - dx)
        #No change in y-coordinate for straight line
    return points

def midPointLineTopToBottom(X1, Y1, X2, Y2):
    dx = abs(X2 - X1)
    dy = abs(Y2 - Y1)
    x, y = X1, Y1
    p = 2 * dx - dy

    points = []

    while y <= Y2: #same just now with y-coordinate condition
        points.append((x, y))

        y += 1
        if p < 0:
            p += 2 * dx
        else:
            p += 2 * (dx - dy)
            x += 1

    return points
def draw(coords): #generating points as the (x,y) coordinate point 
    glBegin(GL_POINTS)
    for x, y in coords:
        glVertex2f(x, y)
    glEnd()

def close_button():
    glutLeaveMainLoop()  #closes opengl window
def stop_button():
    global animation_running
    animation_running = False
def start_button():
    global animation_running
    animation_running = True


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    #Cross
    glColor3f(1.0, 0.0, 0.0)  #color=red
    coords1 = midPointLine1(450, 700,500, 650)
    draw(coords1)
    coords2 = midPointLine2(450, 650, 500, 700)
    draw(coords2)

    #Stop
    glColor3f(1.0, 1.0, 0.0)  # color=Yellow

    coords3 = midPointLineTopToBottom(250, 630,250, 680)
    coords4 = midPointLineTopToBottom(275, 630,275, 680)
    draw(coords3)
    draw(coords4)

    #Arrow
    glColor3f(0.0, 1.0, 1.0)  # color=blue

    coords5 = midPointLineLeftToRight(10, 650,50, 650)
    coords6 = midPointLine1(10, 650,30,580)
    coords7 = midPointLine2(10, 650,30,680)
    draw(coords5)
    draw(coords6)
    draw(coords7)

    

    global diamondY,diamondX,catcherX,catcherY

    #Diamond using the midpoint line algorithm
    global diamond_color
    glColor3f(*diamond_color)
    a=midPointLine2(diamondX, diamondY, diamondX+15, diamondY + 15)
    b=midPointLine1(diamondX+15, diamondY+15,diamondX+30, diamondY)
    c=midPointLine2(diamondX+15, diamondY - 15,diamondX+30, diamondY)
    d=midPointLine1(diamondX, diamondY, diamondX+15, diamondY -15)

    draw(a)
    draw(b)
    draw(c)
    draw(d)
    
    # To make the diamond fall
    global animation_running
    if animation_running==True:
        diamondY -= 1 #decreasing y-coordinate
        if diamondY==0:
            diamondY=600
            diamondX=random.randint(10, 450)
    
    #cather using the midpoint line algorithm
    glColor3f(1.0, 1.0, 1.0)
    e=midPointLineLeftToRight(catcherX, catcherY, catcherX+80, catcherY)
    f=midPointLineLeftToRight(catcherX-20, catcherY+20, catcherX+100, catcherY+20)
    g=midPointLine1(catcherX-20, catcherY+20, catcherX, catcherY)
    h=midPointLine2(catcherX+80, catcherY ,catcherX+100, catcherY+20)

    draw(e)
    draw(f)
    draw(g)
    draw(h)

    glFlush()
    check_collision()
    glutSwapBuffers()

def timer(value):
    glutPostRedisplay()
    glutTimerFunc(5, timer, 0)  

def check_collision():
    global score, diamond_color

    #collision check-> 40 units left and right of the diamonds centre 
    if (diamondX-40 <= catcherX <= diamondX+40) and (diamondY-40<= catcherY <=diamondY+40): 
        score += 1
        diamond_color =  [random.random(), random.random(), random.random()]  

def mouse_callback(button, state, x, y):

    
    #print(f"Mouse Clicked at ({x}, {y})")
    #cross button area
    if 450 <= x <= 500 and 20 <= y <= 60:
        close_button()

    #stop button area
    elif 250 <= x <= 275 and 20 <= y <= 60:
        stop_button()

    #start button area
    elif 10 <= x <= 50 and 20 <= y <= 60:
        start_button()

def special_key_pressed(key, x, y):
    global catcherX,catcherY
    if key == GLUT_KEY_LEFT:
        catcherX=catcherX-20
       
    elif key == GLUT_KEY_RIGHT:
        catcherX=catcherX+20



def reshape(width, height):
    glViewport(0, 0, GLsizei(width), GLsizei(height))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0.0, float(width), 0.0, float(height))
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500,700)
    glutCreateWindow(b"Diamond-catcher")

    glClearColor(0.0, 0.0, 0.0, 0.0)  # Set clear color to black

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutSpecialFunc(special_key_pressed) 
    glutMouseFunc(mouse_callback)
    glutTimerFunc(0, timer, 0)  # Start the timer
    


    glutMainLoop()

if __name__ == "__main__":
    main()