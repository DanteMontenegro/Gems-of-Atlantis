#Import libraries
import os
import random, time, pygame, sys
from pygame.locals import *

#Set screen 

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 16
BOARDWIDTH = 12
BOARDHEIGHT = 22
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1 

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#Colors

WHITE = (255, 255, 255)
CYANBLUE = ( 6, 77, 135)
GRAY = (185, 185, 185)
BLACK = ( 0, 0, 0)
PINK = (96, 0, 128)
LIGHTPINK = (128, 0, 255)
GREEN = ( 0, 120, 3)
LIGHTGREEN = ( 20, 175, 20)
BLUE = ( 0, 0, 155)
LIGHTBLUE = ( 20, 20, 175)
YELLOW = (0, 119, 120)
LIGHTYELLOW = (23, 159, 161)

PLAYBACKGROUND = pygame.image.load('background.jpg')
PLAYBACKGROUND = pygame.transform.scale(PLAYBACKGROUND, (640, 480))
BACKGROUNDCOVER = pygame.image.load('background-3.jpg')
BACKGROUNDCOVER = pygame.transform.scale(BACKGROUNDCOVER, (640, 480))
BORDERCOLOR = CYANBLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (    BLUE,    GREEN,    PINK,    YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTPINK, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS)

#Draw and set templates 

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

SHAPES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

#Main function

#Draw Board 

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT 
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 65)
    pygame.display.set_caption('Gems of Atlantis')
    DISPLAYSURF.blit(BACKGROUNDCOVER, ( 0,0 ) )
    pygame.display.flip()

#Set music

    showTextScreen('Gems of Atlantis')
    while True:
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('ambience.mp3')
        else:
            pygame.mixer.music.load('ambience.mp3')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

#Set start game configs

def runGame():
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False 
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()   

    #Initiate piece
    while True:
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() 

            if not isValidPosition(board, fallingPiece):
                return

        #Pause Button
        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if (event.key == K_p):
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') 
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_RIGHT or event.key == K_d):
                    movingRight = False
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = False

            elif event.type == KEYDOWN:
                #Set key commands
                if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                #Rotate piece 
                elif (event.key == K_UP or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                elif (event.key == K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])

                #Set fall faster
                elif (event.key == K_DOWN or event.key == K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                #Set instant fall
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        #Handle the fall for user input
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        #Set piece fall flow
        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board, fallingPiece, adjY=1):
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        #Draw Screen
        DISPLAYSURF.blit(PLAYBACKGROUND, ( 0,0 ))
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        pygame.display.flip()

#Make text

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

#Terminate function

def terminate():
    pygame.quit()
    sys.exit()

#Check key press

def checkForKeyPress():
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key 
    return None

#Display curtomized text on screen

def showTextScreen(text):
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

#Quit text if key press

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

#Check for quit 

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

#Get score points

def calculateLevelAndFallFreq(score):
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

#Define and initialize new piece

def getNewPiece():
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape,
    'rotation': random.randint(0, len(SHAPES[shape]) - 1),
    'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2), 
    'y': -2,
    'color': random.randint(0, len(COLORS)-1)}
    return newPiece

#Fix a piece to the board after landed

def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('bubble.mp3'), maxtime=600)



#Reset board 

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board


def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT 

#Check if the next position is valid (blank) or not (filled)

def isValidPosition(board, piece, adjX = 0, adjY = 0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK: 
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

#Check if the given line is complete

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('splash.mp3'), maxtime=1800)
    return True

#If it is complete, then remove the line

def removeCompleteLines(board):
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1  
    while y >= 0:
        if isCompleteLine(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
        else:
            y -= 1 
    return numLinesRemoved

#Convert board coordinates to pixels

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

#Draw Piece 

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 5, pixely + 5, BOXSIZE - 4, BOXSIZE - 4))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 5, pixely + 5, BOXSIZE - 4, BOXSIZE - 4))

#Draw Board

def drawBoard(board):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * 16) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOXSIZE * BOARDWIDTH) + 8, (BOXSIZE * BOARDHEIGHT) + 8))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, 25 - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * 3.50) + 8), 5)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN - 3, 25 - 7, (BOXSIZE * BOARDWIDTH) + 8, (3.50 * BOARDHEIGHT) + 8))

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

#Draw Status 

def drawStatus(score, level):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 397, 27)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 397, 52.9)
    DISPLAYSURF.blit(levelSurf, levelRect)

#Draw piece 

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

#Draw next piece

def drawNextPiece(piece):
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 397, 78.0)
    DISPLAYSURF.blit(nextSurf, nextRect)
    drawPiece(piece, pixelx=WINDOWWIDTH-298, pixely=21)

#Call main

if __name__ == '__main__':
    main()











    
           
        






    
