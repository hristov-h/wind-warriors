import cv2
import numpy as np
import random
import threading
import time
import pygame
import sys
import os
import pygame_menu
from pygame import mixer
from pygame.locals import *

WIDTH = 800
HEIGHT = 500
GRAY = (169, 169, 169)
pygame.init() #initialise pygame
surface = pygame.display.set_mode((WIDTH, HEIGHT)) #set the resolution for the menu window
pygame.display.set_caption("Wind Warriors!") # display wind warriors on window bar
jetPlane = pygame.transform.scale2x(pygame.image.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/assets/jet-sprite.png')).convert_alpha() #Load backround, convert the alpha channel of the image and scale it to fit in to the screen 
jetPlane_rect = jetPlane.get_rect() # add a rectangle so we can detect collision
player_vel = 3 # player movement
menu_music = mixer.music.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/sound/menu_music.wav')#loads music
mixer.music.play(-1) #play music on repeat
mixer.music.set_volume(0.1) #the volume of the music
mixer.music.get_volume() #start music

#enemy drones
class Drone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale2x(pygame.image.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/assets/drone_spr.png')).convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect = Rect(0.1,-20,37,40) #width=37 height=40
        #self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.x = random.randrange(820, 1500) # spawn in this range
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedx = random.randrange(-4, -1) # set speed on x axis
        self.speedy = random.randrange(-1, 2) # set speed on y axis

    def update(self):
        self.rect.x += self.speedx  
        self.rect.y += self.speedy
        if self.rect.left < - 200 or self.rect.top < -80: #if the drones goes above the coordinates
            self.rect.x = random.randrange(900, 950)   # spawn them somewhere in these coordinates 
            self.rect.y = random.randrange(0, HEIGHT)
            self.speedx = random.randrange(-4, -1) #set speed on x axis
            self.speedy = random.randrange(-1, 2) #set speed on y axis

        collide = jetPlane_rect.colliderect(self.rect) #check if we have collision
        if collide == True: # if collide happens 
            mixer.music.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/sound/end_game.wav') #load music
            mixer.music.play(1) #play music once
            mixer.music.set_volume(0.6) #the volume of the music
            mixer.music.get_volume() #start music
            time.sleep(2.5) # wait 2.5 seconds before the Game Over screen
            end_game() # jump to the game over screen

class EnemyJet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale2x(pygame.image.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/assets/jet-sprite1_rotated.png')).convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect = Rect(10,10,10,10)
        self.rect.x = random.randrange(820, 1500)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedx = random.randrange(-8, -6)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < - 2200:
            self.rect.x = random.randrange(900, 950)
            self.rect.y = random.randrange(0, HEIGHT)
            self.speedx = random.randrange(-8, -6)

        collide = jetPlane_rect.colliderect(self.rect)
        if collide == True:
            mixer.music.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/sound/end_game.wav')
            mixer.music.play(1) #play music once
            mixer.music.set_volume(0.6) #the volume of the music
            mixer.music.get_volume() #start music
            time.sleep(2.5)
            end_game()

#white particles
class WhiteParticles(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2, 2))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        #self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.x = random.randrange(50, 820)
        #self.rect.x = random.randrange(-600, 100)
        self.rect.y = random.randrange(0, HEIGHT)
        self.speedx = random.randrange(-4, -1)
        self.speedy = random.randrange(-1, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < - 200:
            #self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.x = random.randrange(500, 820)
            self.rect.y = random.randrange(0, HEIGHT)
            self.speedx = random.randrange(-4, -1)
            self.speedy = random.randrange(-1, 2)


def start_the_game():
    global jetPlane_rect, all_sprites #set to global variables so we can use them
    #pygame.init() # initiallise pygame ()
    #set the resolution for the game window
    game_screen = pygame.display.set_mode((WIDTH,HEIGHT)) # set the dimesnion of the game
    screen_rect=game_screen.get_rect() #make a screen rectangle to keep player inside
    clock = pygame.time.Clock() # initialise clock object
    background_image = pygame.transform.scale2x(pygame.image.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/assets/space.png')).convert() #Load backround and scale it to fit in to the screen 
    jetPlane_rect.x = 100 # set x coordinate for player
    jetPlane_rect.y = 250 # set y coordinate for player
    all_sprites = pygame.sprite.Group() # group all sprites so we can add them on the screen
    for i in range(8): #spawn 8 drones
        drone = Drone()
        all_sprites.add(drone)
    for i in range(200): #spawn 200 particles
        particles = WhiteParticles()
        all_sprites.add(particles)
    for i in range(4): #spawn 4 enemy jets/ rockets
        enemy_jet = EnemyJet()
        all_sprites.add(enemy_jet)
    #Background sound
    mixer.music.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/sound/Ungodly(Karl_Casey_@_WhiteBatAudio).wav') #load game music
    mixer.music.play(-1) #play music on repeat
    mixer.music.set_volume(0.1) #the volume of the music
    mixer.music.get_volume() #start music

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # unables the game to quit
                sys.exit() # shut down the game completely
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]: # if up arrow key is pressed go up
            jetPlane_rect.y -= player_vel 
        if keys[pygame.K_DOWN]: # if down arrow key is pressed go down
            jetPlane_rect.y += player_vel 
            
        jetPlane_rect.clamp_ip(screen_rect)# ensure player is inside screen
        game_screen.blit(background_image,(0,0)) #draw image to the canvas
        game_screen.blit(jetPlane,jetPlane_rect)
        all_sprites.update()
        all_sprites.draw(game_screen)

        pygame.display.update()
        clock.tick(60) # initialise frames per second

#restarts the menu music because if we dont the music stops and does not load  
def play_music():
    menu_music = mixer.music.load('/home/ratiboro/Projects/OX_Brookes/COMP6013_Computing_Project/sound/menu_music.wav')
    mixer.music.play(-1) #play music on repeat
    mixer.music.set_volume(0.1) #the volume of the music
    mixer.music.get_volume() #start music


#end game screen    
def end_game():
    endgame = pygame_menu.Menu(HEIGHT, WIDTH, '',
                        theme=pygame_menu.themes.THEME_DARK)
    HELP = "GAME OVER \n "
    endgame.add_label(HELP, max_char=-1, font_size=50)
    endgame.add_button('Go back',  main_menu)
    play_music()
    endgame.mainloop(surface)
#menu settings
def menu_settings():
    sub_menu = pygame_menu.Menu(HEIGHT, WIDTH, 'Settings',
                        theme=pygame_menu.themes.THEME_DARK)
    sub_menu.add_button('Audio', start_the_game)
    sub_menu.add_button('About', about_game)
    sub_menu.add_button('Go back',  main_menu)
    sub_menu.mainloop(surface)
# main menu screen
def main_menu():
    menu = pygame_menu.Menu(HEIGHT, WIDTH, 'Wind Warriors',
                        theme=pygame_menu.themes.THEME_DARK)
    menu.add_button('Play', start_the_game)
    menu.add_button('Settings',  menu_settings)
    menu.add_button('Quit Game', pygame_menu.events.EXIT)
    menu.mainloop(surface)
#about the game screen
def about_game():
    about = pygame_menu.Menu(HEIGHT, WIDTH, 'About',
                        theme=pygame_menu.themes.THEME_DARK)
    
    HELP = "This game is made by SN 17051611 \n "\
        "Music by: Karl Casey @ White Bat Audio \n "\
        "Thank you for playing! \n "\
            "Enjoy the game! "\
                " =) "
    about.add_label(HELP, max_char=-1, font_size=20)
    about.add_button('Go back',  menu_settings)

    about.mainloop(surface)



#OpenCV tracking function
def cv_function():
    cap =cv2.VideoCapture(0)
    # Here we can choose which tracker to use/ Best for use are CSRT and KCF from my testing
    tracker = cv2.TrackerCSRT_create()
    #tracker = cv2.TrackerKCF_create()
    #tracker = cv2.TrackerMOSSE_create()
    #tracker = cv2.TrackerTIO_create()
    #Set up the image to drow the initial square.
    success, img = cap.read()
    img = cv2.flip(img,+1)
    

    #bounding_box - touple
    bounding_box = cv2.selectROI("Tracking",img,False)
    tracker.init(img,bounding_box)

    def draw_upper_line(img):
        cv2.line(img,(1,90),(636,90),(255,0,0),3)

    def draw_lower_line(img):
        cv2.line(img,(1,400),(639,400),(255,0,0),3)


    def draw_box(img,bounding_box):
        x,y,w,h = int(bounding_box[0]),int(bounding_box[1]),int(bounding_box[2]),int(bounding_box[3])
        cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
        cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2) # Display tracking if we can see the object
    
    while True:
        #Set up the image to recieve feed from the camera
        success, img = cap.read()
        #Flip the image
        img = cv2.flip(img,+1)
        timer = cv2.getTickCount() #initilise timer so we can measure performance of the code
        success,bounding_box = tracker.update(img) #update the bounding_box
        if success:
            draw_box(img,bounding_box)
            draw_upper_line(img)
            draw_lower_line(img)
        else:
            cv2.putText(img,"Lost ",(75,75),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2) # if the lines dissapear because we lost the object display Lost

        if int(bounding_box[1]) <= 90:
            cv2.putText(img,"Top", (200,75),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            jetPlane_rect.y -= player_vel + 3 # if the box passes the upper line move the player up
        if int(bounding_box[1]+bounding_box[3]) >= 400:
            cv2.putText(img,"Bottom", (200,75),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            jetPlane_rect.y += player_vel + 3 # if the box passes the lower line move the player down

        fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer) #fps tracker
        cv2.putText(img,str(int(fps)),(75,50),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
        cv2.imshow("Tracking",img) 

        if cv2.waitKey(1) & 0xff ==ord('q'):
            break


t2 = threading.Thread(target=cv_function) #run computer vision code on the second thread
t2.start() #start the thread
main_menu() # start the game on the main thread
t2.join() # synchronize the two threads

