from pickle import TRUE
import pygame
import random

pygame.init()
blockSize = 45
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
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
purple = pygame.Color(145, 0, 170)

GAME_COLOUR = black


#GRID SETUP
grid = []
for i in range(10):
    row = [] 
    for j in range(20):
        row.append({
            'colour': GAME_COLOUR,
            'active': False,
        })
    grid.append(row)

#STOP MOVING BLOCKS
def bottomStop(grid):
    for col in range(len(grid)):
        if grid[col][19]['active'] == True:
            for col in range(len(grid)):
                for row in range(len(grid[col])):
                    grid[col][row]['active'] = False

#COLLISIONS
def collision(grid, colShift, rowShift):
    # Loop through to find active pieces
    for col in range(len(grid)):
        for row in range(len(grid[col])-1):
            if grid[col][row]['active'] == True:
    
    # what it should return (return a TRUE or FALSE)
                if (grid[col + colShift][row + rowShift]['colour'] != GAME_COLOUR and 
                    grid[col + colShift][row + rowShift]['active'] == False):
                        return True
                    
    return False


#VARIABLES
gameX = int(WINDOW_WIDTH / 2 - GAME_WIDTH / 2)
gameY = int(WINDOW_HEIGHT / 2 - GAME_HEIGHT / 2)


MOVE_DOWN_EVENT = pygame.USEREVENT + 1


pygame.time.set_timer(MOVE_DOWN_EVENT, 200)


grid[0 + 4][19]['colour'] = orange
grid[1 + 4][19]['colour'] = orange
grid[2 + 4][19]['colour'] = orange
grid[2 + 4][18]['colour'] = orange

# grid[5][0+2]['colour'] = blue
# grid[5][0+2]['active'] = True
# grid[5][1+2]['colour'] = blue
# grid[5][1+2]['active'] = True
# grid[5][2+2]['colour'] = blue
# grid[5][2+2]['active'] = True
# grid[5][3+2]['colour'] = blue
# grid[5][3+2]['active'] = True 

grid[0+2][5]['colour'] = blue
grid[0+2][5]['active'] = True
grid[1+2][5]['colour'] = blue
grid[1+2][5]['active'] = True
grid[2+2][5]['colour'] = blue
grid[2+2][5]['active'] = True
grid[3+2][5]['colour'] = blue
grid[3+2][5]['active'] = True 

# grid[9][1]['colour'] = purple
# grid[8][1]['colour'] = purple
# grid[7][1]['colour'] = purple
# grid[8][0]['colour'] = purple


#GAME START

while running:  
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
                print(collision(grid, -1, 0))
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
            # check for active block and shift left or right
            # check if pieces are next to the block then move
            # continue to move until released
            # 

        #BLOCK FALLING
        elif event.type == MOVE_DOWN_EVENT:
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
    
    #STOP MOVING BLOCKS
    bottomStop(grid)
            


    #DRAW
    
    gameBorder = pygame.draw.rect(window, white, (gameX-1, gameY-1, GAME_WIDTH + 2, GAME_HEIGHT + 2))
    gameRect = pygame.draw.rect(window, GAME_COLOUR, (gameX, gameY, GAME_WIDTH, GAME_HEIGHT))
    
    gridX = gameX
    gridY = gameY

    #DRAW GRID TO SCREEN
    for col in range(len(grid)):
        for row in range(len(grid[col])):
            pygame.draw.rect(window, grid[col][row]['colour'], (gridX, gridY, blockSize, blockSize))
            gridY += blockSize
        gridX += blockSize
        gridY = gameY



    pygame.display.update()
    fps.tick(264)