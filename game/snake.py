# import pygame
# import random

# class Snake(): 
#     def __init__(self):
#         pygame.init()
#         self.screen_info = pygame.display.Info()
#         self.screen_width = self.screen_info.current_w
#         self.screen_height = self.screen_info.current_h
#         # head start position of the snake
#         self.x = self.screen_width/2
#         self.y = self.screen_height/2
#         #body dimensions of the snake
#         self.width = 20
#         self.height = 20
#         self.velocity = 0.05
#         self.direction = "right"
#         # create the game window
#         pygame.display.set_caption("Snake Game")
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

#     def  generate_new_food_position(self):
#         width = 15
#         height = 15
#         x = random.randint(0, self.screen_width-width)
#         y = random.randint(0, self.screen_height-height)
#         return (x, y, width, height)

#     def check_game_over(self):
#         if self.x < 0 or self.x > self.screen_width-self.width:
#             pygame.quit()
#         if self.y < 0 or self.y > self.screen_height-self.height:
#             pygame.quit()
    
#     def move(self):
#         if self.direction == "right":
#             self.x += self.velocity
#             self.check_game_over()
#         elif self.direction == "left":
#             self.x -= self.velocity
#             self.check_game_over()
#         elif self.direction == "up":
#             self.y -= self.velocity
#             self.check_game_over()
#         elif self.direction == "down":
#             self.y += self.velocity
#             self.check_game_over()
    
#     def start_game_loop(self):
#         done = False
#         food = self.generate_new_food_position()
#         while not done:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     done = True
#             keys = pygame.key.get_pressed()
#             if keys[pygame.K_LEFT]:
#                 self.move("left")
#             if keys[pygame.K_RIGHT]:
#                 self.move("right")
#             if keys[pygame.K_UP]:
#                 self.move("up")
#             if keys[pygame.K_DOWN]:
#                 self.move("down")
#             self.screen.fill("black")
#             pygame.draw.rect(self.screen, "white", food)
#             pygame.draw.rect(self.screen, "blue", (self.x, self.y, self.width, self.height))
#             pygame.display.flip()



# game = Snake()
# game.start_game_loop()


import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define Colors
white = (255, 25                , 255)
yellow = (255, 255, 215)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Screen Dimensions
dis_width = 600
dis_height = 400

# Create the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by AI')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame  .font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_list):
    """Draws the snake on the screen."""
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    """Displays a message in the center of the screen."""
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def show_score(score):
    """Displays the current score."""
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def gameLoop():
    """The main game loop containing the logic."""
    game_over = False
    game_close = False

    # Starting position of the snake
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Movement variables
    x1_change = 0
    y1_change = 0

    # Snake body list
    snake_List = []
    Length_of_snake = 1

    # Create food position randomly
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        # Loop for when the player loses (Game Over screen)
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            show_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Event Handling (Keyboard inputs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Check for wall collisions
        if x1 >= dis_width or x1 < 0 or y1 >= dis_lag or y1 < 0: # Note: Logic error fix below
            pass # We use the boundary check logic inside the loop

        # Correct Boundary Logic
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        
        # Draw food
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        # Snake movement logic
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if snake hits itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        show_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        # Control the game speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
gameLoop()
