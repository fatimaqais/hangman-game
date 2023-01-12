# Hangman Game - Portfolio Project 3
This hamngman game is a python terminal game, which runs in the mock terminal on Heroku.

Users can start the game after they have entered their username for the game. Users are given an option to start the game, view rules and see the leaderboard. Once the game has started the user is presented with blank lines to show the missing letters. The number of blank lines shows how many letters need to be guessed by user. The user has 6 lives to guess the word. For every wrong word or letter guessed, the player loses 1 life. The incorrect guesses are displayed to the user so they can keep track of what they have already guessed.

If the user guesses a word correctly, they gain 10 points. They can continue to keep guessing to be placed in the top 5 players in the leaderboard. The more word they guess without losing, the higher their points will be. Once the player runs out of life and fails to guess the word, the game ends and the player has to start a new game. Once the game has ended, the leaderboard is shown to the user to check if they've made it in the top 5.

The live link to the site: [Live Link to the site]()

![Mockup screenshot]()

![Flowchart]()

## __Technologies Used__

### Languages Used
- [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) was the only language used to create the program.

### Frameworks, Libraries and Programs Used
- [random](https://docs.python.org/3/library/random.html) was used to generate a random word from the list of words.
- [gspread](https://docs.gspread.org/en/v5.7.0/) was used to store the players name and points. It is used to display the top 5 highscore in the leaderboard.
- [Smartdraw](https://www.smartdraw.com/flowchart/flowchart-maker.htm) was used to create the flowchart.
- [Git](https://git-scm.com/) was used for version control.
- [Github](https://github.com/) was used to save and store the project's code.

