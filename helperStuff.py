#helper functions for ctf challenge program

import random
import string
from constants import *

def randomString(size):
    random.seed()
    msg = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

    return bytes(msg, "ascii")

#exception to call when time limit has passed
class TimeExpired(Exception): pass

#key for easy crypto algo
def randomKey(min_val = MIN_KEY, max_val = MAX_KEY):
    random.seed()
    return random.randint(min_val, max_val)

