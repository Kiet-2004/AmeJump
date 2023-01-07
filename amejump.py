import pygame
from pygame.locals import *
import sys
import random
from pygame import mixer

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

class AmeJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("AmeJump")
        pygame_icon = pygame.image.load("assets/left_1.png")
        pygame.display.set_icon(pygame_icon)
        self.green = pygame.image.load("assets/green.png").convert_alpha()
        pygame.font.init()
        pygame.mixer.init()
        self.score = 0
        self.font = pygame.font.Font("font/DoodleJump.ttf", 25)
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
        self.font1 = pygame.font.Font("font/DoodleJump.ttf", 105)
        self.buttonIMG = pygame.image.load("assets/menu_unselected.png").convert_alpha()
        
        self.startBTN = Button(320, 220, self.buttonIMG, 1, "START")
        self.tutoBTN = Button(320, 280, self.buttonIMG, 1, "HOW TO PLAY")
        self.highscoreBTN = Button(320, 340, self.buttonIMG, 1, "HIGHSCORE")
        self.gachaBTN = Button(320, 400, self.buttonIMG, 1, "GACHA")
        self.creditBTN = Button(320, 460, self.buttonIMG, 1, "CREDITS")
        self.quitBTN = Button(320, 520, self.buttonIMG, 1, "QUIT")
        
        self.menuBTN = Button(320, 360, self.buttonIMG, 1, "MENU")
        self.restartBTN = Button(320, 280, self.buttonIMG, 1, "RESTART")
        self.continueBTN = Button(320, 280, self.buttonIMG, 1, "CONTINUE")
        self.continue1BTN = Button(320, 540, self.buttonIMG, 1, "CONTINUE")
        
        self.rollBTN = Button(320, 420, self.buttonIMG, 1, "ROLL")
        self.galleryBTN = Button(320, 480, self.buttonIMG, 1, "GALLERY")
        self.backBTN = Button(320, 540, self.buttonIMG, 1, "BACK")
        
        self.skipBTN = Button(320, 480, self.buttonIMG, 1, "SKIP")
        
        self.doggo = pygame.image.load("assets/doggo.png").convert_alpha()
        self.doggos = []
        self.life = 1
        self.box = pygame.image.load("assets/box.png").convert_alpha()
        self.boxes = []
        self.dogStatus = True
        self.boxStatus = True
        self.rickRolled = pygame.image.load("assets/AmeRolled.png").convert_alpha()
        self.gachaTicket = 0
        
        self.bulletL = pygame.image.load("assets/bulletL.png").convert_alpha()
        self.bulletR = pygame.image.load("assets/bulletR.png").convert_alpha()
        self.bullet = []
        self.rate = 200
        
        self.backgroundNum = 1
    
    def updateHighScore(self):
        scr_list = []
        with open('data/highscore.txt','r') as f:
            for scr in f.read().splitlines():
                scr_list.append(scr)
        for i in range(10):
            if self.score > int(scr_list[i]):
                for j in range(9, i, -1):
                    scr_list[j] = scr_list[j - 1]
                scr_list[i] = self.score
                break
        with open('data/highscore.txt', 'w') as f:        
            for scr in scr_list:
                f.write(str(scr) + "\n")
                
    def updateGachaTicket(self):
        num = 0
        with open('data/gacha_ticket.txt','r') as f:
            for tck in f.read().splitlines():
                num += int(tck) + self.gachaTicket
        with open('data/gacha_ticket.txt', 'w') as f:
            f.write(str(num) + "\n") 
        
    def updatePlayer(self):
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 0.7
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
            rect = pygame.Rect(p[0], p[1], self.green.get_width() - 5, 12)
            player = pygame.Rect(self.playerx, self.playery + self.playerRight.get_height(), self.playerRight.get_width() - 8, 10)
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                if p[2] != 2:
                    self.jump = 18
                    self.gravity = 0
                else:
                    if p[-1] == 0:
                        self.jump = 18
                        self.gravity = 0
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
            if check > 650:
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
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), 10).colliderect(pygame.Rect(self.playerx, self.playery + self.playerRight.get_height() - 10, self.playerRight.get_width(), 10)) and not self.jump:
                self.jump = 30
                self.cameray -= 30
    
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
            
    def drawBackground(self):    
        if self.backgroundNum == -1:
            self.drawGrid()  
        else:
            self.bgIMG = pygame.image.load("assets/bg" + str(self.backgroundNum) + ".jpg").convert_alpha()
            self.screen.blit(self.bgIMG, (0, 0))
    
    def drawDoggo(self):
        if self.score % 5000 == 0 and not self.score % 3000 == 0 and not self.score == 0 and self.dogStatus:
            self.doggos.append([random.randint(100, 700), self.cameray, False])
            self.dogStatus = False
        elif self.score % 5000 != 0:
            self.dogStatus = True
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
                
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 8, self.playerRight.get_height())
            rect = pygame.Rect(self.doggos[len(self.doggos) - 1][0] + 3, self.doggos[len(self.doggos) - 1][1] + 3, self.doggo.get_width() - 3, self.doggo.get_height() - 3)
            if rect.colliderect(player):
                self.gameover = True
    
    def drawBullet(self):
        if self.score >= 10000:
            self.rate = max(10, 200 - (self.score - 10000)// 1000)
            if random.randint(1, self.rate) == 1:
                if random.randint(1,2) == 1:
                    self.bullet.append([0, self.cameray + random.randint(1, 600), 1])
                else:
                    self.bullet.append([800, self.cameray + random.randint(1, 600), 2])
            if len(self.bullet) > 0:
                for b in self.bullet:
                    if b[-1] == 1:
                        self.screen.blit(self.bulletR, [b[0], b[1] - self.cameray])
                        b[0] += 5
                    else:
                        self.screen.blit(self.bulletL, [b[0], b[1] - self.cameray])
                        b[0] -= 5
                    player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 8, self.playerRight.get_height())
                    rect = pygame.Rect(b[0], b[1], self.bulletL.get_width(), self.bulletL.get_height())
                    if rect.colliderect(player):
                        self.gameover = True
    
    def drawGachaBox(self):
        if self.score % 3000 == 0 and not self.score == 0 and self.boxStatus:
            self.boxes.append([random.randint(100, 700), self.cameray])
            self.boxStatus = False
        elif self.score % 3000 != 0:
            self.boxStatus = True
        if len(self.boxes) > 0:
            self.screen.blit(self.box, (self.boxes[len(self.boxes) - 1][0], self.boxes[len(self.boxes) - 1][1] - self.cameray))
            player = pygame.Rect(self.playerx, self.playery, self.playerRight.get_width() - 8, self.playerRight.get_height())
            rect = pygame.Rect(self.boxes[len(self.boxes) - 1][0], self.boxes[len(self.boxes) - 1][1], self.box.get_width(), self.box.get_height())
            if rect.colliderect(player):
                number = random.randint(1, 5)
                if number == 1:
                    self.gameover = True
                elif number == 2:
                    self.life += 1
                elif number == 3:
                    self.gotAmeRolled() 
                elif number == 4:
                    self.gachaTicket += 1  
                else:
                    self.score += 500
                self.boxes.pop(len(self.boxes) - 1)
           
    def gotAmeRolled(self):
        if not self.gameover:
            clock = pygame.time.Clock()     
            pygame.mixer.music.load("sound/rickroll.mp3")
            pygame.mixer.music.play(-1)           
            self.paused = True    
            while self.paused:
                self.screen.blit(self.rickRolled, (0, 0))
                clock.tick(60)
                if self.continue1BTN.draw(self.screen):
                    if self.backgroundNum == -1:
                        pygame.mixer.music.load("sound/game.mp3")
                    else:
                        pygame.mixer.music.load("sound/bgm" + str(self.backgroundNum) + ".mp3")
                    pygame.mixer.music.play(-1)
                    self.paused = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            if self.backgroundNum == -1:
                                pygame.mixer.music.load("sound/game.mp3")
                            else:
                                pygame.mixer.music.load("sound/bgm" + str(self.backgroundNum) + ".mp3")
                            pygame.mixer.music.play(-1)
                            self.paused = False
                pygame.display.update()
                
    def pause(self):
        if not self.gameover:
            clock = pygame.time.Clock()                
            self.paused = True
            while self.paused:
                self.screen.fill((255,255,255))
                clock.tick(60)
                self.drawGrid()
                self.text = self.font1.render("PAUSED", True, (0, 0, 0))
                self.screen.blit(self.text, (400 - self.text.get_width()/2, 200 // 2))   
                if self.continueBTN.draw(self.screen):
                    self.paused = False
                if self.menuBTN.draw(self.screen):
                    self.gameover = False
                    self.menu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            self.paused = False
                        elif event.key == pygame.K_m:
                            self.gameover = False
                            self.menu()   
                pygame.display.update() 
                
    def game_over(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load("sound/gameover.mp3")
        pygame.mixer.music.play(0)
        while True:
            self.screen.fill((255, 255, 255))
            clock.tick(60)
            self.drawGrid()
            self.text = self.font1.render("GAME OVER", True, (0, 0, 0))
            self.screen.blit(self.text, (400 - self.text.get_width()/2, 200 // 2))
            self.text = self.font.render("Highscore: " + str(self.score), True, (0, 0, 0))
            self.screen.blit(self.text, (400 - self.text.get_width()/2, 400 // 2))
            if self.restartBTN.draw(self.screen):
                self.gameover = False
                self.select()
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
        if self.backgroundNum == -1:
            pygame.mixer.music.load("sound/game.mp3")
        else:
            pygame.mixer.music.load("sound/bgm" + str(self.backgroundNum) + ".mp3")
        pygame.mixer.music.play(-1)
        self.doggos = []
        self.boxes = []
        self.bullet = []
        self.life = 3
        self.cameray = 0
        self.score = 0
        self.springs = []
        self.platforms = [[375, 500, 0, 0]]
        self.generatePlatforms()
        self.playerx = 400
        self.playery = 375
        self.rate = 200
        while True:
            self.screen.fill((255,255,255))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause()

            if self.playery - self.cameray > 520:
                self.gameover = True
            if self.gameover and self.life - 1 > 0 :
                self.playery = self.cameray + 260
                self.playerx = 400
                self.stuff = pygame.image.load("assets/right_1.png").convert_alpha()
                self.screen.blit(self.stuff, (self.playerx, self.playery))
                pygame.time.delay(600)
                self.life -= 1
                self.doggos = []
                self.bullet = []
                #self.boxes = []
                self.gameover = False
                self.gravity = 0
                for i in range(-1, -100, -1):
                    if self.platforms[i][1] > self.cameray + 380 and self.platforms[i][2] == 0:
                        self.playerx = self.platforms[i][0] + 25
                        break
            elif self.gameover and self.life == 1:
                self.gachaTicket += self.score // 20000
                self.updateGachaTicket()
                self.updateHighScore()   
                self.game_over()
            else:
                self.drawBackground()
                self.drawPlatforms()
                self.updatePlayer()
                self.updatePlatforms()
                self.drawDoggo()
                self.drawGachaBox()
                self.drawBullet()
                self.screen.blit(self.font.render(" Score: " + str(self.score), -1, (0, 0, 0), (255, 255, 255)), (25, 25))
                self.screen.blit(self.font.render(" Life: " + str(self.life), -1, (0, 0, 0), (255, 255, 255)), (25, 50))
            pygame.display.flip() 
            
    def menu(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.load("sound/menu.mp3")
        pygame.mixer.music.play(-1)
        while True:
            self.screen.fill((255, 255, 255))
            self.image1 = pygame.image.load("assets/ameplaying2.png")
            self.screen.blit(self.image1, (10, 200))
            self.image2 = pygame.image.load("assets/ameplaying.png")
            self.screen.blit(self.image2, (510, 150))
            self.drawGrid()
            self.image = pygame.image.load("assets/logo.png")
            self.screen.blit(self.image, (300, 10))
            clock.tick(60)
            if self.startBTN.draw(self.screen):
                self.select()
            if self.tutoBTN.draw(self.screen):
                self.tutorials()
            if self.highscoreBTN.draw(self.screen):
                self.highscoreDisplay()
            if self.gachaBTN.draw(self.screen):
                self.gachaPage()
            if self.creditBTN.draw(self.screen):
                self.creditPage()
            if self.quitBTN.draw(self.screen):
                sys.exit()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.run()
            pygame.display.update()
    
    def select(self):
        clock = pygame.time.Clock()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            clock.tick(60)
            self.text = self.font1.render("SELECTING", True, (0, 0, 0))
            self.screen.blit(self.text, (400 - self.text.get_width()/2, 100 // 2)) 
            num = []
            with open('data/gacha.txt','r') as f:
                for tck in f.read().splitlines():
                    num.append(int(tck))
            for i in range(len(num)):
                if num[i] == 0:
                    self.image = pygame.image.load("gacha_img/LOCKED.png").convert_alpha()
                    self.screen.blit(self.image, (30 + 150 * i, 250))
                else:
                    self.image = pygame.image.load("gacha_img/" + str(i+1) + ".png").convert_alpha()
                    self.screen.blit(self.image, (30 + 150 * i, 250))
                    rect = pygame.Rect(30 + 150 * i, 250, self.image.get_width(), self.image.get_height())
                    pos = pygame.mouse.get_pos()
                    if rect.collidepoint(pos):
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                self.backgroundNum = i + 1
                                self.run()
            if self.skipBTN.draw(self.screen):
                self.backgroundNum = -1
                self.run()
            if self.backBTN.draw(self.screen):
                self.menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update() 
    
    def tutorials(self):
        clock = pygame.time.Clock()
        self.tuto = pygame.image.load("assets/tutorials.png").convert_alpha()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            self.screen.blit(self.tuto, (10, 10))
            clock.tick(60)
            if self.backBTN.draw(self.screen):
                self.menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update()
            
    def highscoreDisplay(self):
        clock = pygame.time.Clock()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            clock.tick(60)
            scr_list = []
            with open('data/highscore.txt','r') as f:
                for scr in f.read().splitlines():
                    scr_list.append(scr)
            self.text = self.font1.render("HIGHSCORE", True, (0, 0, 0))
            self.screen.blit(self.text, (400 - self.text.get_width()/2, 200 // 2))
            h = 200
            for scr in scr_list:
                self.text = self.font.render(scr, True, (0, 0, 0))
                self.screen.blit(self.text, (375, h))
                h += 25
            if self.backBTN.draw(self.screen):
                self.menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update()
            
    def gachaPage(self):
        self.image = pygame.image.load("gacha_img/LOCKED.png").convert_alpha()
        self.text2 = self.font1.render("", True, (0, 0, 0))
        clock = pygame.time.Clock()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            clock.tick(60)
            self.text = self.font1.render("GACHA STORE", True, (0, 0, 0))
            self.screen.blit(self.text, (400 - self.text.get_width()/2, 100 // 2))
            self.screen.blit(self.image, (330, 200))
            self.screen.blit(self.text2, (120, 250))
            num = 0
            with open('data/gacha_ticket.txt','r') as f:
                for tck in f.read().splitlines():
                    num = int(tck)
            check = []
            with open('data/gacha.txt','r') as f:
                for tck in f.read().splitlines():
                    check.append(int(tck))
            self.text = self.font.render("Ticket: " + str(num), True, (0, 0, 0))
            self.screen.blit(self.text, (375, 160))         
            if self.backBTN.draw(self.screen):
                self.menu()
            if self.rollBTN.draw(self.screen):
                #############################################
                if num == 0:
                    self.text2 = self.font1.render("OUT OF TICKET", True, (0, 0, 0))
                    self.image = pygame.image.load("gacha_img/LOCKED.png").convert_alpha()
                else:
                    num -= 1
                    ran = random.randint(1,100)
                    if ran <= 5:    
                        self.image = pygame.image.load("gacha_img/" + str(ran) + ".png").convert_alpha()
                        check[ran - 1] = 1
                    else:
                        self.image = pygame.image.load("gacha_img/TACH.png").convert_alpha()
                    with open('data/gacha_ticket.txt', 'w') as f:
                        f.write(str(num) + "\n")
                    with open('data/gacha.txt', 'w') as f:        
                        for chk in check:
                            f.write(str(chk) + "\n")
                #############################################

            if self.galleryBTN.draw(self.screen):
                self.gallery()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update()
            
    def gallery(self):
        clock = pygame.time.Clock()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            clock.tick(60)
            self.text = self.font1.render("GALLERY", True, (0, 0, 0))
            self.screen.blit(self.text, (400 - self.text.get_width()/2, 100 // 2)) 
            num = []
            with open('data/gacha.txt','r') as f:
                for tck in f.read().splitlines():
                    num.append(int(tck))
            for i in range(len(num)):
                if num[i] == 0:
                    self.image = pygame.image.load("gacha_img/LOCKED.png").convert_alpha()
                    self.screen.blit(self.image, (30 + 150 * i, 250))
                else:
                    self.image = pygame.image.load("gacha_img/" + str(i+1) + ".png").convert_alpha()
                    self.screen.blit(self.image, (30 + 150 * i, 250))
            
                     
            if self.backBTN.draw(self.screen):
                self.gachaPage()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update()
    
    def creditPage(self):
        clock = pygame.time.Clock()
        self.credit = pygame.image.load("assets/credit.png").convert_alpha()
        while True: 
            self.screen.fill((255, 255, 255))
            self.drawGrid()
            self.screen.blit(self.credit, (10, 10))
            clock.tick(60)
            if self.backBTN.draw(self.screen):
                self.menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        self.menu()
            pygame.display.update()        
            
######################            
AmeJump().menu()
