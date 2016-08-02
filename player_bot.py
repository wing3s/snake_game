from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution2D
from keras.layers.core import Dense, Flatten
from keras.optimizers import SGD, RMSprop
import time
import numpy as np
from random import sample as rsample
import itertools as it
from snake_game import snake_game
from helper import save_image, save_model

GAME_WIDTH = 10
GAME_HEIGHT = 10
NB_FRAMES = 4  # Number of frames (i.e., screens) the agent remembers
POSSIBLE_ACTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1), (0, 0))


def init_model():
    # Recipe of deep reinforcement learning model
    model = Sequential()
    model.add(Convolution2D(16, nb_row=3, nb_col=3, activation='relu', input_shape=(NB_FRAMES, GAME_HEIGHT, GAME_WIDTH)))
    model.add(Convolution2D(32, nb_row=3, nb_col=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(len(POSSIBLE_ACTIONS)))
    model.compile(RMSprop(), 'MSE')
    return model


def experience_replay(batch_size):
    memory = []
    while True:
        exp = yield rsample(memory, batch_size) if batch_size <= len(memory) else None
        memory.append(exp)


def train_model(model, nb_epochs=1000):
    start_time = time.time()
    batch_size = 64
    epsilon = 1.  # Probability to explore, 0 ~ 1.
    gamma = .8

    exp_replay = experience_replay(batch_size)
    exp_replay.next()

    for i in xrange(nb_epochs):
        game = snake_game(width=GAME_WIDTH, height=GAME_HEIGHT)
        screen, _ = game.next()
        state = np.asarray([screen]*NB_FRAMES)

        if epsilon > .1:
            # fine tune epsilon
            epsilon -= .9 / (nb_epochs / 1.5)
        loss = .0

        try:
            while True:
                act_idx = np.random.randint(len(POSSIBLE_ACTIONS))
                if np.random.random() > epsilon:
                    # use prediction
                    act_idx = np.argmax(model.predict(state[np.newaxis]), axis=-1)[0]
                else:
                    # explore
                    act_idx = np.random.randint(len(POSSIBLE_ACTIONS))
                action = POSSIBLE_ACTIONS[act_idx]

                screen, reward = game.send(action)
                state_prime = np.roll(state, 1)
                state_prime[0] = screen
                exp = (state, action, reward, state_prime)
                state = state_prime

                batch = exp_replay.send(exp)
                if batch:
                    inputs = []
                    targets = []
                    for state, action, reward, state_prime in batch:
                        q_vals = model.predict(state[np.newaxis]).flatten()
                        act_idx = POSSIBLE_ACTIONS.index(action)
                        if reward < 0:
                            q_vals[act_idx] = reward
                        else:
                            q_vals[act_idx] = reward + gamma * model.predict(state_prime[np.newaxis]).max(axis=-1)
                        inputs.append(state)
                        targets.append(q_vals)
                    this_loss = model.train_on_batch(np.array(inputs), np.array(targets))
                    loss += this_loss
        except StopIteration:
            pass

        if (i+1) % 10 == 0:
            print 'Epoch %6i/%i, loss: %.6f, epsilon: %.3f' % (i+1, nb_epochs, loss, epsilon)
    time_spent = time.time() - start_time
    mins, secs = divmod(time_spent, 60)
    hours, mins = divmod(mins, 60)
    print "Training completed, %d:%02d:%02d" % (hours, mins, secs)
    return model


def play_game(model):
    img_saver = save_image()
    img_saver.next()

    game_cnt = it.count(1)
    for i in xrange(10):
        game = snake_game(width=GAME_WIDTH, height=GAME_HEIGHT)
        screen, _ = game.next()
        img_saver.send(screen)
        frame_cnt = it.count()
        try:
            state = np.asarray([screen] * NB_FRAMES)
            while True:
                frame_cnt.next()
                act_idx = np.argmax(model.predict(state[np.newaxis]), axis=-1)[0]
                screen, _ = game.send(POSSIBLE_ACTIONS[act_idx])
                state = np.roll(state, 1)
                state[0] = screen
                img_saver.send(screen)
        except StopIteration:
            print 'Saved %4i frames for game %3i' % (frame_cnt.next(), game_cnt.next())
    img_saver.close()


def main():
    model = init_model()
    trained_model = train_model(model, nb_epochs=1000)
    save_model(trained_model, name='snake')
    play_game(trained_model)


if __name__ == '__main__':
    main()
