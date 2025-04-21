from adjacency import generateAdjacentCells
import button
import random
import sys
import pygame
import copy
import time
import threading

sys.setrecursionlimit(1000000)

class Maze:

    def __init__(self, width, menu_components, display):

        if display:
            pygame.init()
        pygame.font.init()

        self.width = width
        self.adjacent_cells = generateAdjacentCells(self.width)
        self.cells = [[Cell((x, y)) for x in range(1, width + 1)] for y in range(1, width + 1)]

        self.DISPLAY_WIDTH = 900
        self.DISPLAY_HEIGHT = 900
        self.DISPLAY_COLOUR = (255, 255, 255)
        self.WALL_COLOUR = (0, 0, 0)

        if display:
            self.screen = pygame.display.set_mode((self.DISPLAY_WIDTH + 500, self.DISPLAY_HEIGHT), pygame.RESIZABLE)
            pygame.display.set_caption("Mazes")

        self.rect_x = 0
        self.rect_y = 0
        self.cell_width = self.DISPLAY_WIDTH / width
        self.cell_height = self.DISPLAY_HEIGHT / width

        self.previous_position = (1, 1)
        self.end_position = (self.width, self.width)

        self.title_font = pygame.font.SysFont("poppins.regular.ttf", 80)

        self.menu_components = menu_components

    def reset(self):
        self.screen.fill(self.DISPLAY_COLOUR)
        self.drawMenu()
        for row in self.cells:
            for cell in row:
                for direction in cell.connections:
                    cell.connections[direction] = False
                    cell.visited = False


    def selectCell(self, position, cells=[False, None]):
        if cells[0]:
            cells = cells[1]
        else:
            cells = self.cells
        return cells[position[1] - 1][position[0] - 1]

    def connectionDirection(self, current_position, next_position):
        delta_position = (next_position[0] - current_position[0], next_position[1] - current_position[1])
        if delta_position == (0, 1):
            return "S"
        elif delta_position == (0, -1):
            return "N"
        elif delta_position == (1, 0):
            return "E"
        elif delta_position == (-1, 0):
            return "W"

    def drawGrid(self):
        for i in range(self.width):
            for j in range(self.width):
                pygame.draw.rect(self.screen, self.WALL_COLOUR,
                                 pygame.Rect(self.rect_x + i * self.cell_width, self.rect_y + j * self.cell_width,
                                             self.cell_width, self.cell_height), 1)
        pygame.display.update()

    def drawMaze(self, cells=[0, None]):

        if cells[0]:
            cells = cells[1]
        else:
            cells = self.cells

        for y in range(1, self.width + 1):
            for x in range(1, self.width + 1):
                if self.selectCell((x, y), cells=[1, cells]).connections["N"]:
                    pygame.draw.rect(self.screen, self.DISPLAY_COLOUR, pygame.Rect(1 + (x - 1) * self.cell_width, (y - 1) * self.cell_height - 1, self.cell_width - 2, 2))
                if self.selectCell((x, y), cells=[1, cells]).connections["E"]:
                    pygame.draw.rect(self.screen, self.DISPLAY_COLOUR, pygame.Rect(x * self.cell_width - 1, (y - 1) * self.cell_height + 1, 2, self.cell_height - 2))

        pygame.display.update()

    def drawMenu(self):
        components = self.menu_components
        self.screen.blit(components[0], (915, 15))
        for i in range(1, len(components)):
            components[i].draw(self.screen)

    def displayNumCells(self, num_cells_display, font):
        used_space = font.size(num_cells_display)
        self.menu_components[5].draw(self.screen)
        text_img = font.render(num_cells_display, True, (0, 0, 0))
        self.screen.blit(text_img, (915 + ((157 - used_space[0]) / 2), 200 + ((87 - used_space[1]) / 2)))

    def removeWall(self, position, direction):
        if direction == "S":
            direction = "N"
            position = (position[0], position[1] + 1)
        if direction == "W":
            direction = "E"
            position = (position[0] - 1, position[1])
        if direction == "N":
            pygame.draw.rect(self.screen, self.DISPLAY_COLOUR, pygame.Rect(1 + (position[0] - 1) * self.cell_width, (position[1] - 1) * self.cell_height - 1, self.cell_width - 2, 2))
        if direction == "E":
            pygame.draw.rect(self.screen, self.DISPLAY_COLOUR, pygame.Rect(position[0] * self.cell_width - 1, (position[1] - 1) * self.cell_height + 1, 2, self.cell_height - 2))

        pygame.display.update()


    def highlightCell(self, cell, colour, trail=False, animated=True):

        width = self.cell_width - 2
        height = self.cell_height - 2
        y = (cell.position[1] - 1) * self.cell_height + 1
        x = (cell.position[0] - 1) * self.cell_width + 1
        previous_x = (self.previous_position[0] - 1) * self.cell_width + 1
        previous_y = (self.previous_position[1] - 1) * self.cell_height + 1

        if trail:

            if cell.connections["N"]:
                y -= 2
                height += 2
            if cell.connections["E"]:
                width += 2
            if cell.connections["S"]:
                height += 2
            if cell.connections["W"]:
                x -= 2
                width += 2

        if not trail:
            pygame.draw.rect(self.screen, self.DISPLAY_COLOUR, pygame.Rect(previous_x, previous_y, width, height))

        pygame.draw.rect(self.screen, colour, pygame.Rect(x, y, width, height))

        if animated:
            pygame.display.update()

        self.previous_position = cell.position

    def removeHighlightedCell(self):
        pygame.draw.rect(self.screen, self.DISPLAY_COLOUR, pygame.Rect((self.previous_position[0] - 1) * self.cell_width + 1, (self.previous_position[1] - 1) * self.cell_height + 1, self.cell_width - 2, self.cell_height - 2))
        pygame.display.update()

    def recursiveBacktracking(self, start_position, animated):

        current_position = start_position
        self.selectCell(current_position).visited = True

        possible_next_positions = []
        for adjacent_position in self.adjacent_cells[current_position]:
            if not self.selectCell(adjacent_position).visited:
                possible_next_positions.append(adjacent_position)
        while possible_next_positions:
            next_position = random.choice(possible_next_positions)
            direction = self.connectionDirection(current_position, next_position)
            self.selectCell(current_position).updateConnection(direction, self)
            if animated:
                self.highlightCell(self.selectCell(current_position), (255, 0, 0))
                self.removeWall(current_position, direction)
            self.recursiveBacktracking(next_position, animated)
            possible_next_positions = []
            for adjacent_position in self.adjacent_cells[current_position]:
                if not self.selectCell(adjacent_position).visited:
                    possible_next_positions.append(adjacent_position)
        if animated:
            self.removeHighlightedCell()


    def randomMouse(self, start_position):
        end_position = (self.width, self.width)
        current_position = start_position
        while current_position != end_position:
            possible_connections = []
            for connection in self.selectCell(current_position).connections:
                if self.selectCell(current_position).connections[connection]:
                    possible_connections.append(connection)
            chosen_connection = random.choice(possible_connections)
            if chosen_connection == "N":
                current_position = (current_position[0], current_position[1] - 1)
            elif chosen_connection == "E":
                current_position = (current_position[0] + 1, current_position[1])
            elif chosen_connection == "S":
                current_position = (current_position[0], current_position[1] + 1)
            elif chosen_connection == "W":
                current_position = (current_position[0] - 1, current_position[1])
            self.highlightCell(self.selectCell(current_position), (255, 0, 0))


    def deadEndFilling(self, start_position, gen_animated, solve_animated, display):
        original_cells = copy.deepcopy(self.cells)
        end_position = (self.width, self.width)
        for row in self.cells:
            for cell in row:
                dead_end = cell.checkForDeadEnd([start_position, end_position])
                current_cell = cell
                while dead_end:
                    next_cell_position = current_cell.findConnectedCells()[0]
                    next_direction = self.connectionDirection(current_cell.position, next_cell_position)
                    next_cell = self.selectCell(next_cell_position)
                    if solve_animated:
                        self.highlightCell(current_cell, (255, 209, 220), True)
                    current_cell.updateConnection(next_direction, self, create=False)
                    current_cell = next_cell
                    dead_end = current_cell.checkForDeadEnd([start_position, end_position])
        current_cell = self.selectCell(start_position)
        solution_cells = []
        if solve_animated:
            self.highlightCell(current_cell, (119, 221, 119), True)
        solution_cells.append(copy.deepcopy(current_cell))
        while current_cell.position != end_position:
            next_cell_position = current_cell.findConnectedCells()[0]
            next_direction = self.connectionDirection(current_cell.position, next_cell_position)
            next_cell = self.selectCell(next_cell_position)
            current_cell.updateConnection(next_direction, self, create=False)
            current_cell = next_cell
            if solve_animated:
                self.highlightCell(current_cell, (119, 221, 119), True)
            solution_cells.append(copy.deepcopy(current_cell))
        if display:
            self.screen.fill(self.DISPLAY_COLOUR)
            self.drawMenu()
            self.displayNumCells(str(self.width), pygame.font.SysFont("Arial.ttf", size=75))
            self.drawGrid()
            self.drawMaze([1, original_cells])
            for cell in solution_cells:
                self.highlightCell(cell, (119, 221, 119), trail=True, animated=False)


class Cell:

    def __init__(self, position):
        self.position = position
        self.visited = False
        self.dead_end = False
        self.connections = {"N": False, "E": False, "S": False, "W": False}

    def updateConnection(self, direction, maze, create=True):
        self.connections[direction] = create
        if direction == "N":
            delta_position = (0, -1)
            inverse_direction = "S"
        elif direction == "E":
            delta_position = (1, 0)
            inverse_direction = "W"
        elif direction == "S":
            delta_position = (0, 1)
            inverse_direction = "N"
        elif direction == "W":
            delta_position = (-1, 0)
            inverse_direction = "E"
        else:
            delta_position = (0, 0)
            inverse_direction = ""
        adjacent_pos = (self.position[0] + delta_position[0], self.position[1] + delta_position[1])
        adjacent_cell = maze.selectCell(adjacent_pos)
        adjacent_cell.connections[inverse_direction] = create

    def checkForDeadEnd(self, excluded_cells):
        current_connections = 0
        direction_of_connections = []
        for direction in self.connections:
            if self.connections[direction]:
                current_connections += 1
                direction_of_connections.append(direction)
        if current_connections == 1 and not self.position in excluded_cells:
            return True
        return False

    def findConnectedCells(self):
        connected_positions = []
        for direction in self.connections:
            if self.connections[direction]:
                if direction == "N":
                    connected_positions.append((self.position[0], self.position[1] - 1))
                if direction == "E":
                    connected_positions.append((self.position[0] + 1, self.position[1]))
                if direction == "S":
                    connected_positions.append((self.position[0], self.position[1] + 1))
                if direction == "W":
                    connected_positions.append((self.position[0] - 1, self.position[1]))
        return connected_positions

#maze1 = Maze(50, [], False)

"""

FIRST ATTEMPT AT A GOOD IMPLEMENTATION

    def deadEndFilling(self, start_position):
        end_position = (self.width, self.width)
        for row in self.cells:
            for cell in row:
                dead_end = True
                current_cell = cell
                while dead_end:
                    current_connections = 0
                    new_position = (0, 0)
                    for direction in current_cell.connections:
                        if current_cell.connections[direction]:
                            current_connections += 1
                    if current_connections == 1 and not current_cell.position in [start_position, end_position]:
                        for direction in current_cell.connections:
                            if current_cell.connections[direction]:
                                print("Dead end")
                                if direction == "N":
                                    new_position = (current_cell.position[0], current_cell.position[1] - 1)
                                if direction == "E":
                                    new_position = (current_cell.position[0]  + 1, current_cell.position[1])
                                if direction == "S":
                                    new_position = (current_cell.position[0], current_cell.position[1] + 1)
                                if direction == "W":
                                    new_position = (current_cell.position[1] - 1, current_cell.position[1])
                                current_cell.updateConnection(direction, self, create=False)
                        self.highlightCell(current_cell.position, (0, 255, 0), True)
                    else:
                        dead_end = False
                    print(current_cell.position, new_position)
                    current_cell = self.selectCell(new_position)
                    time.sleep(0.1)
"""

"""

ORIGINAL BAD IMPLEMENTATION

def deadEndFilling(self, start_position):
    end_position = (self.width, self.width)
    change = True
    while change:
        for row in self.cells:
            change = False
            for cell in row:
                current_connections = 0
                for direction in cell.connections:
                    if cell.connections[direction]:
                        current_connections += 1
                print(current_connections)
                if current_connections == 1 and not cell.position in [start_position, end_position]:
                    for direction in cell.connections:
                        if cell.connections[direction]:
                            cell.updateConnection(direction, self, create=False)
                    change = True
                    self.highlightCell(cell.position, (0, 255, 0), True)
"""
