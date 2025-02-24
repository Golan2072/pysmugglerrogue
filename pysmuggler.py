import json
import random
import os
import platform


def yn():
    query = True
    while query:
        answer = input("Y/N: ")
        if answer.lower() == "y" or "yes":
            return True
            break
        if answer.lower() == "n" or "no":
            return False
            break
        else:
            print("Invalid Answer")


def dice(n, sides):
    die = 0
    roll = 0
    while die < n:
        roll = roll + random.randint(1, sides)
        die += 1
    return roll


def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def random_line(filename):
    with open(filename, "r") as line_list:
        line = random.choice(line_list.readlines())
        line = line.strip()
    return line


def list_stringer(input_list):
    output_list = []
    for item in input_list:
        output_list.append(str(item))
    return ' '.join(output_list)


def generate_empty_starmap():
    starmap = {}
    for column in range(1, 10):
        starmap[column] = {}
        for row in range(0, 12):
            starmap[column][row] = ["       ", " "]
    return starmap


def hex_number(column, row, starmap):
    if starmap[column][row][1] == " ":
        return "___"
    elif row == 10:
        return f"{column}10"
    else:
        return f"{column}0{row}"


def base_row(base_row_string):
    row_string = ""
    for i in range(0, 4):
        row_string += base_row_string
    return row_string


class Screen:
    def __init__(self, game):
        self.screen_title = ""
        self.previous = ""
        self.screen_string = ""
        self.menu_options = []

    def render_screen(self):
        print(self.screen_title, "\n")
        print(self.screen_string, "\n")
        for i, v in enumerate(self.menu_options):
            print(f"{i+1}. {self.menu_options[i][0]}")
        print(f"{len(self.menu_options)+1}. Exit")

    def menu(self):
        while True:
            self.render_screen()
            choice = input("Please enter your chosen option number: ")
            if choice == "":
                choice = -1
            if int(choice) in range (0, len(self.menu_options)+1):
                menu_method = self.menu_options[int(choice)-1][1]
                menu_method()
                clear_screen()
            elif int(choice) == len(self.menu_options)+1:
                break
            else:
                print("Invalid Choice; please input one of the menu items numbers.")
                input()
                clear_screen()


class Starmap_screen(Screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mS T A R   M A P"
        self.menu_options = [("Option1", self.method1), ("Option2", self.method2)]
        self.cursor = game.location
        self.starmap = game.starmap
        self.screen_string = self.render_starmap()

    def render_starmap(self):
        star_string = f"\u001b[32m"
        row = 1
        for column in self.starmap:
            for row in self.starmap:
                if column == self.cursor[1]:
                    if row == self.cursor[0]:
                        self.starmap[row][column][1] = "\u001b[31m@\u001b[32m"
        star_string += " ___     ___     ___     ___ \n"
        for row in range(1, 11):
            star_string += f"/ {self.starmap[1][row][1]} \\{hex_number(2, row-1, self.starmap)}/ {self.starmap[3][row][1]} \\{hex_number(4, row, self.starmap)}/ {self.starmap[5][row][1]} \\{hex_number(6, row-1, self.starmap)}/ {self.starmap[7][row][1]} \\{hex_number(8, row-1, self.starmap)}/ \n"
            star_string += f"\\{hex_number(1, row, self.starmap)}/ {self.starmap[2][row][1]} \\{hex_number(3, row, self.starmap)}/ {self.starmap[4][row][1]} \\{hex_number(5, row, self.starmap)}/ {self.starmap[6][row][1]} \\{hex_number(7, row, self.starmap)}/ {self.starmap[8][row][1]} \\ \n"
        star_string += f"    \\{hex_number(2, 10, self.starmap)}/   \\{hex_number(4, 10, self.starmap)}/   \\{hex_number(6, 10, self.starmap)}/   \\{hex_number(8, 10, self.starmap)}/\n"
        star_string += "\u001b[0m"
        return star_string
    
    def method1(self):
        print("Choice 1 Selected, press Enter to continue.")
        input()

    def method2(self):
        print("Choice 2 Selected, press Enter to continue.")
        input()


class Trade_screen (Screen):
    def __init__(self, game):
        super().__init__(game)


class Starship:
    def __init__(self, name):
        self.name = name
        self.tonnage = 0
        self.cargo_space = 0
        self.fuel = 0
        self.manifesto = {}
        self.jump_rating = 0


class Game:
    def __init__(self, location, starmap):
        self.starship_data = Starship
        self.location = location
        self.starmap = starmap

    def save_game(self):
        save_dir = os.path.join(os.getcwd(), 'savegames')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        savegame_name = input("Enter the savegame name: ").strip()
        savegame_path = os.path.join(save_dir, f"{savegame_name}.json")
        if os.path.exists(savegame_path):
            overwrite = input(
                f"'{savegame_name}.json' already exists. Do you want to overwrite it? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Save operation cancelled.")
                return
        save_data = {
            "name": self.starship_data.name,
            "tonnage": self.starship_data.tonnage,
            "jump_rating": self.starship_data.jump_rating
        }
        with open(savegame_path, 'w') as save_file:
            json.dump(save_data, save_file, indent=4)
        print(f"Game saved successfully as '{savegame_name}.json'")

    def load_game(self):
        save_dir = os.path.join(os.getcwd(), 'savegames')
        if not os.path.exists(save_dir):
            print("No saved games found.")
            return None
        save_files = [f for f in os.listdir(save_dir) if f.endswith('.json')]
        if not save_files:
            print("No saved games found.")
            return None
        print("Available saved games:")
        for save_file in save_files:
            print(f" - {os.path.splitext(save_file)[0]}")
        load_loop = True
        while load_loop:
            savegame_name = input("Enter the savegame name to load: ").strip()
            savegame_path = os.path.join(save_dir, f"{savegame_name}.json")
            if not os.path.exists(savegame_path):
                print(
                    f"No save file found with the name '{savegame_name}.json'.")
            else:
                with open(savegame_path, 'r') as save_file:
                    save_data = json.load(save_file)
                    break
        print(f"Game loaded successfully from '{savegame_name}.json'")
        input("Press any key to continue: ")
        self.starship_data.name = save_data["name"]
        self.starship_data.tonnage = save_data["tonnage"]
        self.starship_data.jump_rating = save_data["jump_rating"]


if __name__ == "__main__":
    starmap = generate_empty_starmap()
    starmap[1][1] = ["ALPHA  ", "\u001b[33m*\u001b[32m"]
    starmap[2][2] = ["BETA   ", "\u001b[33m*\u001b[32m"]
    starmap[2][4] = ["GAMMA  ", "\u001b[33m*\u001b[32m"]
    starmap[3][5] = ["DELTA  ", "\u001b[33m*\u001b[32m"]
    starmap[7][10] = ["OMEGA  ", "\u001b[33m*\u001b[32m"]
    starmap[8][10] = ["ZETA  ", "\u001b[33m*\u001b[32m"]
    game = Game((1,1), starmap)
    screen = Starmap_screen(game)
    screen.menu()
