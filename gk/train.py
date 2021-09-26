#1.Import library
import cv2
import keras.applications.mobilenet
from keras.applications.mobilenet import MobileNet
from keras.layers import GlobalAveragePooling2D,Dense,Dropout,Flatten
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import  keras
from keras.callbacks import ModelCheckpoint
#2.Định nghĩa tham số
n_class = 2
#3.Build model
def get_model():
    #Tạo base model
    
    base_model = MobileNet(include_top = False,weights = 'imagenet',input_shape=(224,224,3))

    #Tao model chinh
    x = base_model.output
    # Add some new Fully connected layers to
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    x = Dropout(0.25)(x)
    x = Dense(1024,activation='relu')(x)
    x = Dropout(0.25)(x)
    x = Dense(512, activation='relu')(x)

    outs = Dense(n_class,activation='softmax')(x)
    #Dong bang model

    for layer in base_model.layers:
        layer.trainable = False

    model = Model(inputs = base_model.inputs,outputs= outs)
    return model
model = get_model()

#3.Make model
data_folder = 'cats_and_dogs_filtered'

train_datagen = ImageDataGenerator(preprocessing_function=keras.applications.mobilenet.preprocess_input,rotation_range=0.2,
                                   width_shift_range=0.2, height_shift_range=0.2, shear_range=0.3,zoom_range=0.5,
                                   horizontal_flip=True,vertical_flip=True,validation_split=0.2)

train_generator  = train_datagen.flow_from_directory(data_folder,target_size=(224,224),
                                                     batch_size=64,
                                                     class_mode='categorical',
                                                     subset='training')
validation_generator = train_datagen.flow_from_directory(data_folder,target_size=(224,224),
                                                     batch_size=64,
                                                     class_mode='categorical',
                                                     subset='validation')

classes = train_generator.class_indices
print(classes)
classes = list(classes.keys())

#4.Train model
n_epochs = 10
batch_size = 64

model.compile(optimizer='sgd',loss='categorical_crossentropy',metrics=['accuracy'])
checkpoint = ModelCheckpoint('models/best.hdf5',monitor='val_loss',save_best_only=True,mode='auto')

callback_list = [checkpoint]

step_train  = train_generator.n//batch_size
step_val = validation_generator.n//batch_size

model.fit_generator(generator=train_generator,steps_per_epoch=step_train,
                    validation_data = validation_generator,validation_steps=step_val,
                    callbacks = callback_list,
                    epochs=n_epochs)
#Lưu lại model
model.save('models/model.h5')
