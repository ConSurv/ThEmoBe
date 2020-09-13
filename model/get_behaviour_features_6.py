
def get_behaviour_features(behaviour_model,cropped_image_sequence_behaviour):

    behaviour_features = np.empty((0,1024))

    behaviour_model.eval()
    with torch.no_grad():
        image_sequences = Variable(cropped_image_sequence_behaviour.resize_((1,15,3,112,112)).to(device), requires_grad=False)
        print(image_sequences.shape)
        print(type(image_sequences))

        # Reset LSTM hidden state
        behaviour_model.lstm.reset_hidden_state()
        # Get sequence predictions
        predictions = behaviour_model(image_sequences)

        pred = predictions.to(torch.device("cpu")).numpy()
        print(pred.shape)

        behaviour_features = np.append(behaviour_features, pred, axis = 0)
        print(behaviour_features.shape)

        return  behaviour_features