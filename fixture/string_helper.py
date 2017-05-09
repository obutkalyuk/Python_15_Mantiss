import re
import random
import string


def random_string(prefix, max_len):
    symbols = string.ascii_letters + string.digits  + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(max_len))])

def random_set(len):
    symbols = string.ascii_letters + string.digits
    return clear("".join([random.choice(symbols) for i in range(len)]))

def random_digits(max_len):
    symbols = string.digits
    return "".join([random.choice(symbols) for i in range(random.randrange(max_len))])

def clear(s):
    return re.sub("[() -]", "", s)