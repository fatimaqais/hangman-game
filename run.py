import random

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


def start_game():
    """
    Gets a username from the player to start game.
    Validates the username to be letters only.
    Tells the rules of the game to the user.
    """

    while True:
        username = input("Please enter a username to play: ")
        if username.isalpha() and len(username) >= 3 and len(username) <= 10:
            break
        else:
            print("Username need to be letters and between 3-10 characters\n")

    print(f"Hello {username}! Let's start the game\n")


def play_hangman(random_word):
    """
    Once the game has started, displays the words for user.
    Let's the user play until lives are finished.
    Checks users guesses and adds it to a list of words or letters.
    """
    full_word = random_word
    lives = 6
    player_won = False
    game_over = False
    correct_guess = []
    incorrect_guess = []

    while not game_over:
        word = ''
        for letter in full_word:
            if letter in correct_guess:
                word += letter
            else:
                word += "_"

        print(word)

        if "_" not in word:
            player_won = True
            game_over = True
        break


def main():
    """
    Calls all the functions
    """
    random_word = get_random_words()
    start_game()
    play_hangman(random_word)


main()
