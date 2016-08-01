import os
import itertools as it
from matplotlib import pyplot as plt
from matplotlib import colors


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
        plt.savefig('%s/%05i.png' % (folder, frame_cnt.next()))


def save_model(model, name, folder='models'):
    if folder not in os.listdir('.'):
        os.mkdir(folder)
    model.save_weights('%s/%s.h5' % (folder, name))
