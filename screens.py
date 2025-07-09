import os
import platform
import math


class GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class Getch:
    def __init__(self):
        try:
            self.impl = GetchWindows()
        except ImportError:
            self.impl = GetchUnix()

    def __call__(self):
        return self.impl()


def getkeypress():
    if platform.system() == "Windows":
        directory = os.listdir(".\\")
        key = Getch()
        return key().decode()
    else:
        key = Getch()
        return key()

def yn():
    while True:
        print("please press Y to confirm or N to cancel")
        try:
            keypress = getkeypress()
            if str(keypress).upper() == "Y":
                return True
                break
            elif str(keypress).upper() == "N":
                return False
                break
            else:
                print("Invalid choice")
        except UnicodeDecodeError:
                choice = None

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def calculate_distance(origin_hexagon, destination_hexagon): #both Hexagon objects
    return max(abs(origin_hexagon.x - destination_hexagon.x), abs(origin_hexagon.y - destination_hexagon.y), abs(origin_hexagon.z - destination_hexagon.z))
 

def generate_empty_starmap():
    starmap = {}
    for column in range(1, 10):
        starmap[column] = {}
        for row in range(0, 12):
            starmap[column][row] = ["       ", " "]
    return starmap


def menu_stringer(menu_dict):
    menu_string = ""
    i = 0
    for key in menu_dict.keys():
        if i%4 == 0:
            menu_string = menu_string[:-2]
            menu_string += "\n"
        menu_string += key + " " + menu_dict[key][0] + ", "
        i += 1
    return menu_string[:-2]


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

class Hexagon():
    def __init__(self, coords): # 3-digit string coords
        if int(coords[1]) == 1:
            self.column = int(coords[0])  
            self.row = 10
        else:
            self.column = int(coords[0])
            self.row = int(coords[2])
        self.x = self.column
        self.z = self.row - (self.column + (self.column&1)) // 2
        self.y = -self.x - self.z

class Game_screen:
    def __init__(self, game):
        self.game = game
        self.screen_title = ""
        self.screen_string = ""
        self.menu_options = {"Z": ("Main Menu", self.main_menu), "A": ("Character", self.character_menu), "C": ("Cargo", self.cargo_menu), "S": (
            "Ship", self.ship_menu), "N": ("Navigation", self.navigation_menu), "M": ("Market", self.market_menu), "Y": ("Shipyard", self.shipyard_menu), "B": ("Job Board", self.job_board_menu)}
        self.particular_menu_options = {}

    def render_screen(self):
        pass

    def menu(self):
        if self.particular_menu_options != {}:
            self.menu_options = self.menu_options | self.particular_menu_options
        else:
            pass
        self.render_screen()
        print()
        print("\u001b[32mPlease press your chosen key: ")
        while True:
            try:
                choice = str(getkeypress()).upper()
                if choice in self.menu_options.keys():
                    method_choice = self.menu_options[choice][1]
                    method_choice()
                    break
                else:
                    print("\u001b[32mInvalid choice; please choose again")
            except UnicodeDecodeError:
                choice = None

    def render_general_features(self):
        clear_screen()
        self.menu_string = menu_stringer(self.menu_options)
        print(f"\u001b[32mPySmuggler v{self.game.version}")
        print()
        print(self.screen_title)
        print("-"*50)
        print(self.menu_string)
        print("-"*50)
        print(f"Current Terran Credits {self.game.character.credits}")
        print()

    def purchase(self, cost):
        if self.game.character.credits >= cost:
            self.game.character.credits -= cost
            return True
        else:
            print("insufficient credits")
            input("Press Enter to continue")
            return False
    
    def main_menu(self):
        menu = Main_screen(self.game)
        menu.menu()

    def ship_menu(self):
        menu = Ship_screen(self.game)
        menu.menu()

    def cargo_menu(self):
        menu = Cargo_screen(self.game)
        menu.menu()

    def navigation_menu(self):
        menu = Navigation_screen(self.game)
        menu.menu()

    def market_menu(self):
        menu = Market_screen(self.game)
        menu.menu()

    def shipyard_menu(self):
        menu = Shipyard_screen(self.game)
        menu.menu()

    def job_board_menu(self):
        menu = Job_board_screen(self.game)
        menu.menu()

    def character_menu(self):
        menu = Character_screen(self.game)
        menu.menu()

class Main_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.particular_menu_options = {"X": ("Exit Game", self.exit_game)}
        self.screen_title = "\u001b[32mMain Screen"

    def render_screen(self):
        self.render_general_features()
        print(f"PySmuggler {self.game.version}\n\nBy Omer Golan-Joel\n\nMain Screen")

    def exit_game(self):
        quit()

class Cargo_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mCargo Screen"

    def render_screen(self):
        self.render_general_features()
        print("Cargo")


class Ship_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mShip Screen"

    def render_screen(self):
        self.render_general_features()
        print("Ship")

class Job_board_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mJob Board Screen"

    def render_screen(self):
        self.render_general_features()
        print("Job Board")

class Navigation_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mNavigation Screen"
        self.cursor = game.character.location
        self.starmap = game.starmap
        self.particular_menu_options = {"J": ("Jump", self.jump), "I": ("Information", self.information)}

    def render_screen(self):
        self.render_general_features()
        print(f"Fuel: {self.game.starship.current_fuel} tons, sufficient for {self.game.starship.current_fuel/self.game.starship.fuel_per_parsec} Parsecs; Maximum FTL Range {self.game.starship.ftl_rating} Parsecs")
        print(self.render_starmap())

    def render_starmap(self):
        star_string = f"\u001b[32m"
        row = 1
        for column in self.starmap:
            for row in self.starmap:
                if column == self.cursor[1]:
                    if row == self.cursor[0]:
                        self.starmap[row][column][1] = "\u001b[31m@\u001b[32m"
                else:
                    pass
        star_string += " ___     ___     ___     ___ \n"
        for row in range(1, 11):
            star_string += f"/ {self.starmap[1][row][1]} \\{hex_number(2, row-1, self.starmap)}/ {self.starmap[3][row][1]} \\{hex_number(4, row-1, self.starmap)}/ {self.starmap[5][row][1]} \\{hex_number(6, row-1, self.starmap)}/ {self.starmap[7][row][1]} \\{hex_number(8, row-1, self.starmap)}/ \n"
            star_string += f"\\{hex_number(1, row, self.starmap)}/ {self.starmap[2][row][1]} \\{hex_number(3, row, self.starmap)}/ {self.starmap[4][row][1]} \\{hex_number(5, row, self.starmap)}/ {self.starmap[6][row][1]} \\{hex_number(7, row, self.starmap)}/ {self.starmap[8][row][1]} \\ \n"
        star_string += f"    \\{hex_number(2, 10, self.starmap)}/   \\{hex_number(4, 10, self.starmap)}/   \\{hex_number(6, 10, self.starmap)}/   \\{hex_number(8, 10, self.starmap)}/\n"
        star_string += "\u001b[0m"
        return star_string

    def jump(self):
        clear_screen()
        print("\u001b[32mJump Destination Selection")
        print(self.render_starmap())
        destination = input("\u001b[32mPlease enter destination coordinates: ")
        current_location_string = f"{self.game.character.location[0]}0{self.game.character.location[1]}"
        origin_hex = Hexagon(current_location_string)
        destination_hex = Hexagon(destination)
        if origin_hex.column == destination_hex.column and origin_hex.row == destination_hex.row:
            print("You are already there...")
        elif self.starmap[destination_hex.column][destination_hex.row][1] != "\u001b[33m*\u001b[32m":
            print("No gravity well detected at destination")
        elif calculate_distance(origin_hex, destination_hex) > self.game.starship.ftl_rating:
            print(f"Your FTL Rating is {self.game.starship.ftl_rating}, which is insufficient for this jump.")
        elif self.game.starship.current_fuel < self.game.starship.fuel_per_parsec*calculate_distance(origin_hex, destination_hex):
            print("Insufficient Fuel")
        elif calculate_distance(origin_hex, destination_hex) <= self.game.starship.ftl_rating:
            self.game.character.location = (destination_hex.column, destination_hex.row)
            self.game.starship.current_fuel -= self.game.starship.fuel_per_parsec*calculate_distance(origin_hex, destination_hex)
            print("Jump Completed!")
        else:
            pass
        input("Press Enter to proceed")
        self.cursor = self.game.character.location
        self.starmap[origin_hex.column][origin_hex.row][1] = "\u001b[33m*\u001b[32m"
        self.menu()
    
    def information(self):
        pass

class Market_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mMarket Screen"

    def render_screen(self):
        self.render_general_features()
        print("Market")


class Shipyard_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mMarket Screen"
        self.particular_menu_options = {"F": ("Refuel", self.refuel)}

    def render_screen(self):
        self.render_general_features()
        print("Shipyard and Fuel Depot")
        print(f"Fuel {self.game.starship.current_fuel} tons out of {self.game.starship.max_fuel} tons")
        print (f"Refuel cost {50*(self.game.starship.max_fuel - self.game.starship.current_fuel)} Terran Credits")
        
    def refuel(self):
        cost = 50*(self.game.starship.max_fuel - self.game.starship.current_fuel)
        print(f"Refuel cost {cost}, proceed?")
        choice = yn()
        if choice:
            if self.game.starship.current_fuel == self.game.starship.max_fuel:
                print("Fuel tank already full!")
                input("Press Enter to continue")
                self.menu()
            elif self.purchase(cost):
                self.game.starship.current_fuel = self.game.starship.max_fuel
                print ("Ship Refueled")
                input("Press Enter to continue")
                self.menu()
            else:
                pass
        else:
            print("Refeul cancelled.")
            input("Press Enter to continue")
            self.menu()

class Character_screen (Game_screen):
    def __init__(self, game):
        super().__init__(game)
        self.screen_title = "\u001b[32mCharacter Screen"

    def render_screen(self):
        self.render_general_features()
        print("Character")