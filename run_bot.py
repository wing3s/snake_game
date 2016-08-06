from keras.models import Sequential
from keras.layers.convolutional import Convolution2D
from keras.layers.core import Dense, Flatten
from keras.optimizers import RMSprop

from snake_game import snake_game
from agent import Agent


def main():
    game_width = 12
    game_height = 9
    nb_frames = 4
    actions = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))

    # Recipe of deep reinforcement learning model
    model = Sequential()
    model.add(Convolution2D(
        16,
        nb_row=3,
        nb_col=3,
        activation='relu',
        input_shape=(nb_frames, game_height, game_width)))
    model.add(Convolution2D(32, nb_row=3, nb_col=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(len(actions)))
    model.compile(RMSprop(), 'MSE')

    agent = Agent(
        model, nb_frames, snake_game, actions, size=(game_width, game_height))
    agent.train(nb_epochs=10000, batch_size=64, gamma=0.8, save_model=True)
    agent.play(nb_rounds=10)


if __name__ == '__main__':
    main()
