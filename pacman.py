#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
#import pygame._view
from asyncio.windows_events import NULL
from turtle import width
import pygame
import time


  
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow   = ( 255, 255, 0)


Pacman_icon = pygame.image.load('images/pacman.png')

pygame.display.set_icon(Pacman_icon)

#Add music
#pygame.mixer.init()
#pygame.mixer.music.load('pacman.mp3')
#pygame.mixer.music.play(-1, 0.0)


# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [0,0,6,600],
              [0,0,600,6],
              [0,600,606,6],
              [600,0,6,606],
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6]
            ]
     
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)
         
    # return our new list
    return wall_list

def setupGate(all_sprites_list):
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
  
    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y

#Inheritime Player klassist
class Ghost(Player):
  # These to variable keep track of the turns and steps of its ghost/virus
    ghost_turn  = 0
    ghost_step  = 0

    # Change the speed of the ghost
    def changespeed(self,list,ghost,turn,steps,l):
      try:
        z=list[turn][2]
        if steps < z:
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps+=1
        else:
          if turn < l:
            turn+=1
          elif ghost == "clyde":
            turn = 2
          else:
            turn = 0
          self.change_x=list[turn][0]
          self.change_y=list[turn][1]
          steps = 0
        return [turn,steps]
      except IndexError:
         return [0,0]

Pinky_directions = [
[0,-30,4],
[15,0,9],
[0,15,11],
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Pinky_directions)-1
bl = len(Blinky_directions)-1
il = len(Inky_directions)-1
cl = len(Clyde_directions)-1


# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Pacman')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)


clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#default locations for Pacman and monstas
w = 303-16 #Width
p_h = (7*60)+19 #Pacman height
m_h = (4*60)+19 #Monster height
b_h = (3*60)+19 #Binky height
i_w = 303-16-32 #Inky width
c_w = 303+(32-16) #Clyde width




def startGame():

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)



  pinky_list = pygame.sprite.RenderPlain()

  blinky_list = pygame.sprite.RenderPlain()
  
  inky_list = pygame.sprite.RenderPlain()

  clyde_list = pygame.sprite.RenderPlain()
  
  
  # The turn and step variables are deleted and intsead the Ghost class will keep track of turns and steps
  # of the individual ghost/virus


  # Create the player paddle object
  Pacman = Player( w, p_h, "images/pacman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
  
  # Creates the first of each viruses and add them to their lists
  Blinky=Ghost( w, b_h, "images/Blinky.png" )
  blinky_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "images/Pinky.png" )
  pinky_list.add(Pinky)
  all_sprites_list.add(Pinky)

  Inky=Ghost( i_w, m_h, "images/Inky.png" )
  inky_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "images/Clyde.png" )
  clyde_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0
  infect  =  0 
  done = False

  i = 0


  p_delay = 0
  b_delay = 0
  i_delay = 0
  c_delay = 0
  

  time_start = pygame.time.get_ticks()



  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,-30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,30)

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  Pacman.changespeed(30,0)
              if event.key == pygame.K_RIGHT:
                  Pacman.changespeed(-30,0)
              if event.key == pygame.K_UP:
                  Pacman.changespeed(0,30)
              if event.key == pygame.K_DOWN:
                  Pacman.changespeed(0,-30)
          
      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)

    # The 4 for loops loops through each virus list and moves the virus

      #for pink in pinky_list:
      for p_temp in pinky_list:
        returned = p_temp.changespeed(Pinky_directions,False,p_temp.ghost_turn,p_temp.ghost_step, pl )
        p_temp.ghost_turn = returned[0]
        p_temp.ghost_step = returned[1]
        p_temp.changespeed(Pinky_directions,False,p_temp.ghost_turn,p_temp.ghost_step,  pl )
        p_temp.update(wall_list,False)


      #blinky_list
      for b_temp in blinky_list:
        returned = b_temp.changespeed(Blinky_directions, False, b_temp.ghost_turn, b_temp.ghost_step, bl)
        b_temp.ghost_turn = returned[0]
        b_temp.ghost_step = returned[1]
        b_temp.changespeed(Blinky_directions, False, b_temp.ghost_turn, b_temp.ghost_step, bl)
        b_temp.update(wall_list,False)

      #inky_list
      for i_temp in inky_list:
        returned = i_temp.changespeed(Inky_directions, False, i_temp.ghost_turn, i_temp.ghost_step, il )
        i_temp.ghost_turn = returned[0]
        i_temp.ghost_step = returned[1]
        i_temp.changespeed(Inky_directions, False, i_temp.ghost_turn, i_temp.ghost_step,  il )
        i_temp.update(wall_list,False)

      # clyde_list
      for c_temp in clyde_list:
        returned = c_temp.changespeed(Clyde_directions, "clyde", c_temp.ghost_turn, c_temp.ghost_step, cl )
        c_temp.ghost_turn = returned[0]
        c_temp.ghost_step = returned[1]
        c_temp.changespeed(Clyde_directions, "clyde", c_temp.ghost_turn, c_temp.ghost_step,  cl )
        c_temp.update(wall_list,False)



    # See if the Pacman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
      pinky_hit_list = pygame.sprite.spritecollide(Pacman, pinky_list, True)
      blinky_hit_list =  pygame.sprite.spritecollide(Pacman, blinky_list, True)
      inky_hit_list =  pygame.sprite.spritecollide(Pacman, inky_list, True)
      clyde_hit_list =  pygame.sprite.spritecollide(Pacman, clyde_list, True)

      

      # Check the list of block collisions, to later update the score.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)



    # Check if time has reached 30 seconds to add a new virus
      # get_ticks - time_start == (total time of since pygame was initialized) MINUS (when the new round started)
      # get_ticks will get numbers close to 30 and not exact (ex: 0.001, 0.093, 0.193)

      # the delay variables keep track of how many viruses to add and the type of virus
      if (pygame.time.get_ticks() - time_start) // 100  % 300 == 0   and (pygame.time.get_ticks() - time_start)//1000 != 0:
        # the delay variables is multipled by two so that the for-loop can check it and add viruses
        # in every other iteration in the while loop 
        p_delay = len(pinky_list) * 2
        b_delay = len(blinky_list) * 2
        i_delay = len(inky_list) * 2
        c_delay = len(clyde_list) * 2
        

      # After getting the number of viruses to duplicate after the correct amount of seconds (30s) has passed.
      # p_delay will add a ghost every-other iteration of the while loop
      
      #     NO -> if you try to do a for/while loop in the main loop to add the viruses all at once, the sprits
      #           will be added on top of each other and will look like only one ghost was added. 
      
      # Not a bug - the same-type viruses are added close to each other, because it adds another level of 
      #             strategy to the game where you have to choose between chasing after an individual virus 
      #             or a group of very close together viruses or collect the dots.
      
      if p_delay > 0 and p_delay%2 == 0:
        temp_Pinky = Ghost( w, m_h, "images/Pinky.png" )
        pinky_list.add(temp_Pinky)
        all_sprites_list.add(temp_Pinky)
      p_delay -= 1
      
      # Add a extra blinky for every existing blinky
      # Added everyother iteration of the while loop
      if b_delay > 0 and b_delay%2 == 0:
        temp_Blinky = Ghost( w, b_h, "images/Blinky.png" )
        blinky_list.add(temp_Blinky)
        all_sprites_list.add(temp_Blinky)
      b_delay -= 1

      # Add a extra inky for every existing inky
      # Added everyother iteration of the while loop
      if i_delay > 0 and i_delay%2 == 0:
        temp_inky = Ghost( i_w, m_h, "images/Inky.png" )
        inky_list.add(temp_inky)
        all_sprites_list.add(temp_inky)
      i_delay -= 1

      # Add a extra clyde for every existing clyde
      # Added everyother iteration of the while loop
      if c_delay > 0 and c_delay%2 == 0:
        temp_clyde = Ghost( c_w, m_h, "images/Clyde.png" )
        clyde_list.add(temp_clyde)
        all_sprites_list.add(temp_clyde)
      c_delay -= 1
      

      infect = len(pinky_list) + len(blinky_list) + len(inky_list) + len(clyde_list)


      ######################################################################################################
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)


    # Score to the top left of the screen
      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

    # Infection counter to the top right of the screen
      text=font.render("Infection: "+str(infect), True, red)
      screen.blit(text, [400, 10])

    # Timer counter to the bottom left of the screen
      text=font.render("Timer: "+ str(  (pygame.time.get_ticks() - time_start) // 1000   ), True, red)  
      screen.blit(text, [10, 580])


      if score == bll:
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if infect >= 32:
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)



      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()
          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            
            startGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()