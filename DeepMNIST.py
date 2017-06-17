# Load data
import pickle
file_path = open('mnist_data.pickle', 'rb')
mnist = pickle.load(file_path)
file_path.close()

#
import tensorflow as tf
sess = tf.InteractiveSession()

# Input & output data
x = tf.placeholder(tf.float32, shape=[None, 784])
y_real = tf.placeholder(tf.float32, shape=[None, 10])

# Weight matrix
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

# Predicted results
y = tf.matmul(x, W) + b
sess.run(tf.global_variables_initializer())

# Evaluate loss
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_real, logits=y))

# Train
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

for i in range(1000):
    batch = mnist.train.next_batch(100)
    train_step.run(feed_dict={x: batch[0], y_real: batch[1]})

# Evaluate
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_real, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_real: mnist.test.labels}))
