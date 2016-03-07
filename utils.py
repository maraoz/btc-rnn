import os
import collections
import cPickle
import numpy as np
from shove import Shove


class DataLoader():
    def __init__(self, data_dir, batch_size, seq_length):
        self.data_dir = data_dir
        root = Shove('file://'+data_dir)
        self.batch_size = batch_size
        self.seq_length = seq_length

        tensor_file = os.path.join(data_dir, "data.npy")

        if not os.path.exists(tensor_file):
            print "reading text file"
            self.preprocess(root, tensor_file)
        else:
            print "loading preprocessed files"
            self.load_preprocessed(tensor_file)
        self.create_batches()
        self.reset_batch_pointer()

    def preprocess(self, root, tensor_file):
        dates = sorted(root.keys())
        prices = []
        print dates
        for date in dates:
          price = float(root[date].get('BAVERAGE-USD.24h Average') or 0)
          prices.append(price)
        print prices
        self.tensor = np.array(prices)
        np.save(tensor_file, self.tensor)

    def load_preprocessed(self, tensor_file):
        self.tensor = np.load(tensor_file)
        self.num_batches = self.tensor.size / (self.batch_size * self.seq_length)

    def create_batches(self):
        self.num_batches = self.tensor.size / (self.batch_size * self.seq_length)
        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.tensor
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)


    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def reset_batch_pointer(self):
        self.pointer = 0

