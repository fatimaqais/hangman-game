import random
import os

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hangman_game')

score = SHEET.worksheet('userscores')
points = 0


words = ['happy', 'excited', 'lucky', 'swimming', 'jump', 'running',
         'climbing', 'movie', 'music', 'dancing', 'apple', 'banana', 'oranges',
         'mango', 'pineapple', 'guava', 'lemon', 'watermelon', 'strawberry',
         'building', 'mountain', 'river', 'trees', 'tiger', 'lion', 'elephant',
         'awkward', 'python', 'umbrella', 'juice', 'camera', 'glasses',
         'notebook', 'laptop', 'toothbrush', 'magazine', 'headphone', 'boat'
         'calculator', 'balloon', 'battery', 'tissue', 'computer', 'scissors']


def get_random_words():
    """
    Picks a random word from the words list.
    Displays it to user in uppercase letters.
    """
    random_word = random.choice(words)
    return random_word.upper()


def clear_terminal():
    """
    Code found on stack overflow
    Clears the terminal if it gets too crowded
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def username_validator():
    """
    Checks the user entered a valid username.
    Checks if the username is 3-10 characters long.
    Only accepts letters ad dispays error message if requirements don't match
    """
    global username
    username = ''
    while True:
        username = input("Please enter a username to play:\n")
        if username.isalpha() and len(username) >= 3 and len(username) <= 10:
            print(f"Hello {username}! Let's start the game\n")
            break
        else:
            print("Username need to be letters and between 3-10 characters")

    play_hangman()
    return username


def start_game():
    """
    Gets a username from the player to start game.
    Validates the username to be letters only.
    Tells the rules of the game to the user.
    """
    print("Please select an option: 1, 2 or 3\n")
    print("1.Start Game\n2.Rules \n3.Highscores \n")
    option = input("Enter a number:\n")
    print("\n")
    if option == '1':
        print("Starting game...")
        username_validator()
    elif option == '2':
        print("1. You will be given a random word to guess.")
        print("The blank lines '_' show how many letters are missing.\n")
        print("2. You can either guess a letter or the full word.\n")
        print("3. You have 6 lives to guess the word.")
        print("Every wrong guess deducts a life\n")
        print("4. Each word you guess correctly scores you 10 points\n")
        end_game()
    elif option == '3':
        leader_board()
        end_game()
    else:
        print("Please enter a valid number \n")
        start_game()


def play_hangman():
    """
    Once the game has started, displays the words for user.
    Let's the user play until lives are finished.
    Checks users guesses and adds it to a list of words or letters.
    """
    random_word = get_random_words()
    full_word = random_word
    lives = 6
    player_won = False
    game_over = False
    correct_guess = []
    incorrect_guess = []
    global points

    while not game_over and lives > 0:
        word = ''
        for letter in full_word:
            if letter in correct_guess:
                word += letter
            else:
                word += "_"

        print("The word is: ", word, "\n")
        print(f"Lives Left: {lives}")
        print("Incorrect guesses: ", incorrect_guess, "\n")

        if "_" not in word:
            game_over = True
            player_won = True
            break

        print("...............................\n")
        guess = input("Guess a letter or word:\n").upper()

        if guess.isalpha() and len(guess) == 1:
            if guess in correct_guess or guess in incorrect_guess:
                print("You already guessed that letter")
            elif guess not in full_word:
                print(guess, "is not in the word")
                incorrect_guess.append(guess)
                lives -= 1
                print(display_hangman(lives))
            else:
                print("Great! you made a correct guess\n")
                correct_guess.append(guess)
        elif guess.isalpha() and len(guess) == len(full_word):
            if guess == full_word:
                print("Congartulations, You guessed the correct word!")
                correct_guess.append(guess)
                game_over = True
                player_won = True
            elif guess in incorrect_guess:
                print("You already guessed this word")
            else:
                print("Incorrect guess")
                incorrect_guess.append(guess)
                lives -= 1
                print(display_hangman(lives))
        else:
            print("Please make a valid guess")

    if player_won:
        print("You won!\n")
        points += 10
        print(f"Total score: {points}")
        keep_playing = input("Would you like to keep playing? Y/N:\n").upper()
        while keep_playing == "Y":
            clear_terminal()
            random_word = get_random_words()
            play_hangman()
            break
        if keep_playing == "N":
            print("Thank you for playing!\n")
            update_leaderboard()
            leader_board()
    else:
        print("Sorry, you lost! The correct word was: " + full_word, '\n')
        print(f"Total score: {points}\n")
        leader_board()


def update_leaderboard():
    """
    Updates the score sheet with username and their total score
    """
    update = [username, points]
    score.insert_row(update, 2)


def leader_board():
    """
    Display the user scores
    """
    score.sort((2, 'des'))
    data = score.get('A1:B6')
    print(*data, sep="\n")
    print("\n")


def end_game():
    """
    Gives the user option to start game or quit.
    """
    while True:
        continue_game = input("Would you like to start game? Y/N:\n").upper()
        try:
            if continue_game == "Y":
                print("Starting game... \n")
                username_validator()
                break
            elif continue_game == "N":
                print("Thankyou for playing! Hope to see you again\n")
                break
            else:
                raise ValueError
        except ValueError:
            print("Invalid entry. Please try again!\n")


def display_hangman(lives):
    """
    This is an image of how many lives the user has left
    before the game is over.
    This code was taken from "https://www.youtube.com/watch?v=m4nEnsavl6w".
    """
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     /
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |
                   |
                   |
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |
                   |
                   |
                   |
                   -
                """
    ]
    return stages[lives]


def main():
    """
    Calls the function to start the game
    """
    start_game()


print("Welcome to a game of hangman! \n")
main()
