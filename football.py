import math
import random
import pygame

class player:
    def __init__(self): 
        self.x = None
        self.y = None
        self.goal_x = None
        self.goal_y = None
        self.huristic = None
        self.team = None
        self.playerNumber = None

class ball:
    def __init__(self): 
        self.x = None
        self.y = None
        self.redious = 4
        self.color = (0,0,0)


class football_game:

    def __init__(self): 
        self.width = 400 # Take even no for proper formating 
        self.height = 550 # Take even no for proper formating
        self.goal_width = 80 # Take even no for proper formating
        self.offset = 20
        self.height_offset = 5
        self.width_offset = 4
        self.circle_redious = 30
        self.image_redious = 15
        self.background_color = (56,118,29)  # Green Color
        self.grid_color = (255,255,255) # White color of greed
        self.team1_color = (255,0,0) # RED color, Team 1 Goal post color
        self.team2_color = (7,55,99) # Blue color, Team 2 Goal post color
        self.boll_color = (255,255,255) # White color of ball
        self.screen = None
        self.players = []
        self.goal_box_x = (self.width // self.width_offset + 2 * self.image_redious, self.width - self.width // self.width_offset - 2 * self.image_redious)
        self.goal_box_y = (self.offset + 2 * self.image_redious, self.height // self.height_offset - 2 * self.image_redious)
        self.goal_box_out_x = (self.offset + 2 * self.image_redious, self.width - self.offset - 2 * self.image_redious)
        self.goal_box_out_y = (self.height // self.height_offset + 2 * self.image_redious, self.height // 2 - 2 * self.image_redious)
        self.goal_x = (self.width // 2 - self.goal_width // 2, self.width // 2 + self.goal_width // 2)
        self.goal_y = (self.offset, self.offset)
        self.centerPlayer = None
        self.huristic = [self.height for i in range(9)]
        self.ball = ball()
        self.bestPlayer = None
        self.movingOffset = None


    def createScreen(self):
        #print(self.goal_box_x, self.goal_box_y, self.goal_box_out_x, self.goal_box_out_y)
        self.screen = pygame.display.set_mode((self.width, self.height))  # Creates screen objec()
        
        self.initGame()

        clock = pygame.time.Clock() # creating a clock object

        flag = True
        # STARTING MAIN LOOP
        count = 0
        step = 0
        while flag:
            pygame.time.delay(50)  # This will delay the game so it doesn't run too quickly
            clock.tick(10)  # Will ensure our game runs at 10 FPS
            pygame.display.update()  # Updates the screen
            if step < 2:
                if count +4 >= self.movingOffset[2]:
                    if step < 1:
                        self.movingOffset = self.computeMovingOffset(self.bestPlayer, False)
                    count = -8
                    step += 1
                count += 1
                self.ball.x -= self.movingOffset[0]
                self.ball.y -= self.movingOffset[1]
                self.screen.fill(self.background_color) # Screen color setting
                self.createLayout() # Ground Layout creation
                self.printPlayer()
                pygame.draw.circle(self.screen, self.ball.color, (self.ball.x, self.ball.y), self.ball.redious)
            else: 
                self.initGame()
                count = 0
                step = 0
        


    def initGame(self):
        self.createPlayers()
        self.bestPlayer = self.playGame()
        self.movingOffset = self.computeMovingOffset(self.bestPlayer, True)

        self.screen.fill(self.background_color) # Screen color setting
        self.createLayout() # Ground Layout creation
        self.printPlayer()
        # Ball
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        pygame.draw.circle(self.screen, self.ball.color, (self.ball.x, self.ball.y), self.ball.redious)
        

    def createLayout(self):
        # Center Circle
        pygame.draw.circle(self.screen, self.grid_color, (self.width // 2, self.height // 2), self.circle_redious)
        pygame.draw.circle(self.screen, self.background_color, (self.width // 2, self.height // 2), self.circle_redious - 1)
        # Vertical Line outer
        self.drawLine((self.offset, self.offset), (self.offset, self.height - self.offset))
        self.drawLine((self.width - self.offset, self.offset),(self.width - self.offset, self.height - self.offset))
        # Horigental line outer
        self.drawLine((self.offset, self.offset), (self.width - self.offset, self.offset))
        self.drawLine((self.offset, self.height - self.offset), (self.width - self.offset, self.height - self.offset))
        # Center line
        self.drawLine((self.offset, self.height // 2), (self.width - self.offset, self.height // 2))
        # Inner Line 1
        self.drawLine((self.width // self.width_offset, self.height // self.height_offset), (self.width - self.width // self.width_offset, self.height // self.height_offset)) # horigental
        self.drawLine((self.width // self.width_offset, self.offset), (self.width // self.width_offset, self.height // self.height_offset)) # vertical
        self.drawLine((self.width - self.width // self.width_offset, self.offset), (self.width - self.width // self.width_offset, self.height // self.height_offset)) # vertical
        # Inner Line 2
        self.drawLine((self.width // self.width_offset, self.height - self.height // self.height_offset), (self.width - self.width // self.width_offset, self.height - self.height // self.height_offset)) # horigental
        self.drawLine((self.width // self.width_offset, self.height - self.offset), (self.width // self.width_offset, self.height - self.height // self.height_offset)) # vertical
        self.drawLine((self.width - self.width // self.width_offset, self.height - self.offset), (self.width - self.width // self.width_offset, self.height - self.height // self.height_offset)) # vertical
        # goal post
        pygame.draw.rect(self.screen, self.team1_color, pygame.Rect(self.width // 2 - self.goal_width // 2, 0, self.goal_width, self.offset))
        pygame.draw.rect(self.screen, self.team2_color, pygame.Rect(self.width // 2 - self.goal_width // 2, self.height - self.offset, self.goal_width, self.offset))
        
    def drawLine(self, point1, point2):
        #print( point1, point2)
        #print('------------------')
        pygame.draw.line(self.screen, self.grid_color, point1, point2)

    def displayImage(self, point, name):
        image = pygame.image.load(name)
        self.screen.blit(image, point)

    def createPlayers(self):
        self.players = []
        # Center Player
        self.centerPlayer = self.initPlayer(self.width // 2, self.height // 2 + self.image_redious, 2, -1)
        self.players.append(self.centerPlayer)
        # Inner Player
        self.players.append(self.initPlayer(random.randint(self.goal_box_x[0], self.goal_box_x[1]), random.randint(self.goal_box_y[0], self.goal_box_y[1]), 1, 1))
        self.players.append(self.initPlayer(random.randint(self.goal_box_x[0], self.goal_box_x[1]), random.randint(self.goal_box_y[0], self.goal_box_y[1]), 2, 2))
        # Outer Player
        for i in range(6):
            self.players.append(self.initPlayer(random.randint(self.goal_box_out_x[0], self.goal_box_out_x[1]), random.randint(self.goal_box_out_y[0], self.goal_box_out_y[1]), 1 + i // 3, i+3))
        
    def initPlayer(self, x, y, team, playerNumber):
        p = player()
        p.x = x 
        p.y = y
        p.team = team
        p.playerNumber = playerNumber
        if x < self.goal_x[0]:
            p.goal_x = self.goal_x[0]
            p.goal_y = self.goal_y[0]
            p.huristic = math.sqrt((x - self.goal_x[0]) ** 2 + (y - self.goal_y[0]) ** 2)
        elif x > self.goal_x[1]:
            p.goal_x = self.goal_x[1]
            p.goal_y = self.goal_y[1]
            p.huristic = math.sqrt((x - self.goal_x[1]) ** 2 + (y - self.goal_y[1]) ** 2)
        else:
            p.goal_x = x
            p.goal_y = self.goal_y[0]
            p.huristic = y - self.offset

        if self.centerPlayer != None and self.centerPlayer.team == team:
            self.huristic[playerNumber] = math.sqrt((x - self.centerPlayer.x) ** 2 + (y - self.centerPlayer.y) ** 2)
        
        return p

    def printPlayer(self):
        for p in self.players:
            self.displayImage((p.x-self.image_redious, p.y-self.image_redious), 'team_'+str(p.team)+'_player.png')

    def playGame(self):
        bestPlayer = None
        cost = self.height
        for p in self.players:
            if self.centerPlayer.team == p.team and p.playerNumber != self.centerPlayer:
                c = p.huristic + self.huristic[p.playerNumber]
                if cost > c:
                    bestPlayer = p
                    cost = c
        
        self.drawLine((self.centerPlayer.x, self.centerPlayer.y), (bestPlayer.x, bestPlayer.y))
        self.drawLine((bestPlayer.x, bestPlayer.y), (bestPlayer.goal_x, bestPlayer.goal_y))
        return bestPlayer

        # pygame.draw.line(surface, color, start_pos, end_pos, width)

    def computeMovingOffset(self, player, isCenterPlayer):
        x = 0
        y = 0
        cost = 0
        if isCenterPlayer:
            cost = self.huristic[player.playerNumber]
            x = self.centerPlayer.x - player.x
            y = self.centerPlayer.y - player.y
        else:
            cost = player.huristic
            x = player.x - player.goal_x
            y = player.y - player.goal_y
        cost = int(cost) // 4
        return (float(format(x/cost, '.4f')), float(format(y/cost, '.4f')), cost)

fg = football_game()
fg.createScreen()