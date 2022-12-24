import pygame
from pygame.locals import *
import sys
import random

class Button():
    def __init__(self, x, y, image, scale, text):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.font = pygame.font.Font("font/DoodleJump.ttf", 15)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.rect1 = self.text.get_rect()
        self.rect1.center = (x, y)

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = True
        #if pygame.mouse.get_pressed()[0] == 0:
            #self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        surface.blit(self.text, (self.rect1.x + self.width / 2, self.rect1.y + self.height / 2))
        return action

class DoodleJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("AmeJump")
        pygame_icon = pygame.image.load("assets/left_1.png")
        pygame.display.set_icon(pygame_icon)
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("font/DoodleJump.ttf", 25)
        self.blue = pygame.image.load("assets/blue.png").convert_alpha()
        self.red = pygame.image.load("assets/red.png").convert_alpha()
        self.red_1 = pygame.image.load("assets/red_1.png").convert_alpha()
        self.playerRight = pygame.image.load("assets/right.png").convert_alpha()
        self.playerRight_1 = pygame.image.load("assets/right_1.png").convert_alpha()
        self.playerLeft = pygame.image.load("assets/left.png").convert_alpha()
        self.playerLeft_1 = pygame.image.load("assets/left_1.png").convert_alpha()
        self.spring = pygame.image.load("assets/spring.png").convert_alpha()
        self.spring_1 = pygame.image.load("assets/spring_1.png").convert_alpha()
        self.direction = 0
        self.playerx = 400
        self.playery = 400
        self.platforms = [[400, 500, 0, 0]]
        self.springs = []
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
        self.gameover = False
        self.font1 = pygame.font.SysFont("font/DoodleJump.ttf", 125)
        self.buttonIMG = pygame.image.load("assets/menu_unselected.png").convert_alpha()
        self.startBTN = Button(320, 280, self.buttonIMG, 1, "START")
        self.tutoBTN = Button(320, 360, self.buttonIMG, 1, "HOW TO PLAY")
        self.quitBTN = Button(320, 440, self.buttonIMG, 1, "QUIT")
        self.menuBTN = Button(320, 360, self.buttonIMG, 1, "MENU")
        self.restartBTN = Button(320, 280, self.buttonIMG, 1, "RESTART")
        self.continueBTN = Button(320, 280, self.buttonIMG, 1, "CONTINUE")
        self.backBTN = Button(320, 540, self.buttonIMG, 1, "BACK")
        self.doggo = pygame.image.load("assets/doggo.png").convert_alpha()
        self.doggos = []
        
    def updatePlayer(self):
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.direction = 0

        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.direction = 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 850:
            self.playerx = -50
        elif self.playerx < -50:
            self.playerx = 850
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 10
        if not self.direction:
            if self.jump:
                self.screen.blit(self.playerRight_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerRight, (self.playerx, self.playery - self.cameray))
        else:
            if self.jump:
                self.screen.blit(self.playerLeft_1, (self.playerx, self.playery - self.cameray))
            else:
                self.screen.blit(self.playerLeft, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 10, self.green.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 15
                    self.gravity = 0
                else:
                    p[-1] = 1
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 550:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 1000)
                if platform < 800:
                    platform = 0
                elif platform < 900:
                    platform = 1
                else:
                    platform = 2

                self.platforms.append([random.randint(0, 700), self.platforms[-1][1] - 50, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 1000)
                if check > 900 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.green, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.blue, (p[0], p[1] - self.cameray))
            elif p[2] == 2:
                if not p[3]:
                    self.screen.blit(self.red, (p[0], p[1] - self.cameray))
                else:
                    self.screen.blit(self.red_1, (p[0], p[1] - self.cameray))
    
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.playerRight.get_width(), self.playerRight.get_height())):
                self.jump = 50
                self.cameray -= 50
    
    def generatePlatforms(self):
        on = 600
        while on > -100:
            x = random.randint(0,700)
            platform = random.randint(0, 1000)
            if platform < 800:
                platform = 0
            elif platform < 900:
                platform = 1
            else:
                platform = 2
            self.platforms.append([x, on, platform, 0])
            on -= 50

    def drawGrid(self):
        for x in range(80):
            pygame.draw.line(self.screen, (222,222,222), (x * 12, 0), (x * 12, 600))
            pygame.draw.line(self.screen, (222,222,222), (0, x * 12), (800, x * 12))
    
    def drawDoggo(self):
        if self.score % 5000 == 0 and not self.score == 0:
            self.doggos.append([0, self.cameray, False])
        if len(self.doggos) > 0:
            self.screen.blit(self.doggo, (self.doggos[len(self.doggos) - 1][0], self.doggos[len(self.doggos) - 1][1] - self.cameray))
            if self.doggos[len(self.doggos) - 1][0] >= 650:
                self.doggos[len(self.doggos) - 1][2] = True
            elif self.doggos[len(self.doggos) - 1][0] <= 50:
                self.doggos[len(self.doggos) - 1][2] = False
            if self.doggos[len(self.doggos) - 1][2]:
                self.doggos[len(self.doggos) - 1][0] -= 5
            else:
                self.doggos[len(self.doggos) - 1][0] += 5
                
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 10, self.playerRight.get_height())
            rect = pygame.Rect(self.doggos[len(self.doggos) - 1][0], self.doggos[len(self.doggos) - 1][1], self.doggo.get_width(), self.doggo.get_height())
            if rect.colliderect(player):
                self.gameover = True
                
    def pause(self):
        if not self.gameover:
            clock = pygame.time.Clock()                
            self.paused = True
            while self.paused:
                self.screen.fill((255,255,255))
                clock.tick(60)
                self.drawGrid()
                self.text = self.font1.render("PAUSED", True, (0, 0, 0))
                self.screen.blit(self.text, (480 // 2, 200 // 2))   
                if self.continueBTN.draw(self.screen):
                    self.paused = False
                if self.menuBTN.draw(self.screen):
                    self.gameover = False
                    self.menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.paused = False
                        elif event.key == pygame.K_m:
                            self.cameray = 0
                            self.score = 0
                            self.springs = []
                            self.platforms = [[400, 500, 0, 0]]
                            self.generatePlatforms()
                            self.playerx = 400
                            self.playery = 400
                            self.gameover = False
                            self.menu()   
                pygame.display.update() 
                
    def game_over(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)
            self.drawGrid()
            self.text = self.font1.render("GAME OVER", True, (0, 0, 0))
            self.screen.blit(self.text, (280 // 2, 200 // 2))
            self.text = self.font.render("Highscore: " + str(self.score), True, (0, 0, 0))
            self.screen.blit(self.text, (680 // 2, 400 // 2))
            if self.restartBTN.draw(self.screen):
                self.gameover = False
                self.run()
            if self.menuBTN.draw(self.screen):
                self.gameover = False
                self.menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.gameover:
                        self.gameover = False
                        self.run()
                    elif event.key == pygame.K_m and self.gameover:
                        self.gameover = False
                        self.menu()
            pygame.display.update()
            
                              
    def run(self):
        clock = pygame.time.Clock()
        self.doggos = []
        self.cameray = 0
        self.score = 0
        self.springs = []
        self.platforms = [[400, 500, 0, 0]]
        self.generatePlatforms()
        self.playerx = 400
        self.playery = 400
        while True:
            self.screen.fill((255,255,255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause()

            if self.playery - self.cameray > 600:
                self.gameover = True
            if self.gameover:    
                self.game_over()
            else:
                self.drawGrid()
                self.drawPlatforms()
                self.updatePlayer()
                self.updatePlatforms()
                self.drawDoggo()
                self.screen.blit(self.font.render(str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip() 
            
    def menu(self):
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            self.image = pygame.image.load("assets/logo.png")
            self.screen.blit(self.image, (300, 50))
            clock.tick(60)
            if self.startBTN.draw(self.screen):
                self.run()
            if self.tutoBTN.draw(self.screen):
                self.tutorials()
            if self.quitBTN.draw(self.screen):
                quit()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.run()
            pygame.display.update()
    
    def tutorials(self):
        clock = pygame.time.Clock()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            clock.tick(60)
            if self.backBTN.draw(self.screen):
                self.menu()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update()
            
            
######################            
DoodleJump().menu()
