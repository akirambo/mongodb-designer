
import sys
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn import datasets
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

np.random.seed(0)
tf.set_random_seed(1234)

class CNN(object):
    def __init__(self, n_in, n_hiddens, n_out):
        # initialize
        self.n_in = n_in
        self.n_hiddens = n_hiddens
        self.n_out = n_out
        self.weights = []
        self.biases = []

        self._x = None
        self._t = None
        self._keep_prob = None
        self._sess = None
        self._history = {
            'accuracy': [],
            'loss': [],
            'test_loss': [],
            'test_accuracy' :[]
        }
        
    def weight_variable(self, shape):
        initial = tf.truncated_normal(shape, stddev=0.01)
        return tf.Variable(initial)

    def bias_variable(self, shape):
        initial = tf.zeros(shape)
        return tf.Variable(initial)

    def inference(self, x, keep_prob):
        # Model Definition
        for i, n_hidden in enumerate(self.n_hiddens):
            if i == 0:
                input = x
                input_dim = self.n_in
            else:
                input = output
                input_dim = self.n_hiddens[i-1]
                
            self.weights.append(self.weight_variable([input_dim, n_hidden]))
            self.biases.append(self.bias_variable([n_hidden]))
            h = tf.nn.relu(tf.matmul(
                input, self.weights[-1]) + self.biases[-1])
            output = tf.nn.dropout(h, keep_prob)
                        
        self.weights.append(
            self.weight_variable([self.n_hiddens[-1], self.n_out]))
        self.biases.append(self.bias_variable([self.n_out]))
        y = tf.nn.softmax(tf.matmul(
            output, self.weights[-1]) + self.biases[-1])
        return y
    
    def loss(self, y, t):
        # Loss Function Description
        cross_entropy = tf.reduce_mean(-tf.reduce_sum(t * tf.log(tf.clip_by_value(y, 1e-10, 1.0)),
                                                      reduction_indices=[1]))
        return cross_entropy

    def training(self, loss):
        # Training
        optimizer = tf.train.GradientDescentOptimizer(0.01)
        train_step = optimizer.minimize(loss)
        return train_step

    def accuracy(self, y, t):
        correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(t, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        return accuracy

    def fit(self, X_train, Y_train, X_test, Y_test,
            nb_epoch=100, batch_size=100, p_keep=0.5,
            verbose=1):
        x = tf.placeholder(tf.float32, shape=[None, self.n_in])
        t = tf.placeholder(tf.float32, shape=[None, self.n_out])
        keep_prob = tf.placeholder(tf.float32)
        self._x = x
        self._t = t
        self._keep_prob = keep_prob

        y = self.inference(x, keep_prob)
        loss = self.loss(y, t)
        train_step = self.training(loss)
        accuracy = self.accuracy(y, t)
        # Start & Init Variables
        sess = tf.Session()
        sess.run( tf.global_variables_initializer())
        
        self._sess = sess
        
        N_train = len(X_train)
        n_batches = N_train // batch_size
        for epoch in range(nb_epoch):
            X_, Y_ = shuffle(X_train, Y_train)
            for i in range(n_batches):
                start = i * batch_size
                end = start + batch_size

                sess.run(train_step, feed_dict={
                    x: X_[start:end],
                    t: Y_[start:end],
                    keep_prob: p_keep
                    })

            loss_ = loss.eval(session=sess, feed_dict={
                x: X_train,
                t: Y_train,
                keep_prob : 1.0
            })
            accuracy_ = accuracy.eval(session=sess, feed_dict={
                x: X_train,
                t: Y_train,
                keep_prob : 1.0
            })
            test_loss_ = loss.eval(session=sess, feed_dict={
                x: X_test,
                t: Y_test,
                keep_prob : 1.0
            })
            test_accuracy_ = accuracy.eval(session=sess, feed_dict={
                x: X_test,
                t: Y_test,
                keep_prob : 1.0
            })
            # Save Values
            self._history['loss'].append(loss_)
            self._history['accuracy'].append(accuracy_)
            self._history['test_loss'].append(test_loss_)
            self._history['test_accuracy'].append(test_accuracy_)

            if verbose:
                print('epoch:', epoch,
                      ',loss:', loss_,
                      ',accuracy:', accuracy_,
                      ',test_loss:', test_loss_,
                      ',test_accuracy:', test_accuracy_)
        return self._history
        
    def evaluate(self, X_test, Y_test):
        return self.accuracy.eval(session=self._sess, feed_dict={
            self._x: X_test,
            self._t: Y_test,
            self._keep_prob: 1.0
        })


def visual(np_epoch,history):
    plt.rc("font", family="serif")
    fig = plt.figure()
    plt.plot(range(nb_epoch), history["accuracy"], label="acc", color="blue")
    plt.plot(range(nb_epoch), history["test_accuracy"], label="test_acc", color="red")
    plt.xlabel("epochs")
    plt.ylabel("accuracy")
    plt.ylim([0,1])
    plt.show()

    
if __name__ == "__main__":
    print("[USAGE] python ml_mongo_model_lite.py FILENAME LABELSIZE")
    args = sys.argv
    data = pd.read_csv(args[1]).values
    n = len(data)
    N = 10000
    indices = np.random.permutation(range(n))[:N]
    pos = int(args[2]) * -1
    X = data[:,:pos]
    Y = data[:,pos:]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7)
    model = CNN(n_in=len(X[0]),
                n_hiddens=[25,10],
                n_out=len(Y[0]))
    nb_epoch=100
    print(X_train)
    print(Y_train)
    history = model.fit(X_train, Y_train,
                        X_test, Y_test,
                        nb_epoch,
                        batch_size=100,
                        p_keep=0.5)
    visual(nb_epoch, history)

    
