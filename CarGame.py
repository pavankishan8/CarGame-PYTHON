import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Racing Game")

# Load the background image
background_image = pygame.image.load("D:\\My Projs\\Python\\CarGame-PYTHON\\Images\\high.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Load the car image and scale it
car_image = pygame.image.load("D:\\My Projs\\Python\\CarGame-PYTHON\\Images\\cartopview.png")

car_width, car_height = car_image.get_width(), car_image.get_height()
car_scale = 0.10  # Scale factor for the car image
car_image = pygame.transform.scale(car_image, (int(car_width * car_scale), int(car_height * car_scale)))
car_width, car_height = car_image.get_width(), car_image.get_height()

# Initialize font
font = pygame.font.Font(None, 36)  # You can change the font and size here

# Initialize variables for distance calculation
distance = 0
distance_text = font.render(f"Distance: {int(distance)} km", True, (255, 255, 255))
distance_rect = distance_text.get_rect(center=(screen_width // 2, 30))  # Position the text at the top center

# Class for obstacles
class Obstacle:
    def __init__(self, x, width):
        self.width = width
        self.height = 20
        self.x = x
        self.y = random.randint(-screen_height, 0)
        self.color = (255, 0, 0)
        self.speed = random.randint(2, 5)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.reset()

    def reset(self):
        self.y = random.randint(-screen_height, -self.height - 20)
        self.speed = random.randint(2, 5)

obstacles = []
obstacle_gap = 150  # Decreased gap between obstacles
obstacle_widths = [random.randint(50, 100) for _ in range(5)]
total_obstacles_width = sum(obstacle_widths) + (len(obstacle_widths) - 1) * obstacle_gap
start_x = (screen_width - total_obstacles_width) // 2
for width in obstacle_widths:
    obstacles.append(Obstacle(start_x, width))
    start_x += width + obstacle_gap

# Car position and speed
car_x, car_y = (screen_width - car_width) // 2, screen_height - car_height - 20
car_speed = 5

# Function to handle game over screen and button clicks
def game_over_screen():
    retry_button = font.render("Retry", True, (255, 255, 255))
    retry_rect = retry_button.get_rect(center=(screen_width // 2, screen_height // 2))
    quit_button = font.render("Quit", True, (255, 255, 255))
    quit_rect = quit_button.get_rect(center=(screen_width // 2, screen_height // 2 + 50))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if retry_rect.collidepoint(mouse_pos):
                    # Reset game
                    global distance
                    distance = 0
                    global car_x, car_y
                    car_x, car_y = (screen_width - car_width) // 2, screen_height - car_height - 20
                    global obstacles
                    obstacles = []
                    obstacle_widths = [random.randint(50, 100) for _ in range(5)]
                    total_obstacles_width = sum(obstacle_widths) + (len(obstacle_widths) - 1) * obstacle_gap
                    start_x = (screen_width - total_obstacles_width) // 2
                    for width in obstacle_widths:
                        obstacles.append(Obstacle(start_x, width))
                        start_x += width + obstacle_gap
                    return
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(background_image, (0, 0))
        screen.blit(distance_text, distance_rect)
        screen.blit(retry_button, retry_rect)
        screen.blit(quit_button, quit_rect)
        pygame.display.flip()
        clock.tick(60)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < screen_width - car_width:
        car_x += car_speed

    # Update obstacles
    for obstacle in obstacles:
        obstacle.move()

    # Check for collision with obstacles
    for obstacle in obstacles:
        # Calculate bounding box for car
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        # Calculate bounding box for obstacle
        obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
        # Check for collision
        if car_rect.colliderect(obstacle_rect):
            print("Collision!")
            game_over_screen()  # Show game over screen and handle button clicks
            break  # Exit the collision loop if game is restarted

    # Update the distance traveled
    distance += car_speed / 60  # Assuming 60 frames per second
    distance_text = font.render(f"Distance: {int(distance)} km", True, (255, 255, 255))

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the car and obstacles
    screen.blit(car_image, (car_x, car_y))
    for obstacle in obstacles:
        obstacle.draw()

    # Draw the distance text
    screen.blit(distance_text, distance_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
