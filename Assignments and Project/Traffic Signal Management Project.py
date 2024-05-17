
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import sin, cos, pi
import random
import time


#Raindrop
rainfall=True



#Boat Movement
boatx=100
boaty=100


#Sun Movement
sun_y=0
s_y=0
s_c1,s_c2,s_c3 = 0.0,0.0,0.0
sun = False


# Car Movement
redCarBottom_y = 10
blueCarTop_y = 790
greenCarLeft_x = 10
purpleCarRight_x = 790
light_horizontal = False
light_vertical = False


#day-night Transition
bg_color = (0.0, 0.0, 0.0)  # bg color is black
background_color = [0.0, 0.0, 0.0]
target_color = [0.0, 0.0, 0.0]
black_background = True
white_background = False
transition_duration_black = 5.0
transition_duration_white = 5.0
start_time = 0.0
current_color = [0.0, 0.0, 0.0] #black


#Factory Smoke
circles = [
    {"x": 620, "y": 270, "radius": 12, "color": (0.5, 0.5, 0.5), "visible": False},
    {"x": 650, "y": 272, "radius": 10, "color": (0.5, 0.5, 0.5), "visible": False},
    {"x": 680, "y": 274, "radius": 8, "color": (0.5, 0.5, 0.5), "visible": False},
    {"x": 705, "y": 277, "radius": 7, "color": (0.5, 0.5, 0.5), "visible": False},
]


#Park
balls = [
    {"x": random.uniform(580, 780), "y": random.uniform(520, 630), "radius": random.randint(5, 15),
     "speed": random.uniform(0.5, 2.0), "angle": random.uniform(0, 2 * pi)}
    for _ in range(8)
]


#MidPoint Line Algorithm
def draw(x, y, zone):


    glBegin(GL_POINTS)
    if zone == 0:
        glVertex2f(x, y)
    if zone == 1:
        glVertex2f(y, x)
    if zone == 2:
        glVertex2f(-y, x)
    if zone == 3:
        glVertex2f(-x, y)
    if zone == 4:
        glVertex2f(-x, -y)
    if zone == 5:
        glVertex2f(-y, -x)
    if zone == 6:
        glVertex2f(y, -x)
    if zone == 7:
        glVertex2f(x, -y)


    glEnd()


def findZone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                return x0, y0, x1, y1, 0
            else:
                return x0, -y0, x1, -y0, 7
        else:
            if dy >= 0:
                return -x0, y0, -x1, y1, 3
            else:
                return -x0, -y0, -x1, -y1, 4
    else:
        if dx >= 0:
            if dy >= 0:
                return y0, x0, y1, x1, 1
            else:
                return -y0, x0, -y1, x1, 6
        else:
            if dy >= 0:
                return y0, -x0, y1, -x1, 2
            else:
                return -y0, -x0, -y1, -x1, 5


def draw_line(x0, y0, x1, y1):
    x0, y0, x1, y1, zone = findZone(x0, y0, x1, y1)
    dy = y1 - y0
    dx = x1 - x0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x0
    y = y0
    draw(x, y, zone)
    while x <= x1:
        if d <= 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
        draw(x, y, zone)




#MidPoint Circle Algortihm
def MPCircle(mx, my, r,c1,c2,c3):
    x=0
    y=r
    d = 1-r
    while x<=y:


        if d<0:         #E pixel
            x = x+1
            y = y
            d = d+2*x+3


        else:           #SE Pixel
            x=x+1
            y=y-1
            d=d+2*x-2*y+5
        draw_points(x,y,mx,my,c1,c2,c3)


def draw_points(x, y, mx, my,c1,c2,c3):
    glColor3f(c1, c2, c3)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x+mx, y+my)
    glVertex2f(x+mx, -y+my)
    glVertex2f(-x+mx, y+my)
    glVertex2f(-x+mx, -y+my)
    glVertex2f(y+mx, x+my)
    glVertex2f(y+mx, -x+my)
    glVertex2f(-y+mx, x+my)
    glVertex2f(-y+mx, -x+my)
    glEnd()


#Rain
def draw_raindrop(x, y):
    glColor3f(0.0, 0.0, 1.0)
    draw_line(x, y, x, y+15)


def draw_roads():
    glColor3f(0.5, 0.6, 0.6)
    glPointSize(12)  
    draw_line(300, 0, 300, 800)
    draw_line(500, 0, 500, 800)
    draw_line(0, 300, 800, 300)
    draw_line(0, 500, 800, 500)
    #divider:
    glPointSize(3)
    draw_line(400,0,400,100)
    draw_line(400,150,400,250)
    draw_line(400,320,400,480)
    draw_line(400,550,400,650)
    draw_line(400,700,400,800)


    draw_line(0,400,100,400)
    draw_line(150,400,250,400)
    draw_line(320,400,480,400)
    draw_line(550,400,650,400)
    draw_line(700,400,800,400)
    #crossing
    #right
    glColor3f(0.5, 0.6, 0.6)
    glPointSize(4)
    draw_line(550,300,550,500)
    draw_line(600,300,600,500)


    draw_line(550,340,600,340)
    draw_line(550,380,600,380)
    draw_line(550,420,600,420)
    draw_line(550,460,600,460)
    #left
    glColor3f(0.5, 0.6, 0.6)
    glPointSize(4)
    draw_line(250,300,250,500)
    draw_line(200,300,200,500)


    draw_line(250,340,200,340)
    draw_line(250,380,200,380)
    draw_line(250,420,200,420)
    draw_line(250,460,200,460)
    #top
    glColor3f(0.5, 0.6, 0.6)
    glPointSize(4)
    draw_line(300,550,500,550)
    draw_line(300,600,500,600)


    draw_line(340,550,340,600)
    draw_line(380,550,380,600)
    draw_line(420,550,420,600)
    draw_line(460,550,460,600)


    #bottom
    glColor3f(0.5, 0.6, 0.6)
    glPointSize(4)
    draw_line(300,250,500,250)
    draw_line(300,200,500,200)


    draw_line(340,250,340,200)
    draw_line(380,250,380,200)
    draw_line(420,250,420,200)
    draw_line(460,250,460,200)




def draw_boat():
    global boatx, boaty
    glColor3f(0.6, 0.0, 0.0)  # red color for boat
    glPointSize(5)


    draw_line(boatx-80, boaty+50, boatx, boaty+50) #20,150->100,150
    draw_line(boatx-100, boaty+80, boatx+20, boaty+80) #0,180->120,180
    draw_line(boatx-100, boaty+80, boatx-80, boaty+50)
    draw_line(boatx, boaty+50, boatx+20, boaty+80)
    draw_line(boatx-60, boaty+105, boatx-20, boaty+105) #40,205->80,205
    draw_line(boatx-60, boaty+105, boatx-80, boaty+80)
    draw_line(boatx-20, boaty+105, boatx, boaty+80)
   
    #Waves
    glColor3f(0.0, 1.0, 1.0)
  


    wave_positions = [
        [0, 100, 50, 100],
        [130,5,180,5],
        [50, 125, 100, 125],
        [150, 80, 200, 80],
        [200, 100, 250, 100],
        [0,250,50,250],
        [50,225,100,225],
        [110,210,160,210],
        [85,10,135,10],
        [130,280,180,280]
        ]


    for wave in wave_positions:
        start_x = (wave[0] + boatx) % 300  #300 back to 0
        end_x = (wave[2] + boatx) % 300  


        if start_x <= end_x:
            draw_line(start_x, wave[1], end_x, wave[3])
        else: #when wave hits the 300 boundary
            draw_line(0, 0, 0, 0)  


def city():
   
    #Building-1
    glColor3f(1.0, 1.0, 0.0)  #Yellow
    draw_line(10,550,10,650)
    draw_line(10,650,100,650)
    draw_line(100,550,100,650)


    draw_line(10,650,55,700)
    draw_line(100,650,55,700)


    draw_line(40,550,40,620)
    draw_line(40,620,65,620)
    draw_line(65,550,65,620)


    draw_line(10,550,100,550)


    #Building-2
    glColor3f(1.0, 0.0, 1.0)
    glPointSize(5)
    draw_line(120,550,120,700)
    draw_line(120,700,200,700)
    draw_line(200,550,200,700)
    draw_line(120,625,200,625)
    draw_line(120,550,200,550)


    draw_line(140,575,140,600)
    draw_line(170,575,170,600)
    draw_line(140,575,170,575)
    draw_line(140,600,170,600)


    draw_line(140,640,140,665)
    draw_line(170,640,170,665)
    draw_line(140,640,170,640)
    draw_line(140,665,170,665)
   
    #Building-3


    glColor3f(0.0, 1.0, 0.0)  
    draw_line(210,550,210,650)
    draw_line(210,650,290,650)
    draw_line(290,550,290,650)
    draw_line(210,550,290,550)


    draw_line(210,650,250,700)
    draw_line(290,650,250,700)


    draw_line(240,550,240,600)
    draw_line(240,600,265,600)
    draw_line(265,550,265,600)


    #sun
    glPointSize(10)
    MPCircle(150,sun_y+600,20,s_c1,s_c2,s_c3) #s_c1,s_c2,s_c3 = 1.0,0.9,0.0
    draw_line(170,s_y+630,180,s_y+650)
    draw_line(150,s_y+630,150,s_y+650)
    draw_line(130,s_y+630,120,s_y+650)
   
# Cars On the Road:
def draw_red_car_bottom():
    global redCarBottom_y
    glColor3f(0.8, 0.0, 0.2)
    glPointSize(3)
    #outer box
    draw_line(330,redCarBottom_y,330,redCarBottom_y+50)
    draw_line(370,redCarBottom_y,370,redCarBottom_y+50)
    draw_line(330,redCarBottom_y,370,redCarBottom_y)
    draw_line(330,redCarBottom_y+50,370,redCarBottom_y+50)


    #inner box
    draw_line(340,redCarBottom_y+10,340,redCarBottom_y+40)
    draw_line(360,redCarBottom_y+10,360,redCarBottom_y+40)
    draw_line(340,redCarBottom_y+10,360,redCarBottom_y+10)
    draw_line(340,redCarBottom_y+40,360,redCarBottom_y+40)


    #outer box+inner box connection
    draw_line(330,redCarBottom_y,340,redCarBottom_y+10)
    draw_line(370,redCarBottom_y,360,redCarBottom_y+10)
    draw_line(340,redCarBottom_y+40,330,redCarBottom_y+50)
    draw_line(370,redCarBottom_y+50,360,redCarBottom_y+40)


    #Front part
    draw_line(330,redCarBottom_y+50,340,redCarBottom_y+60)
    draw_line(370,redCarBottom_y+50,360,redCarBottom_y+60)
    draw_line(340,redCarBottom_y+60,360,redCarBottom_y+60)




def draw_blue_car_top():
    global blueCarTop_y
    glColor3f(0.3, 0.0, 1.0)
    glPointSize(3)
    #outer box
    draw_line(430,blueCarTop_y,430,blueCarTop_y-50)
    draw_line(470,blueCarTop_y,470,blueCarTop_y-50)
    draw_line(430,blueCarTop_y,470,blueCarTop_y)
    draw_line(430,blueCarTop_y-50,470,blueCarTop_y-50)
   
    #inner box
    draw_line(440,blueCarTop_y-10,440,blueCarTop_y-40)
    draw_line(460,blueCarTop_y-10,460,blueCarTop_y-40)
    draw_line(440,blueCarTop_y-10,460,blueCarTop_y-10)
    draw_line(440,blueCarTop_y-40,460,blueCarTop_y-40)


    #outer box+inner box connection
    draw_line(440,blueCarTop_y-10,430,blueCarTop_y)
    draw_line(430,blueCarTop_y-50,440,blueCarTop_y-40)
    draw_line(470,blueCarTop_y,460,blueCarTop_y-10)
    draw_line(470,blueCarTop_y-50,460,blueCarTop_y-40)


    #Front part
    draw_line(440, blueCarTop_y-60,430,blueCarTop_y-50)
    draw_line(470,blueCarTop_y-50,460,blueCarTop_y-60)
    draw_line(440, blueCarTop_y-60,460,blueCarTop_y-60)




def draw_green_car_left():
    global greenCarLeft_x
    glColor3f(0.0,1.0,0.0)
    glPointSize(3)
    #outer box
    draw_line(greenCarLeft_x,330,greenCarLeft_x+50,330)
    draw_line(greenCarLeft_x,370,greenCarLeft_x+50,370)
    draw_line(greenCarLeft_x,330,greenCarLeft_x,370)
    draw_line(greenCarLeft_x+50,330,greenCarLeft_x+50,370)
    #inner box
    draw_line(greenCarLeft_x+10,340,greenCarLeft_x+40,340)
    draw_line(greenCarLeft_x+10,360,greenCarLeft_x+40,360)
    draw_line(greenCarLeft_x+10,340,greenCarLeft_x+10,360)
    draw_line(greenCarLeft_x+40,340,greenCarLeft_x+40,360)


    #outer box+inner box connection
    draw_line(greenCarLeft_x,330,greenCarLeft_x+10,340)
    draw_line(greenCarLeft_x+10,360,greenCarLeft_x,370)
    draw_line(greenCarLeft_x+50,330,greenCarLeft_x+40,340)
    draw_line(greenCarLeft_x+50,370,greenCarLeft_x+40,360)


    #Front part
    draw_line(greenCarLeft_x+50,330,greenCarLeft_x+60,340)
    draw_line(greenCarLeft_x+60,360,greenCarLeft_x+50,370)
    draw_line(greenCarLeft_x+60,340,greenCarLeft_x+60,360)




def draw_purple_car_right():
    global purpleCarRight_x
    glColor3f(0.5, 0.0, 0.8)
    glPointSize(3)
    #outer box
    draw_line(purpleCarRight_x,430,purpleCarRight_x-50,430)
    draw_line(purpleCarRight_x,470,purpleCarRight_x-50,470)
    draw_line(purpleCarRight_x,430,purpleCarRight_x,470)
    draw_line(purpleCarRight_x-50,430,purpleCarRight_x-50,470)


    #inner box
    draw_line(purpleCarRight_x-40,440,purpleCarRight_x-10,440)
    draw_line(purpleCarRight_x-10,460,purpleCarRight_x-40,460)
    draw_line(purpleCarRight_x-10,440,purpleCarRight_x-10,460)
    draw_line(purpleCarRight_x-40,440,purpleCarRight_x-40,460)


    #outer box+inner box connection
    draw_line(purpleCarRight_x,430,purpleCarRight_x-10,440)
    draw_line(purpleCarRight_x-50,430,purpleCarRight_x-40,440)
    draw_line(purpleCarRight_x,470,purpleCarRight_x-10,460)
    draw_line(purpleCarRight_x-40,460,purpleCarRight_x-50,470)


    #Front part
    draw_line(purpleCarRight_x-50,430,purpleCarRight_x-60,440)
    draw_line(purpleCarRight_x-60,460,purpleCarRight_x-50,470)
    draw_line(purpleCarRight_x-60,440,purpleCarRight_x-60,460)


def car_movement():
    global redCarBottom_y,blueCarTop_y,greenCarLeft_x,purpleCarRight_x


    #red car
    if 200<redCarBottom_y<300:
        if light_vertical:
            redCarBottom_y = redCarBottom_y
        else:
            redCarBottom_y+=2
    else:
        redCarBottom_y+=2
    if redCarBottom_y == 790:
        redCarBottom_y = 10


    #blue car
    if 500<blueCarTop_y<600:
        if light_vertical:
            blueCarTop_y = blueCarTop_y
        else:
            blueCarTop_y-=2
    else:
        blueCarTop_y -= 2
    if blueCarTop_y == 10:
        blueCarTop_y = 790


    #green car
    if 200<greenCarLeft_x<300:
        if light_horizontal:
            greenCarLeft_x = greenCarLeft_x
        else:
            greenCarLeft_x+=2
    else:
        greenCarLeft_x += 2
    if greenCarLeft_x == 790:
        greenCarLeft_x = 10


    #puple car
    if 500<purpleCarRight_x<600:
        if light_horizontal:
            purpleCarRight_x = purpleCarRight_x
        else:
            purpleCarRight_x -= 2
    else:
        purpleCarRight_x -= 2      
    if purpleCarRight_x == 10:
        purpleCarRight_x = 790




#Traffic Light System:
def traffic_light():
    #outerbox_Horizontal
    glColor3f(0.0, 1.0, 1.0)
    glPointSize(2)
    draw_line(330,410,330,490)
    draw_line(330,410,370,410)
    draw_line(330,490,370,490)
    draw_line(370,410,370,490)


    glPointSize(4)
    draw_line(350,490,350,520)
    draw_line(350,520,290,520)


    #outerbox_Vertical
    glColor3f(0.0, 1.0, 1.0)
    glPointSize(2)
    draw_line(410,330,490,330)
    draw_line(410,330,410,370)
    draw_line(410,370,490,370)
    draw_line(490,370,490,330)
    glPointSize(4)
    draw_line(490,350,520,350)
    draw_line(520,350,520,290)


    if light_horizontal == True:
        MPCircle(350,475,10,1.0, 0.0, 0.0) #redLight
        MPCircle(350,450, 10, 1.0,1.0,0.0)
        MPCircle(475, 350, 10, 0.0,1.0,0.0)
   
    if light_vertical == True:
        MPCircle(425, 350, 10, 1.0, 0.0, 0.0)
        MPCircle(450,350,10,1.0,1.0,0.0)
        MPCircle(350,425,10,0.0,1.0,0.0)


def traffic_light_movement(x,y):
    global  light_vertical, light_horizontal
   
    if (300< x <400) and (300< y <500):
        light_vertical=False
        light_horizontal = True
       
    if (400< x <500) and (300< y <500):
        light_horizontal = False
        light_vertical = True
    glutPostRedisplay()




#Background Color Day-Night:
def change_bg_color(color):
    global bg_color
    bg_color = color
    glClearColor(*color, 1.0) #4th- alpha value for solid color
    glutPostRedisplay()


def transition_to_white():
    global black_background, white_background, start_time, transition_duration_white,sun,target_color


    if not white_background:
        black_background = False
        white_background = True
        sun = True
        start_time = time.time()
        transition_duration_white = 5.0
        target_color = [1.0, 1.0, 1.0]


def transition_to_black():
   global black_background, white_background, start_time, transition_duration_black,sun,target_color


   if not black_background:
        white_background = False
        black_background = True
        sun = False
        start_time = time.time()
        transition_duration_black = 5.0
        target_color = [0.0, 0.0, 0.0]


def update_background_color():
    global sun_y,s_y,s_c1,s_c2,s_c3, start_time, current_color, black_background, white_background, transition_duration_black, transition_duration_white


    current_time = time.time()
    elapsed_time = current_time - start_time


    if white_background and elapsed_time < transition_duration_white:
        t = elapsed_time / transition_duration_white
        current_color = [t, t, t]
        sun_y += 2
        s_y +=2
        if sun_y+600>650:
            s_c1,s_c2,s_c3 = 1.0,0.9,0.0
        else:
            s_c1,s_c2,s_c3 = 0.0,0.0,0.0
        if sun_y+600==790:
            sun_y = 0
            s_y=0
    elif black_background and elapsed_time < transition_duration_black:
        t = elapsed_time / transition_duration_black
        current_color = [1.0 - t, 1.0 - t, 1.0 - t]
        sun_y -= 2
        s_y-=2
        if sun_y+600>650:
            s_c1,s_c2,s_c3 = 1.0,0.9,0.0
        else:
            s_c1,s_c2,s_c3 = 0.0,0.0,0.0
        if sun_y + 600 == 600:
            sun_y = 0
            s_y=0


    glClearColor(current_color[0], current_color[1], current_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glutPostRedisplay()




#Rain Effect:


def rain():
    for raindrop in raindrops:
        draw_raindrop(raindrop[0], raindrop[1])


raindrops = []


def animate_raindrops(value):
    global rain_direction
    for i in range(len(raindrops)):
        raindrops[i][1] -= 5  #raindrop speed, y-coordinate
        if raindrops[i][1] < 0:
            raindrops[i][1] = 800 + random.randint(10, 100) #resetting the raindrop position
            raindrops[i][0] = random.randint(0, 800)
    glutPostRedisplay()
    glutTimerFunc(10, animate_raindrops, 0) #timer for continuous animation




#Factory Functionalities:
def draw_factory():
    glColor3f(1.0, 0.0, 0.5)
    draw_line(510,0,510,160)
    draw_line(510,160,620,160)
    draw_line(620,160,620,0)


    draw_line(525, 20, 525, 80)
    draw_line(545, 20, 545, 80)
    draw_line(565, 20, 565, 80)
    draw_line(525,80, 565,80)


    draw_line(520, 140, 555, 140)
    draw_line(575, 140, 610, 140)
    draw_line(520, 110, 555, 110)
    draw_line(575, 110, 610, 110)


    draw_line(520,140,520,110)
    draw_line(555,140,555,110)
    draw_line(575,140,575,110)
    draw_line(610,140,610,110)


    draw_line(620,130,790,130)
    draw_line(790,130,790,0)


    draw_line(633,110,671,110)
    draw_line(686,110,728,110)
    draw_line(739,110,781,110)
    draw_line(633,50,671,50)
    draw_line(686,50,728,50)
    draw_line(739,50,781,50)
    draw_line(633,110,633,50)
    draw_line(686,110,686,50)
    draw_line(739,110,739,50)
    draw_line(671,110,671,50)
    draw_line(728,110,728,50)
    draw_line(781,110,781,50)


    glColor3f(1.0, 0.0, 0.0)


    draw_line(600,250,640,250)
    draw_line(600,250,600,160)
    draw_line(640,250,640,130)


    draw_line(660,220,770,220)
    draw_line(660,220,660,130)
    draw_line(770,220,770,130)
    draw_line(670, 210, 760, 210)  # Top side
    draw_line(670, 210, 670, 140)  # Left side
    draw_line(760, 210, 760, 140)  # Right side
    draw_line(670, 140, 760, 140)  # Bottom side




    for circle in circles:
        if circle["visible"]:
            MPCircle(circle["x"], circle["y"], circle["radius"], *circle["color"])




def animate_circles(value):
    global circles


    # Make all circles invisible
    for circle in circles:
        circle["visible"] = False


    # Make circles visible one by one until the fourth circle
    for i in range(value + 1):
        circles[i]["visible"] = True


    glutPostRedisplay()


    # Start the animation loop again after a delay
    glutTimerFunc(1000, animate_circles, (value + 1) % len(circles) if value < len(circles) - 1 else 0)




#Park Functonalities:


def draw_park():
    glColor3f(0.0, 1.0, 0.0)
    draw_line(500,650,800,650)
    glColor3f(0.545, 0.271, 0.075)
    draw_line(575,650,575,720)
    draw_line(650,650,650,720)
    draw_line(725,650,725,720)
    glColor3f(0.0, 1.0, 0.0)
    #tree 1
    draw_line(545,690,605,690)
    draw_line(545,690,565,720)
    draw_line(605,690,585,720)
    draw_line(565,720,545,720)
    draw_line(545,720,575,750)
    draw_line(585,720,605,720)
    draw_line(605,720,575,750)


    #tree 2
    draw_line(620,690,680,690)
    draw_line(620,690,640,720)
    draw_line(680,690,660,720)
    draw_line(620,720,640,720)
    draw_line(620,720,650,750)
    draw_line(680,720,660,720)
    draw_line(680,720,650,750)


    #tree 3
    draw_line(695,690,755,690)
    draw_line(695,690,715,720)
    draw_line(715,720,695,720)
    draw_line(695,720,725,750)
    draw_line(755,690,735,720)
    draw_line(755,720,735,720)
    draw_line(755,720,725,750)
def draw_boy():
    # Head
    glColor3f(1.0, 0.8, 0.6)  # Skin color
    MPCircle(550, 600, 10, 0.0, 0.0, 0.5)
    # Body
    draw_line(550, 590, 550, 550)
    # Arms
    draw_line(535, 575, 565, 575)
    # Legs
    draw_line(550,550,530,535)
    draw_line(570,535,550,550)
    #stick
    glColor3f(1.0, 0.0, 0.0)  # Set color to red
    draw_line(565,580,565,565)
    MPCircle(565,585,5,1.0, 0.0, 0.0)


def draw_ball(x, y, radius):
    MPCircle(x, y, radius, 1.0, 0.0, 0.0)


def animate_balls(value):
    for ball in balls:
        ball["x"] += ball["speed"] * cos(ball["angle"])
        ball["y"] += ball["speed"] * sin(ball["angle"])


        # Check if the ball is out of bounds, and if so, reset its position
        if ball["x"] > 780 or ball["x"] < 580 or ball["y"] > 630 or ball["y"] < 520:
            ball["x"] = random.uniform(580, 780)
            ball["y"] = random.uniform(520, 630)


    glutPostRedisplay()
    glutTimerFunc(10, animate_balls, 0)






def cross():
    glColor3f(1.0, 0.0, 0.0)
    draw_line(760,800,800,750)
    draw_line(760,750,800,800)
def terminate_game():
    glutLeaveMainLoop()




def keyboard(key, x, y):
    global rainfall, sun
    if key == b'R' or key == b'r':
        rainfall=not rainfall
    elif key == b't':
        if black_background:
            transition_to_white()
            sun = True
        else:
            transition_to_black()
            sun= False


def mouseListener(button, state, x, y): #/#/x, y is the x-y of the screen (2D)
    global light_vertical, light_horizontal
    if button==GLUT_RIGHT_BUTTON:
        if(state == GLUT_DOWN):    #        // 2 times?? in ONE click? -- solution is checking DOWN or UP
            if 760 <= x <= 800 and 0 <= y <= 50:
               terminate_game()
            else:
                traffic_light_movement(x,y)


    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    update_background_color()
    draw_park()
    draw_factory()
    draw_boy()
    cross()
    draw_roads()
    draw_boat()
    draw_red_car_bottom()
    draw_blue_car_top()
    draw_green_car_left()
    draw_purple_car_right()
    traffic_light()
    city()
    if not rainfall:
        rain()
    for ball in balls:
        draw_ball(ball["x"], ball["y"], ball["radius"])




    glFlush()


def animate(value):
    global boatx, boaty,redCarBottom_y,blueCarTop_y,greenCarLeft_x,purpleCarRight_x,sun_y


    # increase x-coordinate for boat movement
    boatx += 1
    if boatx == 280:  
        boatx = 0
    #carMovement
    car_movement()
    glutPostRedisplay()  


    # Set the next frame update using timer (e.g., every 10 milliseconds)
    glutTimerFunc(10, animate, 0)
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
    glutInitWindowSize(800,800)
    glutCreateWindow(b"Project")


    glClearColor(0.0, 0.0, 0.0, 0.0)  # Set clear color to black


    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutTimerFunc(10, animate, 0)  # Start the animation timer
    glutTimerFunc(1000, animate_circles, 0)
    glutTimerFunc(10, animate_balls, 0)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouseListener)


    for i in range(100):
        x = random.randint(0, 600)
        y = random.randint(0, 600)
        raindrops.append([x, y])
    glutTimerFunc(10, animate_raindrops, 0)
   




    glutMainLoop()


if __name__ == "__main__":
    main()


























