from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
import pickle
from io import __all__

def main():
    mnist = input_data.read_data_sets("MNIsT_data/", one_hot=True)

    file_path = open('D:\mnist_data.pickle', 'wb')
    pickle.dump(mnist, file_path)
    file_path.close()

main()