from collections import namedtuple
import numpy as np

Fruit = namedtuple('Fruit', ['x', 'y'])


def snake_game(width=15, height=10, snake_length=3):
    assert width - 2 > snake_length
    possible_actions = ((0, 1), (0, -1), (1, 0), (-1, 0), (0, 0))
    action = (-1, 0)
    prev_action = action
    head_x = width // 2 - snake_length // 2
    snake = [(x, height//2) for x in xrange(head_x, head_x+snake_length)]
    grow = False

    screen = np.zeros((height, width))
    screen[[0, -1]] = 1
    screen[:, [0, -1]] = 1
    boarders_sum = screen.sum()

    for seg in snake:
        screen[seg[1], seg[0]] = 1

    fruit = getFruit(screen, width, height)
    screen[fruit.y, fruit.x] = .5

    while True:
        game_end = (len(snake) > len(set(snake)) or
                    screen.sum() < boarders_sum + len(snake))
        reward = -1 * game_end

        if screen[fruit.y, fruit.x] > .5:
            grow = True
            reward = len(snake)
            fruit = getFruit(screen, width, height)
            screen[fruit.y, fruit.x] = .5

        action = yield screen, reward
        assert action in possible_actions, "Invalid action"

        if game_end:
            break

        if (sum(action) == 0 or
            abs(action[0] + prev_action[0]) + abs(action[1] + prev_action[1]) == 0):
            action = prev_action
        else:
            prev_action = action

        new_seg = (snake[0][0] + action[0], snake[0][1] + action[1])
        screen[new_seg[1], new_seg[0]] = 1

        snake.insert(0, new_seg)
        if grow:
            grow = False
        else:
            screen[snake[-1][1], snake[-1][0]] = 0
            snake.pop()


def getFruit(screen, width, height):
    while True:
        rand_pt = [np.random.randint(1, width-1), np.random.randint(1, height-1)]
        fruit = Fruit(*rand_pt)
        if screen[fruit.y, fruit.x] < 1:
            return fruit
