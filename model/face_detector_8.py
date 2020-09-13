def cropFaceDNN(cropped_behaviour_img):
    prototxt = "/content/deep-learning-face-detection/deploy.prototxt.txt"
    model = "/content/deep-learning-face-detection/res10_300x300_ssd_iter_140000.caffemodel"
    CONFIDENCE = 0.5

    # load our serialized model from disk
    net = cv2.dnn.readNetFromCaffe(prototxt, model)

    # load the input image and construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    image = cropped_behaviour_img
    clone = image.copy()

    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    face_detected = False
    face = np.zeros((128, 128, 3))

    if (detections.shape[2]):
        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > CONFIDENCE:
                # compute the (x, y)-coordinates of the bounding box for the
                # object

                face_detected = True

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the bounding box of the face
                # cv2.rectangle(image, (startX, startY), (endX, endY),(0, 0, 255), 2)
                face = clone[startY:endY, startX:endX]

    else:
        face_detected = False

    return face_detected, face


import os

def detect_face(cropped_image_sequence_for_emotion):
    black = np.zeros((128, 128, 3))
    difficult_sequences = []

    face_detected = False
    for cropped_image in cropped_image_sequence_for_emotion:

        face_detected, face = cropFaceDNN(cropped_image)
        if face_detected:
            try:
                imageresize = cv2.resize(face, (128, 128), interpolation=cv2.INTER_AREA)
                detected_face = cv2.cvtColor(imageresize, cv2.COLOR_BGR2GRAY)
                detected_face = np.repeat(detected_face[..., np.newaxis], 3, -1)
                break
            except:
                print("No img ")

    if face_detected == False:
        detected_face = black

    return detected_face

def get_emotion_features(emotion_model,detected_face):
    print(detected_face.shape)
    emotion_features = emotion_model.predict(detected_face.reshape(1,128,128,3))
    print(emotion_features.shape)