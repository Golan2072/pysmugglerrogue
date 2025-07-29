import random
from datetime import date, timedelta
import screens


def dice(number, sides):
    roll = 0
    for i in range(0, number):
        roll += random.randint(0, sides)
    return roll


def random_line(filename):
    with open(filename, "r") as line_list:
        line = random.choice(line_list.readlines())
        line = line.strip()
    return line


def sector_gen():
    starmap = screens.generate_empty_starmap()
    for column in range(1, 9):
        for row in range(1, 11):
            if dice(1, 6) >= 4:
                starmap[column][row] = {
                    "Name": random_line("data\worlds.txt"), "Trade Class": "Placeholder", "Tech": "Placeholder", "Law": 0}
            else:
                starmap[column][row] = None
    name_list = []
    for column in range(1, 9):
        for row in range(1, 11):
            if starmap[column][row] == None:
                pass
            else:
                if starmap[column][row]["Name"] not in name_list:
                    name_list.append(starmap[column][row]["Name"])
                elif starmap[column][row]["Name"] in name_list:
                    starmap[column][row]["Name"] = random_line(
                        "data\worlds.txt")
                    name_list.append(starmap[column][row]["Name"])

    return starmap


class Game:
    def __init__(self, starmap):
        self.version = 0.02
        self.far_future = date(2999, 12, 21)
        self.character = Character()
        self.starmap = starmap
        self.starship = Starship()

    def new_day(self):
        self.far_future += timedelta(days=1)

    def new_game_start(self):
        if self.starmap[1][1] != None:
            pass
        else:
            for column in range(1, 9):
                for row in range(1, 11):
                    if self.starmap[column][row] == None:
                        pass
                    else:
                        self.character.location = (column, row)
                        break
                break


class Character:
    def __init__(self):
        self.name = "Default"
        self.location = (1, 1)
        self.credits = 0

    def set_name(self, name):
        self.name = name


class Starship:
    def __init__(self):
        self.name = "Tokay"
        self.shipclass = "Gecko"
        self.tonnage = 100
        self.cargo = 20
        self.max_fuel = 20
        self.current_fuel = 20
        self.fuel_per_parsec = 0.1*self.tonnage
        self.ftl_rating = 2
        self.hull_integrity = 6


if __name__ == "__main__":
    pass
