#   1.导入库
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from tensorflow.keras import models, layers

"""#   2.加载mnist数据集
(x_train,y_train),(x_test,y_test)=tf.keras.datasets.mnist.load_data()
x_train,x_test=x_train/255.0,x_test/255.0   #预处理

#   3.构建神经网络
model=models.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),  #第一层    展平层
    keras.layers.Dense(128,activation='relu'),  #第二层    隐藏层
    keras.layers.Dense(256,activation='relu'),
    keras.layers.Dropout(0.2),  #第三层    dropout层
    keras.layers.Dense(10,activation='softmax') #第四层    输出层
])
#   打印表格信息
model.summary()

#   4.编译模型
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#   5.训练模型
history=model.fit(x_train,y_train,epochs=5)

#   6.评估模型性能
test_loss,test_acc=model.evaluate(x_test,y_test,verbose=2)

#   7.模型预测
predictions=model.predict(x_test[0:5])
for i in range(5):
    predicted_label=tf.argmax(predictions[i]).numpy()
    print(f"第 {i + 1} 张图片的预测结果是: {predicted_label}, 真实结果是: {y_test[i]}")  # 补充打印输出


class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

plt.figure(figsize=(10, 5))
for i in range(5):
    plt.subplot(1, 5, i + 1)
    plt.imshow(x_train[i], cmap=plt.cm.binary)
    plt.title(f"Label: {class_names[y_train[i]]}")
    plt.axis('off')
plt.show()

"""


"""#   1.加载数据集 预处理
(x_train,y_train),(x_test,y_test)=tf.keras.datasets.fashion_mnist.load_data()
x_train=x_train.reshape(-1,28,28,1).astype('float32')/255.0
x_test=x_test.reshape(-1,28,28,1).astype('float32')/255.0

#   2.构建神经网络
model=models.Sequential([
    layers.Conv2D(32, kernel_size=(5, 5), activation='relu',input_shape=(28,28,1)),
    layers.MaxPooling2D(pool_size=(2,2)),

    layers.Conv2D(64,kernel_size=(5, 5),activation='relu'),
    layers.MaxPooling2D(pool_size=(2,2)),

    layers.Conv2D(128,kernel_size=(4, 4),activation='relu'),

    layers.Flatten(),
    layers.Dropout(0.2),

    layers.Dense(128, activation='relu'),
    layers.Dense(10,activation='softmax')
])
#   3.展示
model.summary()

#   4.编译模型
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#   5.训练模型
history = model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

#   6.评估模型性能
test_loss,test_acc=model.evaluate(x_test,y_test,verbose=2)

# 7.预测
predictions=model.predict(x_test[0:5])
for i in range(5):
    predicted_label=tf.argmax(predictions[i]).numpy()
    print(f"第 {i + 1} 张图片的预测结果是: {predicted_label}, 真实结果是: {y_test[i]}")  # 补充打印输出"""



"""#   1.加载数据集 预处理
(x_train,y_train),(x_test,y_test)=tf.keras.datasets.fashion_mnist.load_data()
x_train=x_train.reshape(-1,28*28).astype('float32')/255.0
x_test=x_test.reshape(-1,28*28).astype('float32')/255.0

#   2.构建神经网络
model=models.Sequential([
    layers.Input(shape=(28*28,)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')

])
#   3.展示
model.summary()

#   4.编译模型
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#   5.训练模型
history = model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

#   6.评估模型性能
test_loss,test_acc=model.evaluate(x_test,y_test,verbose=2)

# 7.预测
predictions=model.predict(x_test[0:5])
for i in range(5):
    predicted_label=tf.argmax(predictions[i]).numpy()
    print(f"第 {i + 1} 张图片的预测结果是: {predicted_label}, 真实结果是: {y_test[i]}")  # 补充打印输出"""


"""from tensorflow.keras.datasets import boston_housing
#   1.加载数据集 预处理
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.boston_housing.load_data()

mean = x_train.mean(axis=0)
std = x_train.std(axis=0)
x_train = (x_train - mean) / std
x_test = (x_test - mean) / std

#   2.构建神经网络
model=models.Sequential([
    layers.Input(shape=(13,)),
    layers.Dense(65, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(1)
])
#   3.展示
model.summary()

#   4.编译模型
model.compile(optimizer='adam',loss='mse',metrics=['mae'])

#   5.训练模型
history = model.fit(
    x_train, y_train,
    epochs=5,
    validation_split=0.2
)

#   6.评估模型性能
test_loss,test_mae=model.evaluate(x_test,y_test,verbose=2)


#   7.预测
predictions=model.predict(x_test[0:5])
for i in range(5):
    print(f"第 {i + 1} 个样本 -> 预测房价: ${predictions[i][0]:.2f}k, 真实房价: ${y_test[i]:.2f}k")"""


import tensorflow as tf
from tensorflow.keras import datasets,layers,models
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os


#   1.加载    预处理
cifar_path=r"D:\yy\cifar-10\cifar-10-batches-py"
(train_images,train_labels),(test_images,test_labels)=datasets.cifar10.load_data(path=cifar_path)

train_images,test_images=train_images/255.0,test_images/255.0

class_names=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

#   2.搭建网络
model=models.Sequential([
    layers.Conv2D(32, kernel_size=(5, 5), activation='relu',input_shape=(32,32,3)),
    layers.MaxPooling2D(pool_size=(2,2)),

    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2,2)),

    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),

    layers.Flatten(),

    layers.Dense(64, activation='relu'),
    layers.Dense(10,activation='softmax')
])
model.summary()

#   3.编译模型
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#   4.训练模型
model.fit(train_images,train_labels,epochs=5,validation_data=(test_images,test_labels))

#   5.模型评估
test_loss,test_acc=model.evaluate(test_images,test_labels,verbose=2)





import tensorflow as tf
from tensorflow.keras import datasets,layers,models
import matplotlib.pyplot as plt
import numpy as np


#   1.加载    预处理
(train_images,train_labels),(test_images,test_labels)=datasets.cifar10.load_data()

train_images,test_images=train_images/255.0,test_images/255.0

#   2.搭建网络
model=models.Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu',input_shape=(32,32,3)),
    layers.MaxPooling2D(pool_size=(2,2)),

    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2,2)),

    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),

    layers.Flatten(),

    layers.Dense(64, activation='relu'),
    layers.Dense(10,activation='softmax')
])
model.summary()

#   3.编译模型
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#   4.训练模型
model.fit(train_images,train_labels,epochs=15,validation_data=(test_images,test_labels))

#   5.模型评估
test_loss,test_acc=model.evaluate(test_images,test_labels,verbose=2)
print(f"\n测试集准确率: {test_acc:.4f}")







import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, layers
import numpy as np

"""#   1.加载mnist数据集
(x_train,y_train),(x_test,y_test)=tf.keras.datasets.mnist.load_data()
x_train,x_test=x_train/255.0,x_test/255.0   #预处理

#   2.构建神经网络
model=models.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),  #第一层    展平层
    keras.layers.Dense(128,activation='relu'),  #第二层    隐藏层
    keras.layers.Dense(256,activation='relu'),
    keras.layers.Dropout(0.2),  #第三层    dropout层
    keras.layers.Dense(10,activation='softmax') #第四层    输出层
])
#   打印表格信息
model.summary()

#   3.编译模型
model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

#   4.训练模型
history=model.fit(x_train,y_train,epochs=10)

#   5.评估模型性能
test_loss,test_acc=model.evaluate(x_test,y_test,verbose=2)

#   6.模型保存
model.save('mnist_model.h5')"""

#   7.模型预测
model = tf.keras.models.load_model('mnist_model.h5')
image_path = r"C:\Users\yyx\Desktop\1_8\8.jpg"
ima=tf.io.read_file(image_path)
ima=tf.image.decode_image(ima,channels=1)
ima=tf.image.resize(ima,(28,28))
ima = tf.cast(ima, tf.float32) / 255.0
ima = 1.0 - ima
ima_input = tf.expand_dims(ima, axis=0)
prediction = model.predict(ima_input)
print("模型预测这个数字是:", np.argmax(prediction))

