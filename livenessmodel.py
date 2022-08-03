
import numpy as np
import tensorflow as tf
from keras.applications import mobilenet_v2
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Input, Flatten, SeparableConv2D
from keras.layers import GlobalAveragePooling2D, BatchNormalization, Concatenate
from keras.models import Sequential, Model
def get_liveness_model():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(2))
    return model


def get_liveness_model_soft_max():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dense(2, activation='softmax'))
    return model



def get_liveness_model_MobileNetV2():
    img_width=224
    img_height=224
    # Don't forget to turn on the Internet to download the respective pre-trained weights!
    pretrain_net = mobilenet_v2.MobileNetV2(input_shape=(img_width, img_height, 3),
                                            include_top=False,
                                            weights='imagenet')



    # load_param_path = '../input/mobilenet_v2/xception_weights_tf_dim_ordering_tf_kernels_notop.h5'  # Offline alternative
    # pretrain_net.load_weights(load_param_path)  # Manually load the weights from the input directory

    # ------ Freezing layer(s) up to a specific layer ------
    freeze_before = None  # "block_16_expand"  # use None to train, use "all" to freeze all the layers

    if freeze_before:
        for layer in pretrain_net.layers:
            if layer.name == freeze_before:
                break
            else:
                layer.trainable = False

    x = pretrain_net.output
    x = Conv2D(32, (3, 3), activation='relu')(x)
    x = Dropout(rate=0.2, name='extra_dropout1')(x)
    x = GlobalAveragePooling2D()(x)
    # x = Dense(units=128, activation='relu', name='extra_fc1')(x)
    # x = Dropout(rate=0.2, name='extra_dropout1')(x)
    x = Dense(1, activation='sigmoid', name='classifier')(x)

    model = Model(inputs=pretrain_net.input, outputs=x, name='mobilenetv2_spoof')
    return  model