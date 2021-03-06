from tensorflow import keras

def create_emotion_model_from_checkpoint():
    model = keras.models.load_model("/root/FYP_Model_weights/resnetModel_128_128.h5")
    emotion_model = keras.Model(inputs = model.inputs, outputs=model.layers[-3].output)
    # emotion_model.summary()

    return emotion_model

if __name__ == '__main__':
    create_emotion_model_from_checkpoint()