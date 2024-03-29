import random
import pygame 
from sys import exit
from random import randint, choice

from pygame.sprite import Group


#surface and rec combined
class Player(pygame.sprite.Sprite):
   def __init__(self):
      super().__init__()
      player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
      player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
      self.player_walk = [player_walk_1, player_walk_2]
      self.player_index = 0 #pick one surface or the other 
      self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

      self.image = self.player_walk[self.player_index]
      self.rect = self.image.get_rect(midbottom = (100, 300))
      self.gravity = 0
      self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
      self.jump_sound.set_volume(0.5)

   def player_input(self):
      keys = pygame.key.get_pressed()
      if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
         self.gravity = -20 
         self.jump_sound.play()


   def apply_gravity(self): 
      self.gravity += 1
      self.rect.y += self.gravity
      if self.rect.bottom >= 300: 
         self.rect.bottom = 300

   def animation_state(self) : 
      if self.rect.bottom < 300 : 
         self.image = self.player_jump
      else:
         self.player_index += 0.1
         if self.player_index >= len(self.player_walk):
            self.player_index = 0
         self.image = self.player_walk[int(self.player_index)]

   def update(self): 
      self.player_input()
      self.apply_gravity()
      self.animation_state()


class Obstacle(pygame.sprite.Sprite):
   def __init__(self, type):
      super().__init__() #important

      if type == 'fly':
         fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
         fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
         self.frames = [fly_1, fly_2]
         y_pos = 210
      else : 
         snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #remove alpha value
         snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() #remove alpha value
         self.frames = [snail_1, snail_2]
         y_pos = 300
      self.animation_index = 0

      #mandatory 
      self.image = self.frames[self.animation_index]
      self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

   def animation_state(self):
    self.animation_index += 0.1
    if self.animation_index >= len(self.frames):
        self.animation_index = 0
    self.image = self.frames[int(self.animation_index)]

   def update(self): 
      self.animation_state()
      self.rect.x -= 6
      self.destroy()

   def destroy(self): 
      if self.rect.x <= -100:
         self.kill()



      




pygame.init() #necessary to run, starts pygame 


#update score on every frame, put that on surface, display surface 
def display_score(): 
    current_time = int((pygame .time.get_ticks() - start_time) / 1000) #gives the time the game has been running in milliseconds 
    score_surf = text_font.render(f'Score: {current_time}', False,(64,64,64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)  
    return current_time
 

def obstacle_movement(obstacle_list):
   if obstacle_list:
      for obstacle_rect in obstacle_list:
         obstacle_rect.x -= 5

         if obstacle_rect.bottom == 300:
            screen.blit(snail_surf, obstacle_rect)
         else: 
            screen.blit(fly_surf, obstacle_rect)

      obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
      
      return obstacle_list
   else: return []


def collisions(player, obstacles):
   if obstacles : 
      for obstacle_rect in obstacles : 
         if player.colliderect(obstacle_rect):
            return False
   return True

def collision_sprite():
   if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
      obstacle_group.empty()
      return False #sprite, group, boolean
   else : 
      return True

def player_animation():
   global player_surf, player_index
   if player_rect.bottom < 300 : 
      player_surf = player_jump
   else : 
      player_index += 0.1
      if player_index >= len(player_walk) : 
         player_index = 0
      player_surf = player_walk[int(player_index)]
   #play walking animation if player is on floor 
   #display jump surface when player not on floor
   
   


#display screen
screen = pygame.display.set_mode((800, 400)) #width and height of screen being displayed
pygame.display.set_caption('Runner') #set title of the game
clock = pygame.time.Clock() #time of each frame
#create font (font type, font size), create surface then blit it
text_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False #if the game is on 
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops = -1) #loop forever


#create one group for the player
player = pygame.sprite.GroupSingle()
player.add(Player())

#groups for obstacle 
obstacle_group = pygame.sprite.Group()



sky_surface = pygame.image.load('graphics/Sky.png').convert() #import an image, convert it to something read easily
ground_surface = pygame.image.load('graphics/ground.png').convert()

#score_surf = test_font.render('My Game', False, (64,64,64)) #text, antialias, color
#score_rect = score_surf.get_rect(center = (400, 50))


#obstacles
#create snail 
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #remove alpha value
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha() #remove alpha value
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]


fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []




#player
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0 #pick one surface or the other 
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300)) #create rectangle, takes surface and draws around it
player_gravity = 0 #implement gravity 

#game over screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand) #rescaling (surface, (width, height))
player_stand_rect = player_stand.get_rect(center=(400,200))

#intro screen 
game_name = text_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = text_font.render("Press Space to Run", False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))

#timer 
obstacle_timer = pygame.USEREVENT + 1 #avoid conflict 
pygame.time.set_timer(obstacle_timer, 1500) #event, how often in millisecond

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True : #run game forever until we decide inside to end it
    for event in pygame.event.get(): #get events from user
        #close window 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit() #breaks from all code


        if game_active : 
         

         #collision with mousemotion

         if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                player_gravity = -21.5

         #pressed button then make it specific 
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                player_gravity = -21.5 #if positive goes down but if neg goes up
        else : 
           if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE:
                 game_active = True
                 start_time = pygame.time.get_ticks()

    if game_active :   
          
        if event.type == obstacle_timer: 
           obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
           #if randint(0,2):
            #obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900, 1100), 300)))
           #else:
              #obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900, 1100), 210)))

        if event.type == snail_animation_timer : 
           if snail_frame_index == 0:
              snail_frame_index = 1
           else: 
              snail_frame_index = 0
           snail_surf = snail_frames[snail_frame_index]

        if event.type == fly_animation_timer : 
           if fly_frame_index == 0:
              fly_frame_index = 1
           else: 
              fly_frame_index = 0
           fly_surf = fly_frames[fly_frame_index]

        

    #draw all our elements
    #update everything 

    if game_active:
     
      screen.blit(sky_surface, (0,0)) #put one surface on another surface, (surface, position)
      screen.blit(ground_surface, (0, sky_surface.get_height()))
      score = display_score()
      
      #snail_rect.right -= 4
      #if snail_rect.right <= 0 : 
        # snail_rect.left = 800 #make it come again and again
        # screen.blit(snail_surface, snail_rect)
      
      #player going down after jumping
      #player_gravity += 1
      #player_rect.y += player_gravity
      #check if goes below ground 
      #if player_rect.bottom >= 300 : 
       #  player_rect.bottom = 300
      #player_animation()
      #screen.blit(player_surf, player_rect) #taking player and placing it position of rect´
      player.draw(screen)
      player.update() #groups have draw and update functions, call update method

      obstacle_group.draw(screen)
      obstacle_group.update()


      game_active = collision_sprite()



      #obstacles movement
      #obstacle_rect_list = obstacle_movement(obstacle_rect_list)
      #game_active = collisions(player_rect, obstacle_rect_list) 

    else : 
      screen.fill((94,129,162))
      screen.blit(player_stand, player_stand_rect)
      obstacle_rect_list.clear()
      player_rect.midbottom = (80, 300)
      player_gravity = 0

      #score 
      score_message = text_font.render(f'Your score: {score}', False, (111,196,169))
      score_message_rect = score_message.get_rect(center = (400, 330))

      screen.blit(game_name, game_name_rect)


      if score == 0:
         screen.blit(game_message, game_message_rect)
      else: 
         screen.blit(score_message, score_message_rect)

    pygame.display.update() #updates display surface
    clock.tick(60) #true loop should not run more than that, not too fast, 60 times per second