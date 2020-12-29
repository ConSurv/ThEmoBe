import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import os

def plot_boxes(i, img, x1, x2, y1, y2, prediction_labels, what_to_plot, plot_labels, color):
    # Get the width and height of the image
    width = img.shape[1]
    height = img.shape[0]

    # Create a figure and plot the image
    fig, axis = plt.subplots(1, 1)
    axis.imshow(img)

    # Set the default rgb value to red
    rgb1 = tuple(c / 255 for c in color)
    rgb = color

    # Calculate the width and height of the bounding box relative to the size of the image.
    width_x = x2 - x1
    width_y = y1 - y2

    # Set the postion and size of the bounding box. (x1, y2) is the pixel coordinate of the
    # lower-left corner of the bounding box relative to the size of the image.
    rect = patches.Rectangle((x1, y2),
                             width_x, width_y,
                             linewidth=2,
                             edgecolor=rgb1,
                             facecolor='none')

    # Draw the bounding box on top of the image
    axis.add_patch(rect)

    # If plot_labels = True then plot the corresponding label
    if plot_labels:
        # Create a string with the object class name and the corresponding object class probability
        # conf_tx = class_names[cls_id] + ': {:.1f}'.format(cls_conf)

        emotion_text = prediction_labels[0] + '\n' if what_to_plot[0] else ''
        behaviour_text = prediction_labels[1] + '\n' if what_to_plot[1] else ''
        threat_text = prediction_labels[2] if what_to_plot[2] else ''

        label_text =  emotion_text + behaviour_text + threat_text

        # Define x and y offsets for the labels
        lxc = (img.shape[1] * 0.266) / 100
        lyc = (img.shape[0] * 1.180) / 100

        # Draw the labels on top of the image
        axis.text(x1 + lxc, y1 - lyc, label_text, fontsize=18, color='k',
                  bbox=dict(facecolor=rgb1, edgecolor=rgb1, alpha=0.8))

        # d = ImageDraw.Draw(Image.fromarray(img))
        # d.text(xy=(x1 + lxc, y1 - lyc), text=label_text, fill=rgb)
    # return img
    # plt.show()
    fig.savefig("/root/ThEmoBe/output/img" + str(i) + ".png", bbox_inches='tight', transparent=True, pad_inches=0)



emotion_label_dictionary = {
    "0" : "Anger",
    "1" : "Sad",
    "2" : "Fear",
    "3" : "Surprise",
    "4" : "Happy",
    "5" : "Disgust"
}

behaviour_label_dictionary = {
    "0" : "Quarrel",
    "1" : "Mourn",
    "2" : "Scream",
    "3" : "Excitemet",
    "4" : "Laugh",
    "5" : "Physical Force",
    "6" : "Pinch",
    "7" : "Vomit"
}

threat_label_dictionary = {
     "1" : "No Threat (1)",
     "2" : "Low Threat (2)",
     "3" : "Moderate Threat (3)",
     "4" : "Substantial Threat (4)",
     "5" : "Severe Threat (5)"
}

#color (red, green, blue)
threat_color_dictionary = {
     "5" : (255, 0, 0), #red
     "4" : (255, 128, 0), #orange
     "3" : (255, 255, 102), #yellow
     "2" : (41, 52, 209), #blue
     "1" : (0, 204, 0) #green
}

def plot_bounding_boxes(predictions, frames_list, coordinates_array, what_to_plot, j):
    prediction_labels = [emotion_label_dictionary[predictions[0]],
                         behaviour_label_dictionary[predictions[1]],
                         threat_label_dictionary[predictions[2]]
                         ]

    print("prediction_labels ", prediction_labels)

    chunk_offset = j*15

    for i in range(len(frames_list)):
        selected_frame = cv2.imread(frames_list[i])
        coord = coordinates_array[i]
        x1, x2, y1, y2 = coord[0], coord[1], coord[2], coord[3]
        plot_boxes(i + chunk_offset, selected_frame, x1, x2, y1, y2, prediction_labels,what_to_plot, plot_labels=True, color = threat_color_dictionary[predictions[2]])



def make_video(APP_ROOT, output_video_id, len_frames_list):
    target = "/".join([APP_ROOT, "annotated_output/"])

    if not os.path.isdir(target):
        os.mkdir(target)

    img_array = []
    for i in range(len_frames_list):
        print("Reading " + "/root/ThEmoBe/output/img" + str(i) + ".png")
        try:
            img = cv2.imread("/root/ThEmoBe/output/img" + str(i) + ".png")
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
        except Exception as e:
            print(e)

    out = cv2.VideoWriter(target + output_video_id + ".avi", cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()