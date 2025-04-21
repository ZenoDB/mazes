
def generateAdjacentCells(maze_width):

    adjacent_cells = {}
    for y in range(1, maze_width + 1):
        for x in range(1, maze_width + 1):
            individual_connections = []
            if x == 1 and y == 1:
                individual_connections += [(x + 1, y), (x, y + 1)]
            elif x == 1 and y == maze_width:
                individual_connections += [(x + 1, y), (x, y - 1)]
            elif x == maze_width and y == 1:
                individual_connections += [(x - 1, y), (x, y + 1)]
            elif x == maze_width and y == maze_width:
                individual_connections += [(x - 1, y), (x, y - 1)]
            elif x == 1:
                individual_connections += [(x, y - 1), (x, y + 1), (x + 1, y)]
            elif x == maze_width:
                individual_connections += [(x, y - 1), (x, y + 1), (x - 1, y)]
            elif y == 1:
                individual_connections += [(x - 1, y), (x + 1, y), (x, y + 1)]
            elif y == maze_width:
                individual_connections += [(x - 1, y), (x + 1, y), (x, y - 1)]
            else:
                individual_connections += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            adjacent_cells[(x, y)] = individual_connections

    return adjacent_cells