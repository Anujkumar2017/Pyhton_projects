import random # For generating random numbers
import sys # we will use sys.exit to exit the program
import pygame
from pygame.locals import *  #Basic pygame imports

#Global variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

#for welcome screen 
def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2) 
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0 
    basey = GROUNDY
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button,close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))  
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))  
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))  
                SCREEN.blit(GAME_SPRITES['base'],(basex,basey))  
                pygame.display.update()
                FPSCLOCK.tick(FPS) 

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/2)
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    basex = 0 
    basey = GROUNDY

    #create 2 pipes for bliting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
    ]

    #list of lower pipes
    lowerPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']}
    ]

    pipeVelX = -4                     #pipe velocity(-ive means in left side)

    playerVelY = -9                   #bird velocity
    playerMaxVelY = 10
    playerAccY = 1 

    playerFlapVel = -8                #velocity while flapping
    playerFlapped = False             #it is true only when bird is flapped

    while True: 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery>0:
                    playerVelY = playerFlapVel
                    playerFlapped = True
                    GAME_SOUNDS["wing"].play()
        
        #if collision occurs
        if isCollide(playerx,playery,upperPipes,lowerPipes):
            return        
        
        #check for score
        playerMidPos = playerx +GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score +=1
                # print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        #incresing the velocity
        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        
        #setting new position 
        playerHeight = GAME_SPRITES['player'].get_height()
        playery+=min(playerVelY,GROUNDY-playery - playerHeight)

        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipeVelX
            lowerPipe['x']+=pipeVelX
        
        #add a new pipe in upperpipes and lowerpipes
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        
        #removing the pipe which pass the leftmost screen 
        if upperPipes[0]['x']< - GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #sprite bliting    
        SCREEN.blit(GAME_SPRITES['background'],(0,0))  
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))  
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
              
        SCREEN.blit(GAME_SPRITES['base'],(basex,basey))
        
        #sprite bliting for score
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width+= GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH-width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#detecting collision
def isCollide(playerx,playery,upperPipes,lowerPipes):
    #hitting the ground or above the screen
    if playery >= GROUNDY-GAME_SPRITES["player"].get_height() or playery <= 0:
        GAME_SOUNDS['hit'].play()
        GAME_SOUNDS['die'].play()
        return True
    
    #collision with upperpies
    for pipe in upperPipes:
        pipeHeight= GAME_SPRITES['pipe'][0].get_height()
        pipeWidth = GAME_SPRITES['pipe'][0].get_width()
        if(playery < pipeHeight + pipe['y'] and (abs(playerx - pipe['x'])<pipeWidth)):
            GAME_SOUNDS['swoosh'].play()
            GAME_SOUNDS['die'].play()
            return True
    
    #collision with lowerpipes
    for pipe in lowerPipes:
        playerHeight= GAME_SPRITES['player'].get_height()
        if(playery + playerHeight > pipe['y'] and (abs(playerx - pipe['x'])<pipeWidth)):
            GAME_SOUNDS['swoosh'].play()
            GAME_SOUNDS['die'].play()
            return True
    return False

def getRandomPipe():
    """
    Generating positions of two new pipes for bliting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset+random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex = SCREENWIDTH+10
    y1 = pipeHeight-y2+offset
    pipe =[
        {'x':pipex,'y':-y1}, #upper pipe
        {'x':pipex,'y':y2} #Lower pipe
    ] 
    return pipe

if __name__ == '__main__':
    pygame.init() #Initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()   
    pygame.display.set_caption('FlappyBird by A K')
    
    #Game sprites
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base']= pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['background']= pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']= pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['pipe']= (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()        
    )

    #game sound
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
    