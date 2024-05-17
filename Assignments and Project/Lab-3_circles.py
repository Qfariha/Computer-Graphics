from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window_width, window_height = 500, 500
circles = [] 
initial_radius = 50  
growth_rate=.01
paused= False

def draw_circle(x_centre, y_centre, radius):
    x, y = 0, radius
    d = 1 - radius

    glBegin(GL_POINTS)
    while x <= y:
        
        glVertex2f(x + x_centre, y + y_centre)
        glVertex2f(-x + x_centre, y + y_centre)
        glVertex2f(x + x_centre, -y + y_centre)
        glVertex2f(-x + x_centre, -y +y_centre)
        glVertex2f(y + x_centre, x + y_centre)
        glVertex2f(-y + x_centre, x + y_centre)
        glVertex2f(y + x_centre, -x + y_centre)
        glVertex2f(-y + x_centre, -x + y_centre)

        if d < 0:  
            d += 2 * x + 3
        else:    
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()
    glFlush()

def draw():
    global paused,growth_rate
    if not paused:
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1.0, 0.0, 0.0) 

        to_remove = []
        for i in range(len(circles)):
            center_x, center_y, radius = circles[i]
            radius += growth_rate  
            circles[i] = (center_x, center_y, radius)  
            draw_circle(center_x, center_y, radius)  
            #Boundary checking
            x_min, x_max = radius, window_width - radius 
            y_min, y_max = radius, window_height - radius
            if not (x_min < center_x < x_max and y_min < center_y < y_max):
                to_remove.append(i) 

        for idx in (to_remove):
            del circles[idx]

        glutSwapBuffers()
        glutPostRedisplay()  

def keyboard(key, x, y):
    global paused,growth_rate
    if key == b' ':
        paused = not paused 
    elif key == GLUT_KEY_LEFT: 
        growth_rate += 0.01  
    elif key == GLUT_KEY_RIGHT:  
        growth_rate -= 0.01  
        growth_rate = max(growth_rate, 0.01)  

def special_keys(key, x, y):
    if key == GLUT_KEY_LEFT:
        keyboard(key, x, y)
    elif key == GLUT_KEY_RIGHT:
        keyboard(key, x, y)


def mouse_click(button, state, x, y):
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        
        center_x = x
        center_y = window_height - y 
        circles.append((center_x, center_y, initial_radius))  
        glutPostRedisplay() 

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Circle")

    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0.0, window_width, 0.0, window_height)

    glutDisplayFunc(draw)
    glutMouseFunc(mouse_click) 
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(draw)  
    glutMainLoop()

if __name__ == "__main__":
    main()