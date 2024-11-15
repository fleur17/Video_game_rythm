import pygame
import random
import time
import sys
import csv

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NOTE_SIZE = 50
TARGET_HEIGHT = 500  # The y-coordinate where the player needs to press keys
GAME_DURATION = 30  # Game duration in seconds
DIFFICULTY_LEVELS = {"Easy": 3, "Medium": 5, "Hard": 8}
paused=False
# Load the custom video game font
game_font = pygame.font.Font("press_start_2p.ttf", 20)  # Adjust font size as needed


# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

# Font setup
font = pygame.font.Font("press_start_2p.ttf", 20)
note_font = pygame.font.SysFont("Arial", 24)  # Smaller font for note letters

# Load background images
background_image = pygame.image.load("game_bg.png")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

menu_background = pygame.image.load("new_bg.png")
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))



# Particle system setup
particles = []


# Load sounds
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1, 0.0)  # Loop music indefinitely

# Individual sounds for each key
key_sounds = {
    'a': pygame.mixer.Sound("note_a.wav"),
    's': pygame.mixer.Sound("note_s.wav"),
    'd': pygame.mixer.Sound("note_d.wav"),
    'f': pygame.mixer.Sound("note_f.wav")
}

miss_sound = pygame.mixer.Sound("miss_sound.wav")

# Variables for player info and scores
players = []
scores = []
difficulty = None  # Initially, no difficulty level selected
note_speed = None  # No speed set initially

# Character images
character_images = {
    "Chien": pygame.image.load("dog.png"),
    "Chat": pygame.image.load("cat.png"),
    "Mickey": pygame.image.load("mickey.png"),
    "Goku": pygame.image.load("goku.png"),
    "fox": pygame.image.load("fox.png")  # Add Bird character
}

# Notes setup with a musical sequence
note_sequence = ['a', 'd', 's', 'f', 'a', 's', 'd', 'f']  # Default sequence, but will be randomized for each player
notes = []

# Function to create a note based on random selection
def create_note():
    key = random.choice(['a', 's', 'd', 'f'])  # Randomly select key
    x_pos = random.choice([200, 400, 600])  # Random x-position for the notes
    note = {
        'x': x_pos,
        'y': 0,
        'key': key
    }
    notes.append(note)

# Function to save scores to CSV
import csv

# Assuming GAME_DURATION is a constant representing the game duration for the player
GAME_DURATION = 60  # Example game duration (in seconds)



# Function to save scores to CSV according to the difficulty level
def save_scores_to_csv(difficulty):
    try:
        # Make sure difficulty is in the right format (easy, medium, hard)
        difficulty = difficulty.lower()

        # Choose the appropriate filename based on difficulty level
        filename = f"scores_{difficulty}.csv"  # Example: scores_easy.csv, scores_medium.csv, scores_hard.csv
        
        # Open the CSV file in append mode
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # If the file is empty, write headers
            if file.tell() == 0:
                writer.writerow(["Player Name", "Score", "Time", "Character"])
            
            # Write the player data to the CSV file
            for player_name, score, character in scores:
                writer.writerow([player_name, score, GAME_DURATION, character])
        
        print(f"Scores saved successfully to {filename}!")
    
    except PermissionError:
        print("Permission denied. Make sure the file is not open in another program and you have write permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
save_scores_to_csv("easy")   # To save scores for easy difficulty level
save_scores_to_csv("medium") # To save scores for medium difficulty level
save_scores_to_csv("hard")   # To save scores for hard difficulty level

# Function to display the start menu
def start_menu():
    print("Starting game...")
    global players, difficulty, note_speed
    input_active = True
    player_count = ""
    
    # Create button instances
    easy_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 40, "Easy", WHITE, GREEN, font, BLACK)
    medium_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 40, "Medium", WHITE, BLUE, font, BLACK)
    hard_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 40, "Hard", WHITE, RED, font, BLACK)
    
    while input_active:
        screen.blit(menu_background, (0, 0))  # Use menu background
        
        # Display title for player count entry
        title = font.render("Enter Number of Players:", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        # Show player count input
        player_text = font.render(player_count, True, WHITE)
        screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, HEIGHT // 2))
        
        # Display buttons (they change color when hovered)
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)
        
        pygame.display.flip()
        
        # Event handling for player count and difficulty selection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_count.isdigit() and int(player_count) > 0 and difficulty:
                    # Proceed only if a player count and difficulty are set
                    input_active = False
                    players = ["" for _ in range(int(player_count))]
                elif event.key == pygame.K_BACKSPACE:
                    player_count = player_count[:-1]
                elif event.unicode.isnumeric():
                    player_count += event.unicode
                elif event.unicode == 'e':  # Key for Easy
                    difficulty = "Easy"
                    note_speed = DIFFICULTY_LEVELS[difficulty] * 0.3  # Slow down speed for easier gameplay
                elif event.unicode == 'm':  # Key for Medium
                    difficulty = "Medium"
                    note_speed = DIFFICULTY_LEVELS[difficulty] * 0.5
                elif event.unicode == 'h':  # Key for Hard
                    difficulty = "Hard"
                    note_speed = DIFFICULTY_LEVELS[difficulty] * 0.7  # Slower but challenging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.is_hovered():
                    difficulty = "Easy"
                    note_speed = DIFFICULTY_LEVELS[difficulty] * 0.3
                elif medium_button.is_hovered():
                    difficulty = "Medium"
                    note_speed = DIFFICULTY_LEVELS[difficulty] * 0.5
                elif hard_button.is_hovered():
                    difficulty = "Hard"
                    note_speed = DIFFICULTY_LEVELS[difficulty] * 0.7


# Function to let each player enter their name and choose character
def enter_player_names():
    global players
    for i in range(len(players)):
        name = ""
        character = None
        input_active = True
        
        while input_active:
            screen.fill(BLACK)
            prompt = font.render(f"Player {i+1}, enter your name:", True, WHITE)
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 4))
            
            name_text = font.render(name, True, GREEN)
            screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 3))
            
            y_offset = HEIGHT // 2
            for idx, (char_name, img) in enumerate(character_images.items()):
                scaled_img = pygame.transform.scale(img, (80, 80))
                x_position = WIDTH // 4 + idx * 150
                img_rect = pygame.Rect(x_position - 10, y_offset - 10, 100, 100)
                
                # Draw selection rectangle around chosen character
                if char_name == character:
                    pygame.draw.rect(screen, BLUE, img_rect, 3)
                    
                screen.blit(scaled_img, (x_position, y_offset))
                char_text = font.render(char_name, True, WHITE)
                screen.blit(char_text, (x_position, y_offset + 90))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name and character:
                        players[i] = (name, character)
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for idx, (char_name, img) in enumerate(character_images.items()):
                        img_rect = pygame.Rect(WIDTH // 4 + idx * 150 - 10, y_offset - 10, 100, 100)
                        if img_rect.collidepoint(mouse_pos):
                            character = char_name

# Function to display a waiting screen before starting each player's game
def waiting_screen(player_name):
    print(f"Waiting for {player_name} to start the game...")
    screen.fill(BLACK)
    waiting_message = font.render(f"{player_name}, get ready!", True, WHITE)
    screen.blit(waiting_message, (WIDTH // 2 - waiting_message.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)







# Function to run the main game
def main_game(player_name, character):
    
    print(f"Starting game for {player_name} with {character}...")
    score = 0
    missed = 0
    running = True
    clock = pygame.time.Clock()
    last_note_time = time.time()
    start_time = time.time()

    global paused  # Make sure the global paused variable is used

    while running:
        if paused:
            # If the game is paused, show the black screen with a message
            screen.fill(BLACK)  # Fill the screen with black
            pause_text = font.render("Game Paused. Press Space to Resume", True, WHITE)
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()

            # Wait here until the player presses space to resume
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:  # Press space to resume
                            paused = False
                time.sleep(0.1)  # Small delay to prevent the game from freezing

            continue  # Once paused is False, continue the normal game loop
        
        
        # Normal game logic happens here when not paused
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Draw horizontal line where notes need to be pressed
        pygame.draw.line(screen, GREEN, (0, TARGET_HEIGHT), (WIDTH, TARGET_HEIGHT), 2)

        if time.time() - start_time >= GAME_DURATION:
            running = False
            scores.append((player_name, score, character))  # Append player score
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Toggle pause with SPACEBAR
                    paused = not paused

            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key in key_sounds:
                    for note in notes:
                        timing_diff = abs(note['y'] - TARGET_HEIGHT)
                        if note['key'] == key and timing_diff <= NOTE_SIZE // 2:
                            if timing_diff <= 5:
                                score += 3  # Higher score for perfect timing
                                feedback = "Perfect!"
                            elif timing_diff <= 15:
                                score += 2  # Medium score for good timing
                                feedback = "Good!"
                            else:
                                score += 1  # Lowest score for acceptable timing
                                feedback = "Okay!"
                
                            key_sounds[key].play()
                            notes.remove(note)
                            break
                    else:
                        missed += 1
                        miss_sound.play()
                        feedback = "Miss!"


        # Generate notes according to pattern
        if time.time() - last_note_time >= 1.0 / note_speed:
            create_note()
            last_note_time = time.time()

        # Draw notes
        for note in notes:
            pygame.draw.rect(screen, WHITE, pygame.Rect(note['x'], note['y'], NOTE_SIZE, NOTE_SIZE))
            note_text = note_font.render(note['key'], True, BLACK)
            screen.blit(note_text, (note['x'] + NOTE_SIZE // 4, note['y'] + NOTE_SIZE // 4))

        # Move notes down
        for note in notes:
            note['y'] += note_speed

        # Check for missed notes
        for note in notes:
            if note['y'] > HEIGHT:
                notes.remove(note)
                missed += 1  # Increment missed count only when a note passes
                miss_sound.play()

        # Display the score with a rectangle around it
        score_text = font.render(f"Score: {score}", True, BLUE)
        score_rect = score_text.get_rect(topleft=(10, 10))  # Get the dimensions of the text
        padding = 10  # Padding around the text
        pygame.draw.rect(screen, BLACK, (score_rect.x - padding, score_rect.y - padding, score_rect.width + 2 * padding, score_rect.height + 2 * padding))
        pygame.draw.rect(screen, BLUE, (score_rect.x - padding, score_rect.y - padding, score_rect.width + 2 * padding, score_rect.height + 2 * padding), 2)  # Border
        screen.blit(score_text, (10, 10))

        # Display missed count
        missed_text = font.render(f"Missed: {missed}", True, RED)
        screen.blit(missed_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)





# Function to display final ranking
def display_final_ranking():

    print("Displaying final ranking...")
    # Sort players based on their scores
    ranked_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    screen.fill(BLACK)
    title = font.render("Final Rankings", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    y_offset = HEIGHT // 3
    for idx, (player_name, score, character) in enumerate(ranked_scores):
        rank_text = font.render(f"{idx + 1}. {player_name} - Score: {score}", True, WHITE)
        screen.blit(rank_text, (WIDTH // 2 - rank_text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    time.sleep(5)  # Show rankings for 5 seconds

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.text_color = text_color

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        # Change color if hovered
        color = self.hover_color if self.is_hovered() else self.color
        
        # Draw button rectangle
        pygame.draw.rect(screen, color, self.rect)
        
        # Render and draw the text centered inside the button
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

# Function to run the game
def run_game():
    start_menu()
    enter_player_names()
    for player_name, character in players:
        waiting_screen(player_name)
        main_game(player_name, character)
    
    for difficulty in DIFFICULTY_LEVELS:
        save_scores_to_csv(difficulty)  # Save all players' scores to CSV for each difficulty level

    # Show final ranking after the game finishes
    display_final_ranking()  # Display the ranking after all players finish


# Function to let each player enter their name and choose character
def enter_player_names():
    for i in range(len(players)):
        name = ""
        character = None
        input_active = True
        
        while input_active:
            screen.blit(menu_background, (0, 0))  # Use menu background for character selection
            
            prompt = font.render(f"Player {i+1}, enter your name:", True, WHITE)
            screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 4))
            
            name_text = font.render(name, True,WHITE)
            screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 3))
            
            y_offset = HEIGHT // 2
            for idx, (char_name, img) in enumerate(character_images.items()):
                scaled_img = pygame.transform.scale(img, (80, 80))
                x_position = WIDTH // 4 + idx * 150
                img_rect = pygame.Rect(x_position - 10, y_offset - 10, 100, 100)
                
                # Draw selection rectangle around chosen character
                if char_name == character:
                    pygame.draw.rect(screen, BLUE, img_rect, 3)
                    
                screen.blit(scaled_img, (x_position, y_offset))
                char_text = font.render(char_name, True, WHITE)
                screen.blit(char_text, (x_position, y_offset + 90))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name and character:
                        players[i] = (name, character)
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for idx, (char_name, img) in enumerate(character_images.items()):
                        img_rect = pygame.Rect(WIDTH // 4 + idx * 150 - 10, y_offset - 10, 100, 100)
                        if img_rect.collidepoint(mouse_pos):
                            character = char_name


# Function to display final ranking with background
def display_final_ranking():
    # Sort players based on their scores
    ranked_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    screen.blit(menu_background, (0, 0))  # Use menu background for the ranking screen
    title = font.render("Final Rankings", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    y_offset = HEIGHT // 3
    for idx, (player_name, score, character) in enumerate(ranked_scores):
        rank_text = font.render(f"{idx + 1}. {player_name} - Score: {score}", True, GREEN)
        screen.blit(rank_text, (WIDTH // 2 - rank_text.get_width() // 2, y_offset))
        y_offset += 40

    pygame.display.flip()
    time.sleep(5)  # Show rankings for 5 seconds






def load_leaderboard():
    leaderboard = []
    try:
        with open('scores_easy.csv', mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                player_name, score, game_time, character = row
                leaderboard.append((player_name, int(score), int(game_time), character))
    except FileNotFoundError:
        print("No leaderboard data found. Play a game to generate scores.")
    except Exception as e:
        print(f"Error reading leaderboard: {e}")
    
    # Sort by score in descending order
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    return leaderboard







def display_leaderboard():
    leaderboard = load_leaderboard()
    
    screen.blit(menu_background, (0, 0))  # Use the menu background for leaderboard
    title = game_font.render("Leaderboard", True, WHITE)  # Use custom font
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 6))
    

    
    if not leaderboard:
        no_data_text = game_font.render("No data available.", True, WHITE)  # White text for no data
        screen.blit(no_data_text, (WIDTH // 2 - no_data_text.get_width() // 2, HEIGHT // 2))
    else:
        y_offset = HEIGHT // 4
        for idx, (player_name, score, game_time, character) in enumerate(leaderboard[:10]):  # Top 10 scores
            rank_text = game_font.render(
                f"{idx + 1}. {player_name} - {score} pts - {character}", True, WHITE
            )
            screen.blit(rank_text, (WIDTH // 2 - rank_text.get_width() // 2, y_offset))
            y_offset += 40

    pygame.display.flip()
    time.sleep(5)  # Display for 5 seconds


if __name__ == "__main__":
    
    display_leaderboard()  # Show leaderboard before starting the game
    run_game()
    display_leaderboard()  # Show leaderboard after the game ends


import matplotlib.pyplot as plt
import numpy as np

# Sample player data (replace with actual player data from the game)
players = ['fleur', 'mickey', 'ryu', 'rayan', 'oriane']
scores = [120, 150, 90, 200, 180]

# Plotting the scores distribution
plt.figure(figsize=(10, 6))
plt.bar(players, scores, color='skyblue')
plt.xlabel('Players')
plt.ylabel('Scores')
plt.title('Score Distribution of Players')
plt.show()

# Sample data for difficulty levels and corresponding scores (replace with actual data)
difficulty_levels = ['Easy', 'Medium', 'Hard', 'Medium', 'Easy']
scores = [120, 150, 90, 200, 180]

# Mapping difficulty levels to numeric values for plotting
difficulty_map = {'Easy': 1, 'Medium': 2, 'Hard': 3}
difficulty_numeric = [difficulty_map[d] for d in difficulty_levels]

# Plotting the difficulty vs score scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(difficulty_numeric, scores, color='orange')
plt.xticks([1, 2, 3], ['Easy', 'Medium', 'Hard'])
plt.xlabel('Difficulty Level')
plt.ylabel('Scores')
plt.title('Difficulty Level vs Player Score')
plt.show()


# Sample leaderboard data over time (replace with actual game data)
time_intervals = [1, 2, 3, 4, 5]  # Time progression (e.g., rounds of the game)
leaderboard_scores = {
    'fleur': [120, 150, 180, 200, 220],
    'oriane': [100, 120, 140, 160, 180],
    'oce': [90, 100, 110, 130, 150]
}

# Plotting the leaderboard progression
plt.figure(figsize=(10, 6))

for player, scores in leaderboard_scores.items():
    plt.plot(time_intervals, scores, label=player)

plt.xlabel('Time (Rounds)')
plt.ylabel('Scores')
plt.title('Leaderboard Progression Over Time')
plt.legend()
plt.show()
