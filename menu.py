import pygame

pygame.init()

def display_menu():

grade_option = ["5th", "6th", "7th", "8th"]
gender_option = ["girl", "boy"]

grade_selected = grade_option[0]
gender_selected = gender_option[0]
dropdown_open = False
selected_index = 0

while True:

screen.fill(BLACK)

game_title = font.render("Jump or Math!", True, WHITE)
title_rect = game_title.get_rect(center=(WIDTH // 4, HEIGHT // 2 - 50))
screen.blit(game_title, title_rect)

grade_option = small_font.render(f"What grade are you in? {selected_grade}", True, WHITE)
grade_rect = grade_text.get_rect(center=(WIDTH // 4, HEIGHT // 2 - 30))
screen.blit(grade_option, grade_rect)

gender_text = small_font.render(f"Please select your gender {selected_gender}", True, WHITE)
gender_rect = gender_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
screen.blit(gender_text, gender_rect)

if dropdown_option:
for i, grade in enumerate(grade_option):
option_drop = small_font.render(grade, True, WHITE)
option_rect = option_text.get_rect(center=(WIDTH // 4, HEIGHT // 2 + (i * 30)))
screen.blit(option_text, option_rect)