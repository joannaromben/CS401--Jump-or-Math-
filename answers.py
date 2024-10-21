import pygame 
import random

import random

def answer_options(correct_answer):
    options = [correct_answer]
    
    while len(options) < 4:
        wrong_answer = correct_answer + random.randint(0, 105)
        if wrong_answer not in options and wrong_answer >= 0:
            options.append(wrong_answer)

    random.shuffle(options) 
    return options
