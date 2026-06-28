import random


def generate_otp(length=6):

    code = ""

    for _ in range(length):
        code += str(random.randint(0, 9))

    return code