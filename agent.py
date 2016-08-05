import time
import numpy as np


def experience_replay(batch_size):
    memory = []
    while True:
        exp = yield memory
        memory.append(exp)

        
def save_image(folder='images'):
    if folder not in os.listdir('.'):
        os.mkdir(folder)
    frame_cnt = it.count()

    # Nokia screen color style
    cmap = colors.ListedColormap(['#98C302', '#353C6A', '#425A02'])
    bounds = [0, 0.25, 0.75, 1]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    while True:
        screen = (yield)
        shape = screen.shape
        plt.imshow(
            screen,
            interpolation='none',
            cmap=cmap,
            norm=norm,
            aspect='equal',
            extent=(0, shape[1], 0, shape[0]))
        plt.grid(True)
        plt.axis('off')
        plt.savefig('%s/frame%05i.png' % (folder, frame_cnt.next()))

        
class Agent:
    def __init__(self, model, nb_frames, game, size):
        self.model = model
        self.nb_frames = nb_frames
        self.game = game
        self.width, self.height = size
    
    def train(self, game, size, nb_epochs, batch_size, gamma, save_model):
        exp_replay = experience_replay(batch_size)
        exp_replay.next()
        for i in xrange(nb_epochs):
            start_time = time.time()
            game = self.game(width=self.width, height=self.height)
            screen, _ = game.next()
            state = np.asarray([screen]*NB_FRAMES)

            if epsilon > .1:
                # fine tune epsilon
                epsilon -= .9 / (nb_epochs / 2)
            loss = .0

            try:
                while True:
                    if np.random.random() > epsilon:
                        # use prediction
                        act_idx = np.argmax(self.model.predict(state[np.newaxis]), axis=-1)[0]
                    else:
                        # explore
                        act_idx = np.random.randint(len(POSSIBLE_ACTIONS))
                    action = POSSIBLE_ACTIONS[act_idx]

                    screen, reward = game.send(action)
                    state_prime = np.roll(state, 1, axis=0)
                    state_prime[0] = screen
                    exp = (state, action, reward, state_prime)
                    state = state_prime

                    batch = exp_replay.send(exp)
                    if batch:
                        inputs = []
                        targets = []
                        for s, a, r, s_prime in batch:
                            q_vals = self.model.predict(s[np.newaxis]).flatten()
                            a_idx = POSSIBLE_ACTIONS.index(a)
                            if r < 0:
                                q_vals[a_idx] = r
                            else:
                                q_vals[a_idx] = r + gamma * self.model.predict(s_prime[np.newaxis]).max(axis=-1)
                            inputs.append(s)
                            targets.append(q_vals)
                        loss += self.model.train_on_batch(np.array(inputs), np.array(targets))
            except StopIteration:
                pass
            time_spent = time.time() - start_time

            if (i+1) % 10 == 0:
                print 'Epoch %6i/%i, loss: %.6f, epsilon: %.3f [%is]' % (i+1, nb_epochs, loss, epsilon, int(time_spent))
 
        if save_model:
            if folder not in os.listdir('.'):
                os.mkdir(folder)
            model_name = 'model_%iw_%ih_%iepochs_%ibatch_%.2fgamma' % (self.width, self.height, nb_epochs, batch_size, gamma)
            self.model.save_weights('%s/%s.h5' % (folder, model_name), overwrite=True)

    def play(self):
        img_saver = save_image()
        img_saver.next()

        game_cnt = it.count(1)
        for i in xrange(10):
            game = self.game(width=self.width, height=self.height)
            screen, _ = game.next()
            img_saver.send(screen)
            frame_cnt = it.count()
            try:
                state = np.asarray([screen] * NB_FRAMES)
                while True:
                    frame_cnt.next()
                    act_idx = np.argmax(self.model.predict(state[np.newaxis]), axis=-1)[0]
                    screen, _ = game.send(POSSIBLE_ACTIONS[act_idx])
                    state = np.roll(state, 1, axis=0)
                    state[0] = screen
                    img_saver.send(screen)
            except StopIteration:
                print 'Saved %4i frames for game %3i' % (frame_cnt.next(), game_cnt.next())
        img_saver.close()
