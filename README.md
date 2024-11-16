Rhythm Game - README
Overview
This is a rhythm-based game created using Pygame, where players are required to press specific keys corresponding to moving notes that appear on the screen. The objective is to hit the correct key at the right time to earn points. The game supports multiple players, allowing them to choose a character, set difficulty levels, and compete for the highest score. Players' performance is saved and ranked at the end of the game.

Features
Multiple Players: Up to a customizable number of players can join the game.
Character Selection: Players can choose from several character options, including a dog, cat, fox, etc.
Multiple Difficulty Levels: Easy, Medium, and Hard difficulty levels that affect the speed and challenge of the game.
Score Tracking: The score is based on how accurately the player presses keys in sync with moving notes.
CSV Export: At the end of the game, the scores are saved in CSV files based on the difficulty level.
Final Ranking: After all players have completed their game, a ranking based on scores is displayed.
Requirements
Python 3.x
Pygame library
You can install Pygame using the following command:

bash
Copier le code
pip install pygame
You will also need the following assets for the game to run correctly:

Background music (e.g., background_music.mp3)
Sound effects (e.g., note_a.wav, note_s.wav, miss_sound.wav)
Images for characters (e.g., dog.png, cat.png)
Background images (e.g., game_bg.png, new_bg.png)
Font for text rendering (e.g., press_start_2p.ttf)
Game Controls
Arrow Keys (A, S, D, F): Press the keys corresponding to the notes that fall on the screen.
Spacebar: Pause or unpause the game.
Enter Key: Confirm player information or difficulty level.
Setup Instructions
1. Install Pygame
Ensure you have Python 3.x installed. Then, install the Pygame library:

bash
Copier le code
pip install pygame
2. Place the Game Assets
Ensure that you have the required game assets in the same directory as the game file, including:

Character images (dog.png, cat.png, fox.png, etc.)
Background images (game_bg.png, new_bg.png)
Sound files (background_music.mp3, note_a.wav, etc.)
The custom font (press_start_2p.ttf)
3. Running the Game
Simply run the Python script using:

bash
Copier le code
python rhythm_game.py
Follow the on-screen instructions to start the game:

Enter the number of players.
Select difficulty (Easy, Medium, Hard).
Players enter their names and choose a character.
The game starts, and players press the appropriate keys in sync with the falling notes.
4. Ending the Game
At the end of the game, scores will be ranked, and the top players will be displayed in a final ranking screen.

Game Flow
Start Menu: Players will enter the number of participants and choose a difficulty level.
Character Selection: Each player will input their name and choose a character to play as.
Main Gameplay: The game will begin, with notes falling at increasing speeds based on the selected difficulty. Players must press the correct keys at the right time to score points.
Final Ranking: Once all players have finished, their scores will be sorted, and the final ranking is displayed.
CSV Saving: Scores for each difficulty level will be saved in separate CSV files (e.g., scores_easy.csv).
Saving and Loading Scores
At the end of each game session, the scores are saved in CSV files based on the difficulty level. These files include:

Player name
Score
Time spent
Character chosen



Link of the video:
[https://youtu.be/LXAFYKHYrkI?si=5zQOFPXOvRum525w](https://youtu.be/mHKfnTFwqgo?feature=shared)

![Capture d’écran 2024-11-16 001730](https://github.com/user-attachments/assets/7c6560d9-7d77-4627-af8e-63de4283b631)

![Capture d’écran 2024-11-16 001800](https://github.com/user-attachments/assets/28ddf023-07bd-4a95-b1c9-7c9855b43d94)


![Capture d’écran 2024-11-16 001816](https://github.com/user-attachments/assets/9fc14700-9b7b-4537-b1b2-760e606dc62a)





