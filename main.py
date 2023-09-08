import pygame
import sys
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random

# Data samples
data = []

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
SLOPE_HEIGHT = 100
SLOPE_WIDTH = 300
CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
SLOPE_ANGLE = 30
SLOPE_COLOR = (100, 100, 100)
CHARACTER_COLOR = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slope Climbing Game")

# Character attributes
character_x = WIDTH // 2 - CHARACTER_WIDTH // 2
character_y = HEIGHT - CHARACTER_HEIGHT - 3
character_speed = 5

runcount = 0


def ai(data, key):
    failornot = [item[0] for item in data]
    moves = [item[1] for item in data]
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(moves)
    X_train, X_test, y_train, y_test = train_test_split(
        X, failornot, test_size=0.2, random_state=42)
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy:", accuracy)
    new_moves = vectorizer.transform(key)
    predicted_move = clf.predict(new_moves)
    print("Predicted Move:", predicted_move[0])


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(data)
            running = False

    # Check for user input to move the character
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x += character_speed

    #left is 1, down is 2, up is 3, right is 4
    # in this case left 1 right is 2

    # make it completely random if theres no data yet
    if runcount == 0:
        random_press_combo = []
        for i in range(10):
            random_press_combo.append(random.randint(1, 2))

        for movement in random_press_combo:
            if movement == 1:
                character_x -= character_speed
            elif movement == 2:
                character_x += character_speed
    else:
        # create random movements and test if they'd work
        random_press_combo = []
        for i in range(10):
            random_press_combo.append(random.randint(1, 2))
        key = ''
        for i in random_press_combo:
            key += str(i) + ' '
        ai(data, key)  # Pass the data list and key to the ai function

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the slope
    pygame.draw.polygon(screen, SLOPE_COLOR, [
                        (0, HEIGHT), (SLOPE_WIDTH, HEIGHT), (0, HEIGHT - SLOPE_HEIGHT)])

    # Calculate the character's position on the slope
    if character_x <= SLOPE_WIDTH:
        slope_y = HEIGHT - SLOPE_HEIGHT
        character_y = slope_y + (character_x / SLOPE_WIDTH) * \
            SLOPE_HEIGHT * math.tan(math.radians(SLOPE_ANGLE)) - 3

    # Draw the character
    pygame.draw.rect(screen, CHARACTER_COLOR, (character_x,
                     character_y, CHARACTER_WIDTH, CHARACTER_HEIGHT))

    # Update the display
    pygame.display.update()

    pygame.time.delay(30)

    if 375 - character_x > 0:
        key = ''
        for i in random_press_combo:
            key += str(i) + ' '
        data.append((1, key))
    else:
        key = ''
        for i in random_press_combo:
            key += str(i) + ' '
        data.append((0, key))
    # Check if the character reaches the bottom
    if character_y <= 0:
        running = False
    runcount += 1

# Quit Pygame
pygame.quit()
sys.exit()
