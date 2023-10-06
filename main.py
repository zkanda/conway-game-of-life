import curses
import random


stdscr = curses.initscr()


height, width = stdscr.getmaxyx()

initial_world_population = [[False for x in range(width)] for y in range(height)]

initial_world_population[2][2] = True
initial_world_population[3][3] = True
initial_world_population[4][1] = True
initial_world_population[4][2] = True
initial_world_population[4][3] = True

for row in initial_world_population:
    for x in range(len(row)):
        row[x] = not bool(random.randint(0, 2))


def will_be_alive(is_alive, live_neighbours):
    # get the neighbours

    if is_alive and live_neighbours < 2:
        return False

    elif is_alive and (live_neighbours == 2 or live_neighbours == 3):
        return True

    elif is_alive and live_neighbours > 3:
        return False

    elif not is_alive and  live_neighbours == 3:
        return True

    return False


def get_coordinates(y, x, max_y, max_x):

    first_row = [(y - 1, x - 1), (y, x - 1), (y + 1, x - 1)]

    second_row = [(y -1 , x), (y + 1, x)]

    third_row = [(y - 1, x + 1), (y, x+ 1), (y + 1, x + 1)]

    # filter the valid coordinates

    total_coordinates = first_row + second_row + third_row

    filtered_coordinates = []

    for y, x in total_coordinates:
        if y >= 0 and x >= 0  and y < max_y and x < max_x:
            filtered_coordinates.append((y, x))

    return filtered_coordinates


def determine_neighbours(population, y, x):
    coordinates = get_coordinates(y, x, len(population), len(population[0]))

    neighbours = []

    for y, x in coordinates:
        neighbours.append(population[y][x])

    # we get the number of alive neighbours
    return neighbours


def get_live_neighbours(population, y, x):
    # determine the neighbours
    neighbors = determine_neighbours(population, y, x)

    return len([n for n in neighbors if n])



def apply_rules(population):
    #
    #return [[will_be_alive(x) get_the_neighbours for x in range(len(population(y)))] for y in range(len(population))]

    new_population = []

    for y in range(len(population)):
        temp_list = []
        for x in range(len(population[y])):
            temp_list.append(will_be_alive(population[y][x], get_live_neighbours(population, y, x)))
        new_population.append(temp_list)

    return new_population


def draw_grid(grid):
    for y, column in enumerate(grid):
        for x, cell in enumerate(column):
            try:
                stdscr.addch(y, x, "*" if cell  else "_")
            except curses.error:
                pass

    stdscr.refresh()


if __name__ == "__main__":
    try:
        world_population = initial_world_population
        while True:
            world_population = apply_rules(world_population)
            draw_grid(world_population)
            import time
            time.sleep(.001)
    except KeyboardInterrupt:
        curses.endwin()
