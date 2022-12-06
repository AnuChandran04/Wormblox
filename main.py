import random, pygame, sys
from pygame.locals import *
from random import randint

FPS = 10
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 1, 1)
RANDCOLOUR = (randint(0,255),randint(0,255),randint(0,255))
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = (WHITE)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0
HEAD2 = 0  # syntactic sugar: index of the worm's head


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
      runGame()
      showGameOverScreen()


def runGame():
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    # Adding in a second worm's start point to make the game multiplayer -Anu
    worm2Coords = [{'x': startx, 'y': starty + 5},
                   {'x': startx - 1, 'y': starty + 5},
                   {'x': startx - 2, 'y': starty + 5},
                   {'x': startx - 3, 'y': starty + 5}]
    wallCoords = [{'x': 5, 'y': 6},
                  {'x': 10, 'y': 6},
                  {'x': 3, 'y': 6},
                  {'x': 2, 'y': 6},
                  {'x': 4, 'y': 8},
                  {'x': 10, 'y': 8},
                  {'x': 11, 'y': 8},
                  {'x': 12, 'y': 8},
                  {'x': 13, 'y': 8},
                  {'x': 16, 'y': 8},
                  {'x': 17, 'y': 8},
                  {'x': 18, 'y': 8},
                  {'x': 20, 'y': 8},
                  {'x': 21, 'y': 8},
                  {'x': 22, 'y': 8},
                  {'x': 23, 'y': 8},
                  {'x': 24, 'y': 8},
                  {'x': 28, 'y': 8},
                  {'x': 29, 'y': 8},
                  {'x': 30, 'y': 8},
                  {'x': 31, 'y': 9},
                  {'x': 33, 'y': 9},
                  {'x': 34, 'y': 9},
                  {'x': 35, 'y': 9},
                  {'x': 36, 'y': 9},
                  {'x': 5, 'y': 30},
                  {'x': 6, 'y': 30},
                  {'x': 7, 'y': 30},
                  {'x': 10, 'y': 30},
                  {'x': 11, 'y': 30},
                  {'x': 12, 'y': 30},
                  {'x': 32, 'y': 30},
                  {'x': 33, 'y': 30},
                  {'x': 39, 'y': 30},
                  {'x': 40, 'y': 30},
                  {'x': 41, 'y': 30},
                  {'x': 42, 'y': 30},
                  {'x': 45, 'y': 30},
                  {'x': 20, 'y': 30},
                  {'x': 21, 'y': 30},
                  {'x': 22, 'y': 30},
                  {'x': 23, 'y': 30},
                  {'x': 26, 'y': 30},
                  {'x': 27, 'y': 30}, ]  # If I add any more walls the game will be too hard
    # Wall coordinates like worm coordinates
    # -Samantha.S

    direction = RIGHT
    direction2 = RIGHT
  #direction2 allows directions to be programmed for the second worm in multiplayer -Anu

    # Start the apple in a random place.
    apple = getRandomLocation()
    apple2 = getRandomLocation()
    apple3 = getRandomLocation()
    apple4 = getRandomLocation()


    while True:  # main game loop

        for event in pygame.event.get():  # event handling loop for first worm (controlled using up, down, left, right keys) -Anu
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
    #Event handling loop for second worm (controlled using a, d, w, s keys) -Anu
                if (event.key == K_a) and direction2 != RIGHT:
                    direction2 = LEFT
                elif (event.key == K_d) and direction2 != LEFT:
                    direction2 = RIGHT
                elif (event.key == K_w) and direction2 != DOWN:
                    direction2 = UP
                elif (event.key == K_s) and direction2 != UP:
                    direction2 = DOWN

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == CELLHEIGHT:
            return  # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # game over
            # ******************************************************************************************
        for wormBody in wormCoords[0:]:
            for wallBody in wallCoords[0:]:
                if wormBody['x'] == wallBody['x'] and wormBody['y'] == wallBody['y']:
                    return  # game over
                    # How the wall kills you -Samantha.S
                    # The wall kills you the same way the worm body kills you

        for worm2Body in worm2Coords[0:]:
            for wallBody in wallCoords[0:]:
                if worm2Body['x'] == wallBody['x'] and worm2Body['y'] == wallBody['y']:
                    return  # game over
                        # How the wall kills you -Samantha.S
                        # The wall kills you the same way the worm body kills you
            # ******************************************************************************************

            # check if the second worm has hit itself or the edge -Anu
            if worm2Coords[HEAD2]['x'] == -1 or worm2Coords[HEAD2]['x'] == CELLWIDTH or worm2Coords[HEAD2]['y'] == -1 or \
                    worm2Coords[HEAD2]['y'] == CELLHEIGHT:
                return  # game over
            for worm2Body in worm2Coords[1:]:
                if worm2Body['x'] == worm2Coords[HEAD2]['x'] and worm2Body['y'] == worm2Coords[HEAD2]['y']:
                    return  # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation()
            apple2 = getRandomLocation()
            apple3 = getRandomLocation()
            apple4 = getRandomLocation()
            # set a new apple somewhere
        else:
            del wormCoords[-1]  # remove worm's tail segment

            # check if second worm has eaten an apple -Anu
            if worm2Coords[HEAD2]['x'] == apple['x'] and worm2Coords[HEAD2]['y'] == apple['y']:
                # don't remove worm's tail segment
                apple = getRandomLocation()
                apple2 = getRandomLocation()
                apple3 = getRandomLocation()
                apple4 = getRandomLocation()# set a new apple somewhere
            else:
                del worm2Coords[-1]  # remove second worm's tail segment-Anu

        # Moving the worm involves adding a body segment at the coordinate that the worm is moving toward (aka wormCoords). -Anu
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD][
                                                            'y'] - 1}  # Because the segment is added at the beginning of the snake, it will be the "head", hence the name "newHead". -Anu
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD][
                'y']}  # The new head is right beside the old head's coordinates. This is denoted by the +1 or -1 depending on the direction the snake is moving along a particular axis. -Anu
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

          
        # Moving the second worm involves adding a body segment at the coordinate that the worm is moving toward (aka wormCoords). A new head variable is created. Similar to above. -Anu
        if direction2 == UP:
            newHead2 = {'x': worm2Coords[HEAD2]['x'], 'y': worm2Coords[HEAD2]['y'] - 1}  
        elif direction2 == DOWN:
            newHead2 = {'x': worm2Coords[HEAD2]['x'], 'y': worm2Coords[HEAD2]['y'] + 1}
        elif direction2 == LEFT:
            newHead2 = {'x': worm2Coords[HEAD2]['x'] - 1, 'y': worm2Coords[HEAD2]['y']}  
        elif direction2 == RIGHT:
            newHead2 = {'x': worm2Coords[HEAD2]['x'] + 1, 'y': worm2Coords[HEAD2]['y']}

        wormCoords.insert(0, newHead)
        worm2Coords.insert(0, newHead2)
      #The insert function adds the newHeads for both worms at the end

      
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawWorm2(worm2Coords)
        drawApple(apple)
        drawApple(apple2)
        drawApple(apple3)
        drawApple(apple4)
        drawScore(len(wormCoords) - 3)
        drawScore2(len(worm2Coords) - 3)
        drawWall(wallCoords)  # Wall coordinates
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        DISPLAYSURF.fill(BGCOLOR)


# This function allows the user to press a key to start the game, when on the Start or Game Over screen
def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True,
                                    DARKGRAY)  # The function renders the font so the player knows to press the key -Anu
    pressKeyRect = pressKeySurf.get_rect()  # Then, the function defines and displays the rectangular window of the game. -Anu
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


# This function is called in both the showStartScreen() and the showGameOverScreen() functions, instead of retyping this function both times. -Anu


# This function checks whether to terminate the game.
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    # QUIT is passed as an argument. Therefore, if any QUIT events exist, then the game is terminated.
    # If there are no quit events, the empty list [] is returned. The len() will, as a result, return 0.  -Anu

    # The below function serves a similar purpose: to terminate the game. -Anu
    keyUpEvents = pygame.event.get(
        KEYUP)  # However, here the function passes KEYUP as an argument, and searches for if a keyup event has occurred.-Anu
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[
        0].key  # If the "escape" key is pressed, the game is terminated. Otherwise, the result of the first function is returned. -Anu


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3  # rotate by 3 degrees each frame
        degrees2 += 7  # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    textw = pygame.font.Font('freesansbold.ttf', 100)
    textword = pygame.font.Font('freesansbold.ttf', 55)
    gameSurf = gameOverFont.render('Game', True, BLACK)
    overSurf = gameOverFont.render('Over', True, BLACK)
        # ******************************************************
    text = textw.render("Be better!!", True, BLACK)
    text2 = textword.render("Don't hit the walls!", True, BLACK)
        # *******************************************************
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    textRect = text.get_rect()
    text2Rect = text2.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    textRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 20 + 200)
    text2Rect.midtop = (WINDOWWIDTH / 2, gameRect.height + 50 + 300)

        # Modified it game over screen and added more words
        # -Samantha.S

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    DISPLAYSURF.blit(text, textRect)
    DISPLAYSURF.blit(text2, text2Rect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()  # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get()  # clear event queue
            return


# Code to render and draw the score of the player. Specifies font color, the width of the score display window, and the words. -Anu
def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

# Code to render and draw the score of the second player. Specifies font color, the width of the score display window, and the words.  -Anu
def drawScore2(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, BLACK)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (WINDOWWIDTH - 120, 10) #It also makes sure the score renders in a different location from the first score, preventing overlap -Anu
    DISPLAYSURF.blit(scoreSurf, scoreRect)


# Code to render and draw the worm.
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE  # this converts the grid coordinates to pixel coordinates -Anu
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN,
                         wormSegmentRect)  # this draws dark green boxes for the worm's body at the location of the worm's coordinates (x and y) -Anu
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8,
                                           CELLSIZE - 8)  # this creates light green boxes inside the dark green boxes for aesthetic purposes. There is a 4 pixel margin between the light and dark green. -Anu
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)  # this draws the light green rectangles -Anu


# Code to render and draw the second worm.
def drawWorm2(worm2Coords):
    for coord in worm2Coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE  # this converts the grid coordinates to pixel coordinates -Anu
        worm2SegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN,
                         worm2SegmentRect)  # this draws dark green boxes for the worm's body at the location of the worm's coordinates (x and y) -Anu
        worm2InnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8,CELLSIZE - 8)  # this creates RED boxes inside the dark green boxes for aesthetic purposes, to differentiate the 2 worms. There is a 4 pixel margin between the light and dark green. -Anu
        pygame.draw.rect(DISPLAYSURF, RED, worm2InnerSegmentRect)  # this draws the red rectangles -Anu




# This draws and renders the apple -Anu
def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord[
            'y'] * CELLSIZE  # similar to drawWorm(), this converts the grid coordinates to pixel coordinates for the apple -Anu
    appleRect = pygame.Rect(x, y, CELLSIZE,
                            CELLSIZE)  # The apple is a single red rectangle. This function creates the rectangle -Anu
    pygame.draw.rect(DISPLAYSURF, RANDCOLOUR, appleRect)  # this draws the created rectangle-Anu


# Similar to the above, this function draws and renders the horizontal and vertical grid lines-Anu
def drawWall(coordWall):
    for coord in coordWall:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, WHITE, wormInnerSegmentRect)
        # The walls are made from the bodies of dead worms
        # Wall coordinate function is called on at the top of the game
        # -Samantha.S


def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))
# instead of typing out code for the 32 lines to fill the grid, a for loop is used. This iterates over the width and height to draw the grid, using less code. -Anu

# after all functions and variables are created, main() calls the game. -Anu
if __name__ == '__main__':
  main()

