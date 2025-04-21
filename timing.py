from mazeGenerator import Maze
import time
import matplotlib.pyplot as plt
import numpy as np

maze = Maze(50, [], False)

def timeGeneration(num_cells):
    maze.__init__(num_cells, [], False)

    start_time = time.perf_counter()
    maze.recursiveBacktracking((1, 1), False)
    end_time = time.perf_counter()
    gen_time = end_time - start_time

    return gen_time

def generationProfile(lower_bound, upper_bound, repeats):
    if lower_bound < 2:
        lower_bound = 2
    profile = []
    for num_cells in range(lower_bound, upper_bound + 1):
        average = 0
        for _ in range(repeats):
            timeTaken = timeGeneration(num_cells)
            average += timeTaken
            with open("generation_times.txt", "a") as file:
                file.write(f"{num_cells} {timeTaken}\n")
        average /= repeats
        profile.append([num_cells, average])
        print(f"{num_cells}: {average}")
    return profile

def timeSolving(num_cells):
    maze.__init__(num_cells, [], False)
    maze.recursiveBacktracking((1, 1), False)

    start_time = time.perf_counter()
    maze.deadEndFilling((1, 1), False, False, False)
    end_time = time.perf_counter()
    solve_time = end_time - start_time

    return solve_time

def solvingProfile(lower_bound, upper_bound, repeats):
    if lower_bound < 2:
        lower_bound = 2
    profile = []
    for num_cells in range(lower_bound, upper_bound + 1):
        average = 0
        for _ in range(repeats):
            timeTaken = timeSolving(num_cells)
            average += timeTaken
            with open("solving_times.txt", "a") as file:
                file.write(f"{num_cells} {timeTaken}\n")
        average /= repeats
        profile.append([num_cells, average])
        print(f"{num_cells}: {average}")
    return profile


def interpretFile(filename):
    with open(filename, "r") as file:
        timingData = file.read()
    timingData = timingData.split("\n")
    timingData = timingData[0:-1]
    for i in range(len(timingData)):
        timingData[i] = timingData[i].split(" ")
        timingData[i][0] = int(timingData[i][0])
        timingData[i][1] = float(timingData[i][1])
    max_num_cell = 0
    for entry in timingData:
        if entry[0] > max_num_cell:
            max_num_cell = entry[0]
    average_times = []
    for i in range(2, max_num_cell + 1):
        average = 0
        num_occurrences = 0
        for entry in timingData:
            if entry[0] == i:
                num_occurrences += 1
                average += entry[1]
        average /= num_occurrences
        average_times.append(average)
    list_num_cells = [i for i in range(2, max_num_cell + 1)]
    return list_num_cells, average_times

solveX, solveY = interpretFile("solving_times.txt")
genX, genY = interpretFile("generation_times.txt")

model1 = np.poly1d(np.polyfit(solveX, solveY, 3))
polyline1 = np.linspace(1, 500, 1000)

model2 = np.poly1d(np.polyfit(genX, genY, 2))
polyline2 = np.linspace(1, 500, 1000)

plt.scatter(solveX, solveY, s=0.1)
plt.scatter(genX, genY, s=0.1)
plt.plot(polyline1, model1(polyline1), label="Solving: O(n^3)")
plt.plot(polyline2, model2(polyline2), label="Generating: O(n^2)")
plt.legend()
plt.xlabel("Maze Width (Num. Cells)")
plt.ylabel("Time Taken (Seconds)")
plt.title("Time Efficiency of Maze Generation and Solving")
plt.show()