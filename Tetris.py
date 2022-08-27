from ast import If, Return
from pickle import TRUE
from tkinter.messagebox import RETRY
import pygame
import random

pygame.init()
blockSize = 45
WINDOW_WIDTH = 1680
WINDOW_HEIGHT = 1050
GAME_WIDTH = blockSize*10
GAME_HEIGHT = blockSize*20
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
running = True

fps = pygame.time.Clock()

#COLOURS

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 30, 30)
orange = pygame.Color(255, 100, 30)
green = pygame.Color(0, 255, 70)
blue = pygame.Color(0, 185, 255)
darkBlue = pygame.Color(0, 80, 180)
purple = pygame.Color(145, 0, 170)
yellow = pygame.Color(255, 220, 0)


GAME_COLOUR = black

timeSinceCollision = 0.0

sapontiachh = False   
# Stop active piece on next tick if a collision has happened

#GRID SETUP
grid = []
for i in range(10):
    row = [] 
    for j in range(21):
        row.append({
            'colour': GAME_COLOUR,
            'active': False,
        })
    grid.append(row)

#STOP MOVING BLOCKS
def bottomStop(grid):
    global sapontiachh
    for col in range(len(grid)):
        if grid[col][19]['active'] == True:
            sapontiachh = True  

#COLLISIONS
def collision(grid, colShift, rowShift):
    # Loop through to find active pieces
    for col in range(len(grid)):
        for row in range(len(grid[col])-1):
            if grid[col][row]['active'] == True:
    
    # what it should return (return a TRUE or FALSE)
                if (col + colShift < 0 or
                    col + colShift > 9):
                    return True


                elif (grid[col + colShift][row + rowShift]['colour'] != GAME_COLOUR and 
                      grid[col + colShift][row + rowShift]['active'] == False):
                        return True

    return False


hardDrop = False

def stopActivePieces():
    for col in range(len(grid)):
        for row in range(len(grid[col])-1):
            if grid[col][row]['active'] == True:
                grid[col][row]['active'] = False

    lineClear()

def lineClear():
    # for row in range(len(grid[0])-2, 0, -1):
    row = len(grid[0])-2  #row = 19
    while row > 0:
        rowComplete = True
        for col in range(len(grid)):
        # here
            #Check for missing pieces in row
            if grid[col][row]['colour'] == GAME_COLOUR:
                rowComplete = False

        if rowComplete:
            # print('ROW COMPLETE ', row + 1)
            #  < row complete shift down
            print('completed row:', row)
            
            

            for rowDone in range(row-1, 0, -1):
                for colDone in range(len(grid)):
                    if grid[colDone][rowDone]['active'] == False:
                        grid[colDone][rowDone+1] = grid[colDone][rowDone]
            
            
            
            for colTop in range(len(grid)):
                for rowTop in range(2):    #top 2 rows
                    grid[colTop][rowTop] = {
                                      'colour': GAME_COLOUR,
                                      'active': False,
                                   }
            # only clearing bottom row
            # triple square block
        else:
            row -= 1


#VARIABLES
gameX = int(WINDOW_WIDTH / 2 - GAME_WIDTH / 2)
gameY = int(WINDOW_HEIGHT / 2 - GAME_HEIGHT / 2)


MOVE_DOWN_EVENT = pygame.USEREVENT + 1
KEY_DOWN_EVENT = pygame.USEREVENT + 2
HARD_DROP = pygame.USEREVENT + 3

pygame.time.set_timer(MOVE_DOWN_EVENT, 700)
pygame.time.set_timer(KEY_DOWN_EVENT, 70)
pygame.time.set_timer(HARD_DROP, 1)


# BLOCKS

longbar = {'colour': blue, 'matrix': [[1,1,1,1],[0,0,0,0]]}
sBlock = {'colour': green, 'matrix': [[0,1,1,0],[1,1,0,0]]}
zBlock = {'colour': red, 'matrix': [[1,1,0,0],[0,1,1,0]]}
LBlock = {'colour': orange, 'matrix': [[0,0,1,0],[1,1,1,0]]}
JBlock = {'colour': darkBlue, 'matrix': [[1,0,0,0],[1,1,1,0]]}
square = {'colour': yellow, 'matrix': [[0,1,1,0],[0,1,1,0]]}
tBlock = {'colour': purple, 'matrix': [[0,1,0,0],[1,1,1,0]]}

# BLOCKS = [longbar, sBlock, zBlock, LBlock, JBlock, square, tBlock]
BLOCKS = [longbar, square]


def spawnBlock():
    spawningBlock = random.randrange(0, len(BLOCKS))
    for across in range(len(BLOCKS[spawningBlock]['matrix'])):
        for down in range(len(BLOCKS[spawningBlock]['matrix'][across])):
            if BLOCKS[spawningBlock]['matrix'][across][down] == 1:
                grid[down + 3][across]['colour'] = BLOCKS[spawningBlock]['colour']
                grid[down + 3][across]['active'] = True

for i in range(10):
    grid[i][20]['colour'] = blue

spawnBlock()

def blockFalling():
    global sapontiachh
    wcgdhitnfbos = collision(grid, 0, +1)
    for col in range(len(grid)):
        for row in range(len(grid[col]) -1, 0, -1):
            if grid[col][row - 1]['active'] == True:
                if wcgdhitnfbos == False:
                    #copy row above
                    grid[col][row] = grid[col][row - 1]
                    #reset row above falling block
                    grid[col][row - 1] = {
                                            'colour': GAME_COLOUR,
                                            'active': False,
                                        }
                if wcgdhitnfbos == True:
                    sapontiachh = True

#GAME START
while running:  



    if sapontiachh == True:
        timeSinceCollision += fps.get_time()

        if timeSinceCollision > 400:
            if collision(grid, 0, +1):
                stopActivePieces()
                spawnBlock()
                hardDrop = False
            timeSinceCollision = 0.0
            sapontiachh = False


    window.fill(black)
    #QUIT GAME
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #KEY PRESSES
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        #LEFT & RIGHT MOVEMENT
            elif event.key == pygame.K_LEFT:
                if hardDrop == False:
                    if collision(grid, -1, 0) == False:
                        for col in range(1, len(grid)):
                            for row in range(len(grid[col])-1, -1, -1):
                                if grid[col][row]['active'] == True:
                                    grid[col-1][row] = grid[col][row]
                                    grid[col][row] = {
                                                    'colour': GAME_COLOUR,
                                                    'active': False,
                                                    }
                                
            elif event.key == pygame.K_RIGHT:
                if hardDrop == False:
                    if collision(grid, 1, 0) == False:
                        for col in range(len(grid)-2, -1, -1):
                            for row in range(len(grid[col])-1, -1, -1):
                                if grid[col][row]['active'] == True:
                                    grid[col+1][row] = grid[col][row]
                                    grid[col][row] = {
                                                     'colour': GAME_COLOUR,
                                                     'active': False,
                                                     }
                                    
        #to move left and right:
            # check if pieces are next to the block then move
            # continue to move until released


        elif event.type == KEY_DOWN_EVENT:
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                blockFalling()

        elif event.type == HARD_DROP:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                hardDrop = True
                blockFalling()

        #BLOCK FALLING
        elif event.type == MOVE_DOWN_EVENT:
            blockFalling()

    # next tick of STOP_TIMER, stop block

    #STOP MOVING BLOCKS
    bottomStop(grid)
            

    #DRAW
    
    gameBorder = pygame.draw.rect(window, white, (gameX-1, gameY-1, GAME_WIDTH + 2, GAME_HEIGHT + 2))
    gameRect = pygame.draw.rect(window, GAME_COLOUR, (gameX, gameY, GAME_WIDTH, GAME_HEIGHT))
    

    gridX = gameX
    gridY = gameY

    #DRAW GRID TO SCREEN
    for col in range(len(grid)):
        for row in range(len(grid[col])-1):
            pygame.draw.rect(window, grid[col][row]['colour'], (gridX, gridY, blockSize, blockSize))
            gridY += blockSize
        gridX += blockSize
        gridY = gameY

    # pygame.draw.rect(window, white, (gameX-1, gameY+900, GAME_WIDTH + 2, 1))







    pygame.display.update()
    fps.tick(45)



