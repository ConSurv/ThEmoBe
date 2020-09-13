import sys

sys.path.append('../../')
import Lock
import time
import os
from datetime import datetime

from params import params as Params
import pickle
from model.obsolete.gsom_from_weights_9 import *

def generate_output_config(SF, forget_threshold):
    # File Config
    dataset = 'Classifier'
    experiment_id = 'Exp-' + datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H-%M-%S')
    output_save_location = join('output/', experiment_id)

    # Output data config
    output_save_filename = '{}_data_'.format(dataset)
    filename = output_save_filename + str(SF) + '_T_' + str(temporal_contexts) + '_mage_' + str(
        forget_threshold) + 'itr'
    plot_output_name = join(output_save_location, filename)

    # Generate output plot location
    output_loc = plot_output_name
    output_loc_images = join(output_loc, 'images/')
    if not os.path.exists(output_loc):
        os.makedirs(output_loc)
    if not os.path.exists(output_loc_images):
        os.makedirs(output_loc_images)

    return output_loc, output_loc_images



SF = 0.83
forget_threshold = 60
temporal_contexts = 1
learning_itr = 100
smoothing_irt = 50
plot_for_itr = 4

# Init GSOM Parameters
gsom_params = Params.GSOMParameters(SF, learning_itr, smoothing_irt,
                                    distance=Params.DistanceFunction.EUCLIDEAN,
                                    temporal_context_count=temporal_contexts,
                                    forget_itr_count=forget_threshold)
generalise_params = Params.GeneraliseParameters(gsom_params)

# Setup the age threshold based on the input vector length
generalise_params.setup_age_threshold(Lock.INPUT_SIZE)

# Process the input files
output_loc, output_loc_images = generate_output_config(SF, forget_threshold)


EmotionGSOM = GSOM_from_Weights(generalise_params.get_gsom_parameters())

BehaviourGSOM = GSOM_from_Weights(generalise_params.get_gsom_parameters())

ThreatGSOM = GSOM_from_Weights(generalise_params.get_gsom_parameters())

pickle_directory = "/content/drive/My Drive/Dataset/FEATURES/output-50-epoc/"

pickle_in = open(pickle_directory+"final-emotion-gsom_nodemap_SF-0.83_2020-07-29-05-39-20.pickle","rb")
dict_map = pickle.load(pickle_in)
emotion_node_map = dict_map[0].get('gsom')

pickle_in = open(pickle_directory+"final-behavior-gsom_nodemap_SF-0.83_2020-07-29-05-39-21.pickle","rb")
dict_map = pickle.load(pickle_in)
behaviour_node_map = dict_map[0].get('gsom')

pickle_in = open(pickle_directory+"final-threat-gsom_nodemap_SF-0.83_2020-07-29-12-06-28.pickle","rb")
dict_map = pickle.load(pickle_in)
threat_node_map = dict_map[0].get('gsom')


EmotionGSOM.loadWeights(emotion_node_map)

BehaviourGSOM.loadWeights(behaviour_node_map)

ThreatGSOM.loadWeights(threat_node_map)