import pygame
from pygame.locals import *
import math
import numpy as np
import copy

pygame.init()
screen_width = 1300
screen_height= 1100
pygame.display.set_caption('Projectile Intercept')
screen = pygame.display.set_mode((screen_width,screen_height))
## FPS and Clock ###########################################################################
FPS = 60
FPSclock = pygame.time.Clock()
## Colors ##################################################################################
bg = (50,25,50)
# bg=(0,0,0)
black=(0,0,0)
white = (255,255,255)
aqua = (0,255,255)
red = (255,0,0)
green = (0,255,0)


## Repetitive Functions ####################################################################
def draw_board(background_color):   # Fills background with bg color and draw the board
    screen.fill(background_color)

def get_unit_vector(vect):
    """
    Takes a vector as an input, and outputs its unit vector
    """
    mag = np.linalg.norm(vect)
    return vect/mag
def rotation_transform(theta):
    initial_vect = np.array([1,0])
    T_matrix = np.array([[math.cos(theta),-math.sin(theta)],[math.sin(theta),math.cos(theta)]])
    return np.dot(T_matrix,initial_vect)

## Classes
class Turret:
    def __init__(self,x,y,bullet_speed):
        self.x = x
        self.y = y
        self.pos = np.array([x,y])  # Center of the turret in global coordinates
        self.gun_hat = np.array([1,0])  # Initial unit vector of the turret direction
        self.bullet_speed = bullet_speed
        self.bullet_velocity = self.bullet_speed*self.gun_hat

    def rotate_gun(self):
        mouse_x,mouse_y = pygame.mouse.get_pos()
        mouse_vect = np.array([mouse_x,mouse_y])
        direction_vect = mouse_vect-self.pos
        self.gun_hat = get_unit_vector(direction_vect)
        self.bullet_velocity = self.bullet_speed*self.gun_hat

    def intercept_bullet(self,theta2):
        self.gun_hat = rotation_transform(theta2)
        self.bullet_velocity = self.bullet_speed*self.gun_hat

    def draw(self):
        pygame.draw.circle(screen,white,tuple(self.pos),20,2)
        pygame.draw.line(screen,green,tuple(self.pos),tuple(self.pos+self.gun_hat*30),3)

    @classmethod
    def intercept(cls,gun1,gun2):
        v1_mag = gun1.bullet_speed
        v1x = gun1.bullet_velocity[0]
        v1y = gun1.bullet_velocity[1]
        Ax,Ay = gun1.x,gun1.y
        v2_mag = gun2.bullet_speed
        Bx,By = gun2.x,gun2.y

        if v1_mag != v2_mag:
            A = (v2_mag**2)-(v1x**2)-(v1y**2)
            print(f"v2_mag:{v2_mag},v1x:{v1x},v1y:{v1y}")
            B = ((-2*v1x*(Ax-Bx))-(2*v1y*(Ay-By)))
            C = (-(Ax-Bx)**2-(Ay-By)**2)
            print(f"A:{A},B:{B},C:{C}")

            t1 = (-B+math.sqrt(B**2-(4*A*C)))/(2*A)
            print(t1)
            v2x = ((Ax-Bx)/t1)+v1x
            v2y = ((Ay-By)/t1)+v1y
            print(v2_mag,v2x)

            theta2 = math.atan2(v2y,v2x)
            return theta2
        elif v1_mag == v2_mag:
            vect_from_gun1_to_gun2 = gun2.pos - gun1.pos
            alpha = math.atan2(vect_from_gun1_to_gun2[1],vect_from_gun1_to_gun2[0])
            theta1 = math.atan2(v1y,v1x)
            phi = theta1-alpha
            theta2 = alpha + math.radians(180) - phi
            return theta2

class Bullet:
    def __init__(self,x,y,vel):
        self.pos=np.array([x,y])
        self.vel = vel  # Already an np 2d array

    def update(self):
        self.pos = self.pos + self.vel

    def draw(self):
        pygame.draw.circle(screen,white,self.pos,7)



## Objects
player1 = Turret(screen_width/2,screen_height/2,4)
other_turret1 = Turret(screen_width/4,screen_height/4,4.5)
other_turret2 = Turret(3*screen_width/4,screen_height/4,5)
other_turret3 = Turret(2.5*screen_width/4,3*screen_height/4,7)

## Game loop
run = True
player_bullet_on = False
while run:
    FPSclock.tick(FPS)
    draw_board(black)

    # Define events from user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # Quit the game
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullet=Bullet(player1.x,player1.y,player1.bullet_velocity)
                player_bullet_on = True

                theta2_1 = Turret.intercept(player1,other_turret1)
                other_turret1.intercept_bullet(theta2_1)
                other_bullet1 = Bullet(other_turret1.x,other_turret1.y,other_turret1.bullet_velocity)

                theta2_2 = Turret.intercept(player1,other_turret2)
                other_turret2.intercept_bullet(theta2_2)
                other_bullet2 = Bullet(other_turret2.x,other_turret2.y,other_turret2.bullet_velocity)

                theta2_3 = Turret.intercept(player1,other_turret3)
                other_turret3.intercept_bullet(theta2_3)
                other_bullet3 = Bullet(other_turret3.x,other_turret3.y,other_turret3.bullet_velocity)

    player1.rotate_gun()
    if player_bullet_on:
        player_bullet.update()
        other_bullet1.update()
        other_bullet2.update()
        other_bullet3.update()

    player1.draw()
    other_turret1.draw()
    other_turret2.draw()
    other_turret3.draw()

    if player_bullet_on:
        player_bullet.draw()
        other_bullet1.draw()
        other_bullet2.draw()
        other_bullet3.draw()

    pygame.display.update()     # This appears to be necessary for anything to actually update in the screen
pygame.quit()
