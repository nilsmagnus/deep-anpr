import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization

import mygen

SHAPE = [200, 40]

# Building convolutional network
network = input_data(shape=[None, SHAPE[0], SHAPE[1], 1], name='input')
network = conv_2d(network, 64, 5, activation='relu')
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 64, 5, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 128, 5, activation='relu')
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 256, 5, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 256, 5, activation='relu')
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
#network = fully_connected(network, 16384, activation='tanh')
#network = dropout(network, 0.8)
network = fully_connected(network, 8184, activation='tanh')
network = dropout(network, 0.8)
network = fully_connected(network, 253, activation='softmax')

adam = tflearn.Adam(learning_rate=0.001, epsilon=0.1 )
network = regression(network, optimizer=adam, learning_rate=0.01,
                     loss='categorical_crossentropy', name='target')



# Training
model = tflearn.DNN(network, tensorboard_verbose=0)


for i in range(5):
    X, Y, testX, testY  = mygen.training_set_plates_only(100000)
    X = X.reshape([-1, SHAPE[0], SHAPE[1], 1])
    testX = testX.reshape([-1, SHAPE[0], SHAPE[1], 1])


    model.fit({'input': X}, {'target': Y}, n_epoch=10,
            validation_set=({'input': testX}, {'target': testY}),
               snapshot_step=10000, show_metric=True, run_id='convnet_anpr')

    name = "convnet_myanpr.tflearn."+ str(i)
    #model.save(name)