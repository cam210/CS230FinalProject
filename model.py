import tensorflow as tf
from tensorflow.keras import layers, models

def inception_module(x, filters):
    # Branch 1
    branch_1 = layers.Conv3D(filters[0], kernel_size=(1, 1, 1), padding='same', activation='relu')(x)

    # Branch 2
    branch_2 = layers.Conv3D(filters[1], kernel_size=(1, 1, 1), padding='same', activation='relu')(x)
    branch_2 = layers.Conv3D(filters[2], kernel_size=(3, 3, 3), padding='same', activation='relu')(branch_2)

    # Branch 3
    branch_3 = layers.Conv3D(filters[3], kernel_size=(1, 1, 1), padding='same', activation='relu')(x)
    branch_3 = layers.Conv3D(filters[4], kernel_size=(5, 5, 5), padding='same', activation='relu')(branch_3)

    # Branch 4 (Pooling branch)
    branch_4 = layers.MaxPooling3D(pool_size=(3, 3, 3), strides=(1, 1, 1), padding='same')(x)
    branch_4 = layers.Conv3D(filters[5], kernel_size=(1, 1, 1), padding='same', activation='relu')(branch_4)

    # Concatenate all branches
    x = layers.concatenate([branch_1, branch_2, branch_3, branch_4], axis=-1)
    return x

def I3D_model(input_shape=(16, 64, 64, 3), num_classes=2):
    inputs = layers.Input(shape=input_shape)

    x = layers.Conv3D(64, kernel_size=(7, 7, 7), strides=(2, 2, 2), padding='same', activation='relu')(inputs)
    x = layers.MaxPooling3D(pool_size=(1, 3, 3), strides=(1, 2, 2), padding='same')(x)


    x = layers.Conv3D(64, kernel_size=(1, 1, 1), padding='same', activation='relu')(x)
    x = layers.Conv3D(192, kernel_size=(3, 3, 3), padding='same', activation='relu')(x)
    x = layers.MaxPooling3D(pool_size=(1, 3, 3), strides=(1, 2, 2), padding='same')(x)

    x = inception_module(x, [64, 96, 128, 16, 32, 32])
    x = inception_module(x, [128, 128, 192, 32, 96, 64])
    x = layers.MaxPooling3D(pool_size=(3, 3, 3), strides=(2, 2, 2), padding='same')(x)

    x = inception_module(x, [192, 96, 208, 16, 48, 64])
    x = inception_module(x, [160, 112, 224, 24, 64, 64])
    x = inception_module(x, [128, 128, 256, 24, 64, 64])
    x = inception_module(x, [112, 144, 288, 32, 64, 64])
    x = inception_module(x, [256, 160, 320, 32, 128, 128])
    x = layers.MaxPooling3D(pool_size=(2, 2, 2), strides=(2, 2, 2), padding='same')(x)

    x = inception_module(x, [256, 160, 320, 32, 128, 128])
    x = inception_module(x, [384, 192, 384, 48, 128, 128])

    x = layers.GlobalAveragePooling3D()(x)
    x = layers.Dropout(0.4)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)

    # Create the model
    model = models.Model(inputs, outputs)
    return model

# Instantiate and compile the model
input_shape = (16, 64, 64, 3)  
num_classes = 2
model = I3D_model(input_shape=input_shape, num_classes=num_classes)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()