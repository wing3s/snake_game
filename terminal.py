import curses
from snake_game import snake_game

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0, 2, "Hit arrow keys to play!")
stdscr.addstr(1, 2, "Hit 'q' to quit")
stdscr.refresh()

key_actions = {
    curses.KEY_UP: (0, -1),
    curses.KEY_DOWN: (0, 1),
    curses.KEY_LEFT: (-1, 0),
    curses.KEY_RIGHT: (1, 0)
}

game = snake_game()
game.next()

while True:
    try:
        key = stdscr.getch()
        if key == ord('q'):
            break

        screen, reward = game.send(key_actions[key])
        stdscr.addstr(2, 4, "Reward: "+str(reward))
        screen_y = 5
        for row in screen:
            row_str = " ".join("F" if val == .5 else str(int(val)) for val in row)
            stdscr.addstr(screen_y, 0, row_str)
            screen_y += 1
    except:
        break

curses.echo()
curses.nocbreak()
curses.endwin()
