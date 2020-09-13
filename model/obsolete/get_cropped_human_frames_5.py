import re
import glob
import numpy as np
import matplotlib.pyplot as plt
import cv2
import torchvision.transforms as transforms
from PIL import Image




def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


video_name = 'scream05'
directory = '/content/drive/My Drive/Behavior_Data/FearScream/Train/'+video_name+'/'
frames_list = sorted_alphanumeric(glob.glob(directory+'*.jpg'))
print(frames_list)




IMG_DIM = 112
CHANNELS = 3
input_shape = (CHANNELS, IMG_DIM, IMG_DIM)

transform = transforms.Compose(
        [
            transforms.Resize(input_shape[-2:], Image.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )



def convert_to_frames(video_path):


    frames_list = sorted_alphanumeric(glob.glob(directory + '*.jpg'))
    return frames_list

def get_cropped_frames(frames_list):
    cropped_image_sequence_behaviour = []
    coordinates_array = []
    cropped_image_sequence_for_emotion = []


    for i in range(15):
        selected_frame = cv2.imread(frames_list[i])

        cropped_behaviour, coordinates = crop_human(selected_frame)

        cropped_image_sequence_for_emotion.append(cropped_behaviour)
        cropped_image_sequence_behaviour.append(transform(Image.fromarray(cropped_behaviour)))

        coordinates_array.append(coordinates)

    cropped_image_sequence = torch.stack(cropped_image_sequence_behaviour)
    return cropped_image_sequence, coordinates_array, cropped_image_sequence_for_emotion

