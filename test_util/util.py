import string
import random


def generateRandStr(num_letters: int):
    return ''.join(random.choices(string.ascii_lowercase, k=num_letters))
