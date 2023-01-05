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
    random_word = random.choice(words).upper()
    print(random_word)
    return random_word.upper()


get_random_words()
