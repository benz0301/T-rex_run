# Pygame T-Rex run game

A classic T-Rex Runner game made by using the pygame library

## Table of contents
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Features](#features)
- [Main Menu](#main-menu)
- [Options Menu](#options-menu)
- [Dependencies](#dependencies)
- [License](#license)

## Installation

1. **Prerequisites**: Make sure Python and Pygame are installed on your system.

   Install Pygame:
   ```bash
   pip install pygame
    ```
    
2. **Clone the repository**: Clone the repository to your local machine using the following command:
    ```bash 
   git clone https://github.com/yourusername/t-rex-runner-game.git
    cd t-rex-runner-game
    ```

3. **Download the Assets:** Make sure you have the required images and sound inside it ,the strucutre should look like this:

    ```bash 
    Assets/
    ├── Audio/
    │   ├── jump.mp3
    │   └── death.mp3
    ├── Bird/
    │   ├── Bird1.png
    │   └── Bird2.png
    ├── Cactus/
    │   ├── SmallCactus1.png
    │   ├── SmallCactus2.png
    │   ├── SmallCactus3.png
    │   ├── LargeCactus1.png
    │   ├── LargeCactus2.png
    │   └── LargeCactus3.png
    ├── Dino/
    │   ├── DinoRun1.png
    │   ├── DinoRun2.png
    │   ├── DinoJump.png
    │   └── DinoDuck1.png
    ├── other/
    │   ├── Cloud.png
    │   └── Track.png
    ```

4. **Run the Game:**
    ```bash
    python game.py
    ```

## How to Play

- **Start the Game:** Press the `Spacebar` on the main menu to start the game.
- **Controls:**
  - Press the `Up Arrow` to jump.
  - Press the `Down Arrow` to duck.
- **Score Points:** The player's score increases as they avoid obstacles. Every 100 points, the game speeds up.
- **Avoid Obstacles:** Jump or duck to avoid cacti and birds. Colliding with an obstacle ends the game.
- **Toggle Sound:** Go to the options menu from the main menu and toggle sound on or off.

## Features

- **Character Control:** The player can run, jump, and duck to avoid obstacles.
- **Obstacles:** The game has various obstacles like small cacti, large cacti, and flying birds.
- **Clouds & Background:** Dynamic background and moving clouds.
- **Sound Effects:** The game features sound effects for jumping and collision.
- **Score System:** Tracks and displays the player's score during the game.
- **Pause & Resume Sounds:** Toggle sound effects on or off through the options menu.
- **Custom Player Name:** Allows the player to input their name before starting the game.
- **Game Menu:** Start, restart, or quit the game through the main menu. Access game options like sound muting and player name changes.

## Main Menu

- **Start:** Press the `Spacebar` to start or restart the game.
- **Options:** Click the `Options` button to change the player name and mute/unmute game sounds.
- **Quit:** Press the `Quit` button to exit the game.

## Options Menu

- **Player Name:** Enter your player name in the input box.
- **Mute/Unmute:** Toggle sound effects.
- **Return to Menu:** Click the `Return` button to go back to the main menu after changing the settings.

## Dependencies

- **Python 3.6+**
- **Pygame 2.0+**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


