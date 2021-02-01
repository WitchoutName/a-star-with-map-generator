import pygame, sys, os, random
from pygame import locals
from classes.Map import Map
from classes.Car import Car

# FIRST PARAMETER IS NAME OF A MAP EXISTING IN MAPS FOLDER

pygame.init()
clock = pygame.time.Clock()
pygame.font.init()
running = True
window = pygame.display.set_mode((900, 900))
window.fill((255, 255, 255))
index, r = 0, False
map_to_load = ""


def generate_map():
    largest = -1
    for file in os.listdir(os.getcwd() + "/maps"):
        if file.startswith("rmap") and file.endswith(".txt"):
            num = int(file.partition("p")[2].partition(".")[0])
            if num > largest:
                largest = num

    size = 100
    arr = [["." for x in range(size)] for y in range(size)]
    for x in range(round(pow(size, 2) / 2)):
        arr[random.randint(0, size - 1)][random.randint(0, size - 1)] = "X"
    car = [random.randint(0, size - 1), random.randint(0, size - 1)]
    arr[car[0]][car[1]] = "%"
    dump = [random.randint(0, size - 1), random.randint(0, size - 1)]
    while dump == car:
        dump = [random.randint(0, size - 1), random.randint(0, size - 1)]
    arr[random.randint(0, size - 1)][random.randint(0, size - 1)] = "@"
    for x in arr:
        x.append("\n")
    file_str, file_name = "".join("".join(["".join(x) for x in arr])), f"rmap{largest + 1}.txt"
    with open(f"maps/{file_name}", "w") as file:
        file.write(file_str)
        return file_name


if len(sys.argv) > 1 and sys.argv[1].endswith(".txt"):
    with open(f"maps/{map_to_load}", "r") as file:
        map = Map(file)
else:
    i = ""
    while i == "":
        success = False
        while not success:
            map_to_load = generate_map()
            with open(f"maps/{map_to_load}", "r") as file:
                map = Map(file)
            car = Car(map, window)
            success = car.find_dump()
        i = input("Press enter to repeat.")



pygame.quit()
