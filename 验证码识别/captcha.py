import tensorflow as tf
import numpy as np
from PIL import Image
import re
import os


number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
            'v', 'w', 'x', 'y', 'z']
char_set = number + alphabet + ['_']  # 字符没满四个，用_代替
CHAR_SET_LEN = len(char_set)

# sess = tf.Session()


# 把文本转向量
def text2vec(text):
    # 总共4个字符
    vector = np.zeros(4*CHAR_SET_LEN)

    def char_pos(char):
        for i in range(len(char_set)):
            if char_set[i] == char:
                return i

    for i, c in enumerate(text):
        pos = char_pos(c) + int(i)*CHAR_SET_LEN
        vector[pos] = 1
    return vector


def get_batch(n=0, batch_size=128):
    x_batch = np.zeros([batch_size, 72*32])
    y_batch = np.zeros([batch_size, 4*CHAR_SET_LEN])
    name_list = os.listdir('.\\test_image')
    for i in range(n, batch_size):
        img = name_list[i]
        image = Image.open('.\\test_image\\'+img)
        image = image.resize((72, 32))
        reg = re.compile(r'\.jpg')
        text = re.sub(reg, '', img)
        image = np.array(image.convert('L'))
        x_batch[1, :] = image.flatten() / 255
        y_batch[1, :] = text2vec(text)
    return x_batch, y_batch


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)  # stddev 是返回的样本标准差
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)  # bias以一般取正值会比较好
    return tf.Variable(initial)


def conv2d(x, W):
    # strides = [1, x_movement, y_movement, 1]
    # Must let strides[0] = strides[3] = 1
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
    # padding有两种：valid和same，valid抽取的所有都在图片内，same抽取的边界处是在图片外的，same抽取出来的长和宽是不变的，valid是变小的（不需要pooling）


def max_pool_2x2(x):
    # ksize是指池化窗口大小，也就是[batch, height, weight, channels]因为我们不需要在batch和channels上做操作，所以设1即可
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


xs = tf.placeholder(tf.float32, [None, 72*32])
ys = tf.placeholder(tf.float32, [None, 4*CHAR_SET_LEN])
keep_prob = tf.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1, 72, 32, 1])


def create_cnn():
    # add conv2d-1 #
    W_conv1 = weight_variable([3, 3, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)  # 72*32*32
    h_pool1 = max_pool_2x2(h_conv1)  # 36*16*32

    # add conv2d-2 #
    W_conv2 = weight_variable([3, 3, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)  # 36*16*64
    h_pool2 = max_pool_2x2(h_conv2)  # 18*8*64

    # add conv2d-3 #
    W_conv3 = weight_variable([3, 3, 64, 64])
    b_conv3 = bias_variable([64])
    h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
    h_pool3 = max_pool_2x2(h_conv3)  # 9*4*64

    # func layer-1 #
    W_func1 = weight_variable([9 * 4 * 64, 1024])
    b_func1 = bias_variable([1024])
    h_pool2_flat = tf.reshape(h_pool3, [-1, 9 * 4 * 64])
    h_func1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_func1) + b_func1)
    h_func1_drop = tf.nn.dropout(h_func1, keep_prob)

    # output layer #
    W_func2 = weight_variable([1024, 4 * CHAR_SET_LEN])
    b_func2 = bias_variable([4 * CHAR_SET_LEN])
    prediction = tf.matmul(h_func1_drop, W_func2) + b_func2
    return prediction


def train():
    prediction = create_cnn()
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=prediction, labels=ys))
    # cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction), reduction_indices=[1]))

    train_step = tf.train.AdamOptimizer(0.001).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(tf.reshape(prediction, [-1, 4, CHAR_SET_LEN]), 2),
                                  tf.argmax(tf.reshape(ys, [-1, 4, CHAR_SET_LEN]), 2))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
        saver = tf.train.Saver()
        for i in range(1000):
            batch_xs, batch_ys = get_batch()
            sess.run(train_step, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 0.5})
            if i % 50 == 0:
                # batch_x_test, batch_y_test = get_batch(65)
                acc = sess.run(accuracy, feed_dict={xs: batch_xs, ys: batch_ys, keep_prob: 1.})
                print(acc)
                if acc >= 0.8:
                    saver.save(sess, 'captcha.model')
                    break


if __name__ == '__main__':
    train()
