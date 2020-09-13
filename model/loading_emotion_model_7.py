from tensorflow import keras

def create_emotion_model_from_checkpoint():
    model = keras.models.load_model("/content/drive/My Drive/Emotion/resnetModel_128*128.h5")
    emotion_model = keras.Model(inputs = model.inputs, outputs=model.layers[-3].output)
    emotion_model.summary()

    return model

