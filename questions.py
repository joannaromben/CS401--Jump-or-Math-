import pygame

import random
from answers import answer_options  

questions = {
    "5th": [
        ("What is 45 + 5?", 50),
        ("What is 15 + 10?", 25),
        ("What is 5 + 6?", 11),
        ("What is 45 + 5?", 50),
        ("What is 22 + 4?", 26),
        ("What is 20 + 20?", 40),
        ("What is 455 + 5?", 460),
        ("What is 3 + 4?", 7),
        ("What is 5 + 60?", 165),
        ("What is 45 + 50?", 95),
        ("What is 33 + 4?", 37),
        ("What is 6 + 6?", 12),
    ],
    "6th": [
        ("What is 12 - 4?", 8),
        ("What is 15 - 3?", 12),
        ("What is 45 - 5?", 40),
        ("What is 22 - 2?", 20),
        ("What is 6 - 3?", 3),
        ("What is 15 - 10?", 5),
        ("What is 21 - 11?", 10),
        ("What is 10 - 1?", 9),
        ("What is 100 - 95?", 5),
        ("What is 12 - 4?", 8),
        ("What is 9 - 1?", 8),
        ("What is 67 - 7?", 60),
    ],
    "7th": [
        ("What is 2 × 7?", 14),
        ("What is 1 × 9?", 9),
        ("What is 4 × 5?", 20),
        ("What is 12 × 2?", 24),
        ("What is 6 × 3?", 18),
        ("What is 3 × 3?", 9),
        ("What is 1 × 1?", 1),
        ("What is 10 × 10?", 100),
        ("What is 5 × 3?", 15),
        ("What is 3 × 4?", 12),
        ("What is 6 × 5?", 30),
        ("What is 2 × 4?", 8),
    ],
        "8th": [
        ("What is 2 × 7?", 14),
        ("What is 1 × 9?", 9),
        ("What is 4 × 5?", 20),
        ("What is 12 × 2?", 24),
        ("What is 6 × 3?", 18),
        ("What is 3 × 3?", 9),
        ("What is 1 × 1?", 1),
        ("What is 10 × 10?", 100),
        ("What is 5 × 3?", 15),
        ("What is 3 × 4?", 12),
        ("What is 6 × 5?", 30),
        ("What is 2 × 4?", 8),
    ]
}

def random_question(grade):
    if grade in questions:  
        random.shuffle(questions[grade]) 
        return questions[grade].pop()

def multiple_choice(correct_answer):
    return answer_options(correct_answer)
