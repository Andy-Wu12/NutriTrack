import string
import random


def generateRandStr(num_letters: int):
    return ''.join(random.choices(string.ascii_letters, k=num_letters))
