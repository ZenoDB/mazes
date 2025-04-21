from mazeGenerator import Maze
import button
import pygame
import random
import time

pygame.init()
pygame.font.init()

gen_animated = False
solve_animated = False

num_cells = 50
num_cells_display = str(num_cells)

maze = Maze(num_cells, [], True)

title_img = pygame.image.load("images/title.png").convert_alpha()
on_button_img = pygame.image.load("images/on-button.png").convert_alpha()
off_button_img = pygame.image.load("images/off-button.png").convert_alpha()
gen_button_img = pygame.image.load("images/generate-button.png").convert_alpha()
solve_button_img = pygame.image.load("images/solve-button.png").convert_alpha()
unselected_text_box_img = pygame.image.load("images/text-box-unselected.png").convert_alpha()
selected_text_box_img = pygame.image.load("images/text-box-selected.png").convert_alpha()
save_button_img = pygame.image.load("images/save-image.png").convert_alpha()

generate_button = button.Button(915, 400, gen_button_img)
solve_button = button.Button(1150, 400, solve_button_img)
gen_ani_switch = button.Switch(915, 600, on_button_img, off_button_img, gen_animated)
solve_ani_switch = button.Switch(1150, 600, on_button_img, off_button_img, solve_animated)
text_box = button.TextInput(915, 200, unselected_text_box_img, selected_text_box_img)
save_button = button.Button(915, 750, save_button_img)

menu_components = [title_img, generate_button, solve_button, gen_ani_switch, solve_ani_switch, text_box, save_button]

maze.__init__(num_cells, menu_components, True)

screen = maze.screen

saved_area = pygame.Rect(0, 0, 900, 900)
saved_surface = screen.subsurface(saved_area)

DISPLAY_WIDTH = maze.DISPLAY_WIDTH
DISPLAY_HEIGHT = maze.DISPLAY_HEIGHT
DISPLAY_COLOUR = maze.DISPLAY_COLOUR
WALL_COLOUR = maze.WALL_COLOUR

rect_x = maze.rect_x
maze.rect_y = 0
cell_width = maze.cell_width
cell_height = maze.cell_height

screen.fill(DISPLAY_COLOUR)

maze.drawMenu()

player_x = 0.5 * cell_width - 5
player_y = 0.5 * cell_height - 5

pygame.display.update()

running = True

clock = pygame.time.Clock()

new_maze = False

font = pygame.font.SysFont("Arial.ttf", size=75)

while running:

    #pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(player_x, player_y, 10, 10))

    if generate_button.checkPressed() and num_cells > 0:
        if num_cells != maze.width:
            maze.__init__(num_cells, menu_components, True)
        new_maze = True
        maze.reset()
        maze.displayNumCells(num_cells_display, font)
        maze.drawGrid()
        maze.recursiveBacktracking((1, 1), gen_animated)
        if not gen_animated:
            maze.drawMaze()


    if solve_button.checkPressed() and new_maze:
        new_maze = False
        if not solve_animated:
            start_time = time.perf_counter()
            maze.deadEndFilling((1, 1), gen_animated, solve_animated, True)
            end_time = time.perf_counter()
            solve_time = end_time - start_time
            with open("solve_display_times.txt", "a") as file:
                file.write(f"{maze.width}x{maze.width} cells: {str(solve_time)} seconds\n")
        else:
            maze.deadEndFilling((1, 1), gen_animated, solve_animated, True)

    if gen_ani_switch.checkPressed(screen):
        gen_animated = not gen_animated

    if solve_ani_switch.checkPressed(screen):
        solve_animated = not solve_animated

    if save_button.checkPressed():

        with open("image_counter.txt", "r") as file:
            imageCounter = int(file.read())
        with open("image_counter.txt", "w") as file:
            file.write(str(imageCounter + 1))
        pygame.image.save(saved_surface, f"screenshots/maze{imageCounter}.jpg")

    text_box.draw(screen)
    maze.displayNumCells(num_cells_display, font)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if text_box.checkSelected():
            if event.type == pygame.TEXTINPUT and event.text.isdigit() and len(num_cells_display) < 4:
                num_cells_display += event.text
                num_cells = int(num_cells_display)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(num_cells_display) > 1:
                        num_cells_display = num_cells_display[:-1]
                        num_cells = int(num_cells_display)
                    else:
                        num_cells_display = ""
                        num_cells = 0


        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                #pygame.draw.rect(screen, DISPLAY_COLOUR, pygame.Rect(player_x, player_y, 10, 10))
                player_y -= cell_height

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                #pygame.draw.rect(screen, DISPLAY_COLOUR, pygame.Rect(player_x, player_y, 10, 10))
                player_x -= cell_width

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                #pygame.draw.rect(screen, DISPLAY_COLOUR, pygame.Rect(player_x, player_y, 10, 10))
                player_y += cell_height

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                #pygame.draw.rect(screen, DISPLAY_COLOUR, pygame.Rect(player_x, player_y, 10, 10))
                player_x += cell_width

    pygame.display.update()
    clock.tick(60)
pygame.quit()