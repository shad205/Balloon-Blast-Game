from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time


width, height = 800, 600
score = 0
start_time = 0
bubble_speed = 0.1
pointer_x, pointer_y = width // 2, height // 2
pointer_size = 20
max_bubbles = 7
bubbles = []
game_active = False

class Bubble:
    def __init__(self, color):
        self.x = random.randint(pointer_size, width - pointer_size)
        self.y = height + pointer_size
        self.radius = 20
        self.color = color

def draw_circle(x, y, radius, color):
    num_segments = 100
    glBegin(GL_TRIANGLE_FAN)
    glColor3fv(color)
    for i in range(num_segments):
        theta = 2.0 * math.pi * i / num_segments
        dx = radius * math.cos(theta)
        dy = radius * math.sin(theta)
        glVertex2f(x + dx, y + dy)
    glEnd()

def draw_pointer(x, y):
    glColor3f(1.0, 1.0, 1.0) 
    glBegin(GL_POLYGON)
    glVertex2f(x - 10, y)
    glVertex2f(x + 10, y)
    glVertex2f(x, y + 30)
    glEnd()

def draw_score():
    glColor3f(1.0, 1.0, 1.0) 
    glRasterPos2f(10, 10)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b"Score: " + str(score).encode())

def draw_start_screen():
    glColor3f(1.0, 1.0, 1.0)  
    glRasterPos2f(width // 2 - 120, height // 2)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b"Click 'S' to Start")

def draw_end_screen():
    glColor3f(1.0, 1.0, 1.0)  
    glRasterPos2f(width // 2 - 100, height // 2)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b"Game Over! Your Score: " + str(score).encode())
    glRasterPos2f(width // 2 - 90, height // 2 + 30)
    glutBitmapString(GLUT_BITMAP_HELVETICA_18, b"Click 'R' to Restart")

def game_over():
    global game_active
    game_active = False

def start_game():
    global game_active, start_time, score
    game_active = True
    start_time = time.time()
    score = 0
    reset_bubbles()

def reset_game():
    global game_active, score
    game_active = False
    score = 0
    reset_bubbles()

def reset_bubbles():
    global bubbles
    bubbles = []

def update_bubbles():
    global score, bubble_speed, start_time, max_bubbles

    elapsed_time = time.time() - start_time

    if elapsed_time < 10.0:
        bubble_speed = 0.1
        max_bubbles = 10
    elif elapsed_time < 15.0:
        bubble_speed = 0.3
        max_bubbles = 18
    else:
        bubble_speed = 0.5
        max_bubbles = 25

    for bubble in bubbles:
        bubble.y -= bubble_speed

        distance = math.sqrt((pointer_x - bubble.x) ** 2 + (pointer_y - bubble.y) ** 2)
        if distance <= bubble.radius:
            if bubble.color == (1, 0, 0): 
                game_over()
            else:
                score += 1
                bubbles.remove(bubble)

    new_bubble = Bubble(random.choice([(1, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (1, 0.5, 0)]))
    bubbles.append(new_bubble)

    bubbles[:] = [bubble for bubble in bubbles if bubble.y > -bubble.radius]

    while len(bubbles) < max_bubbles:
        new_bubble = Bubble(random.choice([(1, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1), (1, 0.5, 0)]))
        if new_bubble not in bubbles:
            bubbles.append(new_bubble)

    bubbles[:] = bubbles[:max_bubbles]

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if not game_active:
        draw_start_screen()
    else:
        for bubble in bubbles:
            draw_circle(bubble.x, bubble.y, bubble.radius, bubble.color)

        draw_pointer(pointer_x, pointer_y)
        draw_score()

        if not bubbles:
            draw_end_screen()

    glutSwapBuffers()

def keyboard(key, x, y):
    global bubble_speed, start_time

    if key == b'\x1b':  
        sys.exit()
    elif key == b's' or key == b'S':
        start_game()
    elif key == b'r' or key == b'R':
        reset_game()
    elif key == b'P' or key == b'p':
        pause_game()
    elif key == b'w' or key == b'W':
        bubble_speed += 0.1
    elif key == b's' or key == b'S':
        bubble_speed -= 0.1
        if bubble_speed < 0.1:
            bubble_speed = 0.1

    start_time = time.time()  

def pause_game():
    global game_active
    game_active = not game_active

def mouse(button, state, x, y):
    global pointer_x, pointer_y

    if game_active and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        pointer_x, pointer_y = x, height - y

def update():
    if game_active:
        update_bubbles()
        glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Bubble Burst Game")

glOrtho(0, width, 0, height, -1, 1)
glClearColor(0, 0, 0, 1)


glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutIdleFunc(update)
glutMainLoop()

