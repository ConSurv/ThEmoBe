from model.load_behaviour_model_from_checkpoint_2 import *
from CVND_Exercises_2_2_YOLO.get_cropped_human_frames import *
from model.get_behaviour_features_6 import *
from model.loading_emotion_model_7 import *
from model.face_detector_8 import *
# from model.create_gsom_object_10 import *
from Parallel_GSOM_for_HAAP.create_gsom_objects import *
from model.bounding_box_11 import *


behaviour_model = create_behaviour_model_from_checkpoint()

emotion_model = create_emotion_model_from_checkpoint()



def annotateVideo(APP_ROOT, video_path, emo_annotation,behav_annotation,threat_annotation, video_id):

    frames_list = convert_to_frames(video_path)

    cropped_image_sequence_for_behaviour, coordinates_array, cropped_image_sequence_for_emotion = get_cropped_frames(frames_list)

    behaviour_features = get_behaviour_features(behaviour_model, cropped_image_sequence_for_behaviour)

    detected_face = detect_face(cropped_image_sequence_for_emotion)

    emotion_features = get_emotion_features(emotion_model, detected_face)

    behaviour_predicted, behaviour_winner_weights = BehaviourGSOM.predict_x(behaviour_features[[0], :])

    emotion_predicted, emotion_winner_weights = EmotionGSOM.predict_x(emotion_features[[0], :])

    ALPHA1, ALPHA2 = 1, 1

    threat_feature = np.hstack((ALPHA1 * emotion_winner_weights[0][0], ALPHA2 * behaviour_winner_weights[0][0]))

    threat_feature = threat_feature.reshape(1, 9216)

    threat_predicted, threat_winner_weights = ThreatGSOM.predict_x(threat_feature)

    predictions = [str(int(emotion_predicted[0])), str(int(behaviour_predicted[0])), str(int(threat_predicted[0]))]

    print(predictions)

    what_to_plot = [emo_annotation,behav_annotation,threat_annotation]

    plot_and_save_bounding_boxes(APP_ROOT, predictions, frames_list, coordinates_array, video_id, what_to_plot)

    return "Video annotated successfully!"


