from os.path import exists
import torch
from SimpleNeuronChain import *
 
__clasifier_model_state_file_name__ = "classifier_model.pt"
 
classifier_model = ClassifierModel(inputs_number=2, hidden_layer_neurons_number=5, outputs_number=1)
 
# Wczytaj poprzednio zapisany model, jeśli istnieje
if exists(__clasifier_model_state_file_name__):
    model_state = torch.load(__clasifier_model_state_file_name__)
    classifier_model.load_state_dict(model_state)
    print("Pretrained model loaded from ", __clasifier_model_state_file_name__)
 
net_model = Net()
net_model.train_and_log(model=classifier_model)
 
# Zapisz dotychczasowy model
model_state = classifier_model.state_dict()
torch.save(model_state, __clasifier_model_state_file_name__)
print("Trained model state dictionary saved to ", __clasifier_model_state_file_name__)