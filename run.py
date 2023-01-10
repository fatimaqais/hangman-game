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


def leader_board():
    """
    Display the user scores
    """
    score = SHEET.worksheet('userscores')

    data = score.get_all_values()

    print(data)


words = ['sad', 'happy', 'excited', 'lucky', 'swimming', 'jump', 'running',
         'climbing', 'movie', 'music', 'dancing', 'apple', 'banana', 'oranges',
         'mango', 'pineapple', 'guava', 'lemon', 'watermelon', 'strawberry',
         'building', 'mountain', 'river', 'trees', 'tiger', 'lion', 'elephant']


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
    while True:
        username = input("Please enter a username to play: ")
        if username.isalpha() and len(username) >= 3 and len(username) <= 10:
            print(f"Hello {username}! Let's start the game\n")
            break
        else:
            print("Username need to be letters and between 3-10 characters")

    random_word = get_random_words()
    play_hangman(random_word)


def start_game():
    """
    Gets a username from the player to start game.
    Validates the username to be letters only.
    Tells the rules of the game to the user.
    """
    print("Welcome to a game of hangman! \n")
    print("Please select an option: 1, 2 or 3\n")
    print("1.Start Game\n2.Rules \n3.Highscores \n")
    option = int(input("Enter a number: "))
    print("\n")
    if option == 1:
        username_validator()
    elif option == 2:
        print("1. You will be given a random word to guess.")
        print("The blank lines '_' show how many letters are missing")
        print("2. You have 6 lives to guess the word.")
        print("Every wrong guess deducts a life\n")
        print("3. Each word you guess correctly scores you 10 points\n")
        end_game()
    elif option == 3:
        leader_board()
        end_game()
    else:
        print("Please enter a valid number")
        start_game()


def play_hangman(random_word):
    """
    Once the game has started, displays the words for user.
    Let's the user play until lives are finished.
    Checks users guesses and adds it to a list of words or letters.
    """
    full_word = random_word
    # for debugging
    print(full_word)
    lives = 6
    player_won = False
    game_over = False
    correct_guess = []
    incorrect_guess = []

    while not game_over and lives > 0:
        word = ''
        for letter in full_word:
            if letter in correct_guess:
                word += letter
            else:
                word += "_"
        print(word)

        if "_" not in word:
            game_over = True
            player_won = True
            break

        guess = input("Guess a letter or word: ").upper()

        if guess.isalpha() and len(guess) == 1:
            if guess in correct_guess or guess in incorrect_guess:
                print("You already guessed that letter")
            elif guess not in full_word:
                print(guess, "is not in the word")
                incorrect_guess.append(guess)
                lives -= 1
            else:
                print("Great! you made a correct guess")
                correct_guess.append(guess)
        elif guess.isalpha() and len(guess) == len(full_word):
            if guess in incorrect_guess:
                print("You already guessed this word")
                lives -= 1
            else:
                print("Congartulations, You guessed the correct word!")
                correct_guess.append(guess)
                game_over = True
                player_won = True
        else:
            print("Please make a valid guess")

        print(display_hangman(lives))
        print("Incorrect guesses: ", incorrect_guess)

    if player_won:
        print("You won! Thank you for playing \n")
        keep_playing = input("Would you like to keep playing? Y/N: ").upper()
        while keep_playing == "Y":
            clear_terminal()
            random_word = get_random_words()
            play_hangman(random_word)
            break
    else:
        print("Sorry, you lost! The correct word was: " + full_word)


def end_game():
    """
    Gisves the user option to start game or quit.
    """
    if input("Would you like to start game? Y/N:").upper() == "Y":
        print("Starting game... \n")
        username_validator()
    else:
        print("Thankyou for playing")


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


main()
