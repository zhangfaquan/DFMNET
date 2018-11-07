import pickle
import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import animation

import numpy as np 


class SWSVisualizer():
    def __init__(self, tag:str):
        self.tag = tag
        self.loadResults(self.tag)

    def loadResults(self, tag:str):
        save_path = os.path.join(
            'pre_train_model',
            'dfmnet_for_vis',
            tag + '_sensor_test_result.pick'
        )

        with open(save_path, 'rb') as f:
            results = pickle.load(f)

        self.predictions = results['predictions']
        self.MSEs = results['MSEs'] 

        self.test_y = results['test_y']

        self.MSEs = np.vstack(self.MSEs).T
        self.index = np.arange(0, 20)  + 1
        self.n_frame = 1000
        self.initDraw()

    def initDraw(self):
        self.fig = plt.figure()
        gs = gridspec.GridSpec(1, 2)
        ax1 = self.fig.add_subplot(gs[0, 1])
        self.barchart = ax1.bar(self.index, self.MSEs[0, :])
        ax1.grid()
        ax1.set_ylabel("Effect")
        ax1.set_xlabel("Sensor ID")
        ax1.set_ylim([0, 0.5])

    def update(self, num):
        mses = self.MSEs[num, :]
        mses = mses / np.sum(mses)
        for idx, chart in enumerate(self.barchart):
            chart.set_height(mses[idx])
  
    def show(self):
        ani = animation.FuncAnimation(self.fig, self.update, self.n_frame, interval=20, blit=False)
        plt.show()

if __name__ == '__main__':
    vis = SWSVisualizer('SQ')
    vis.show()