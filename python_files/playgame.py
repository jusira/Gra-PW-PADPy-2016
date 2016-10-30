
print("River Ride")

#import modul_glowny

import pygame                # importujemy biblioteki pygame
import os 
     
class Enemy_zombie_male:
    def __init__(self):
        self.position_x = 500
        self.position_y = 0
        self.image = [pygame.image.load(os.path.join('zombie_male', 'Walk1.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk2.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk3.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk4.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk5.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk6.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk7.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk8.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk9.png')),
                      pygame.image.load(os.path.join('zombie_male', 'Walk10.png'))]

zombie_male_enemy = Enemy_zombie_male()
        
class IsoGame(object):
    def __init__(self,zombie_male_enemy):
        pygame.init()       # incjalizujemy biblioteke pygame
        screen = pygame.display.set_mode((100,100))
        flag = pygame.DOUBLEBUF    # wlaczamy tryb podwojnego buforowania
 
        # tworzymy bufor na  grafike
        self.surface = pygame.display.set_mode((1500,1000),flag)  # ustalamy rozmiar ekranu
         
        #lista przeciwnikow
        self.enemy_list = [zombie_male_enemy]
            
        #tekstury trawy    
        self.grass_image = pygame.image.load(os.path.join('textures', 'grass.png')) #trawa
        self.grass_positions = [[0,0],[1000,0],[2000,0]] #pozycje trawy
        
        #czcionka coins
        self.font2 = pygame.font.Font(os.path.join('other_data', 'From Cartoon Blocks.ttf'), 50)
        self.actual_coins_status = 0
        self.text_coins = self.font2.render("Coins:", 1, (255, 255, 255))
        
        
        #odmierzamy fragmenty czasu
        self.last = pygame.time.get_ticks()
        self.player_cooldown = 60
        self.licznik = 0 # zmienna pomocnicza do liczenia wejść do ifa i odświeżania
 
        # zmienna stanu gry
        self.gamestate = 1  # 1 - run, 0 - exit
        
        player_image_run = [pygame.image.load(os.path.join('robot_run', 'Run(1).png')), 
                            pygame.image.load(os.path.join('robot_run', 'Run(2).png')), 
                            pygame.image.load(os.path.join('robot_run', 'Run(3).png')),
                            pygame.image.load(os.path.join('robot_run', 'Run(4).png')),
                            pygame.image.load(os.path.join('robot_run', 'Run(5).png')),
                            pygame.image.load(os.path.join('robot_run', 'Run(6).png')),
                            pygame.image.load(os.path.join('robot_run', 'Run(7).png')),
                            pygame.image.load(os.path.join('robot_run', 'Run(8).png'))]
        self.player_image = player_image_run
        self.player_frame = 1 
        self.speed = 3     # szybkosc poruszania duszka
        self.player_x = 50   # pozycja x duszka na ekranie
        self.player_y = 30   # pozycja y duszka na ekranie
                    
            
        self.loop()                             # glowna petla gry
    
    def collision(self,x1,y1,w1,h1,x2,y2,w2,h2): #sprawdza kolizję z duszkiem
        if x1 >= x2+w2: return True
        if x1+w1 <= x2: return True
        if y1 >= y2+h2: return True
        if y1+h1 <= y2: return True
        return False
    
    def screen_collision(self, x,y): #sprawdza kolizję z końcem ekranu
        if x <= -50 or x >= 1320: return True
        if y <= -20 or y >= 800: return True
        return False

    def move(self,dirx,diry):
       """ poruszanie duszkiem """
       dx = self.player_x + (dirx * self.speed)
       dy = self.player_y + (diry * self.speed)
       #if not self.collision(dx,dy,100,100,self.sprite_x,self.sprite_y,100,100): #kolizja z innym duszkiem
       if self.screen_collision(dx,dy):
           return
       self.player_x = dx
       self.player_y = dy
    
    def enemy_move(self):
        """rusza przeciwnikiem"""
        for en in self.enemy_list:
            en.position_x -= 10
            
    def enemy_update(self):
        """usuwa przeciwnikow ktorzy wyszli poza plansze lub zostali zabici"""
        for en in self.enemy_list:
            if en.position_x < -200:
                self.enemy_list.remove(en)
        
    def enemy_refresh(self):
        """odswieza przeciwnikow"""
        for en in self.enemy_list:
           self.surface.blit(en.image[(self.player_frame)% 10],(en.position_x,en.position_y)) 
        
           
         
 
    def player_refresh(self):
        ''' odswieza animacje gracza jezeli minelo wystarczajaco duzo czasu od ostatniego ticka'''
        if self.licznik == 1:
            self.player_frame = (self.player_frame +1) % 1000
        else:
            self.licznik = 1
        self.surface.blit(self.player_image[self.player_frame % 8],(self.player_x,self.player_y)) # umieszczamy gracza
    
    def grass_refresh(self):
        """odswieza pozycje trawy"""
        for i in self.grass_positions:
            self.surface.blit(self.grass_image,i)
            if i[0] > -1000:
                i[0] -= 10
            else:
                i[0] = 2000
                
            
    
    
    def game_refresh(self):
        """odświeża cały ekran gry"""
        now = pygame.time.get_ticks()
        if now - self.last >= self.player_cooldown:
            self.last = now
            self.surface.fill((0,0,0)) # czyscimy ekran, malo wydajne ale wystarczy 
            
            
            
            self.grass_refresh()
            #odswiezamy tlo
            self.surface.blit(self.text_coins, (100,20))
            #odswiezamy coinsy
            self.coins_value = self.font2.render(str(self.actual_coins_status), 1, (255, 255, 255))
            self.surface.blit(self.coins_value, (230,20))
            #odswiezamy przeciwnikow
            self.enemy_move()
            self.enemy_update()
            self.enemy_refresh()
            #odswiezamy gracza
            self.player_refresh()
            
            
    
    def game_exit(self):
        """ funkcja przerywa dzialanie gry i wychodzi do systemu"""
        exit()
 
    def loop(self):
        """ glowna petla gry """
        while self.gamestate==1:           
           for event in pygame.event.get():
               if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                   #self.gamestate = 0
                   exec(open(os.path.join('python_files','game_end.py')).read())
                   exit()
                    
           keys = pygame.key.get_pressed() # odczytujemy stan klawiszy
 
           if keys[pygame.K_s] or keys[pygame.K_DOWN]:
              self.move(0,1)  # ruch w dol
 
           if keys[pygame.K_w] or keys[pygame.K_UP]:
              self.move(0,-1)   # ruch w gore
 
           if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
              self.move(1,0)  # ruch w prawo
 
           if keys[pygame.K_a] or keys[pygame.K_LEFT]:
              self.move(-1,0)   # ruch w lewo
 
                     
           
           

           self.game_refresh()
           
           pygame.display.flip()   # przenosimy bufor na ekran
 
        self.game_exit()
 


if __name__ == '__main__':
   IsoGame(zombie_male_enemy)
   
