import games
import screens

if __name__=="__main__":
    starmap = games.sector_gen()
    session = games.Game(starmap)
    session.new_game_start()
    session.character.credits = 100000
    current_screen = screens.Main_screen(session)
    current_screen.menu()
