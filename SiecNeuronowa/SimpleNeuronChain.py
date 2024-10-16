import torch
import torch.utils.data as data

# We will try to create a simple one-directional neuron chain for XOR operation on float numbers.

# Class that would pairs of input - output training data
class XORDataCreator(data.Dataset):

    """
    XORDataCreator jest klasą, która generuje losowe dane treningowe dla głębokiej sieci klasyfikacyjnej.
    Klasyfikator, który korzysta z generowanych danych powinien otrzymać parę liczb zmiennoprzecinkowych
    obarczonych szumem oraz oznaczenie pary liczb jakiego wyniku alternatywy rozłącznej (operacja XOR)
    spodziewamy się po tej parze. Na tej podstawie sieć ma nauczyć się rozpoznawać wyniki z możliwie jak najwyższą
    poprawnością nieznanej dotąd pary liczb zmiennoprzecinkowych.
    """

    def __init__(self, data_size, noise_std_deviation) -> None :
        super().__init__()
        self.data_size = data_size
        self.noise_std_deviation = noise_std_deviation
        self.generate_random_xor_data()

    def generate_random_xor_data(self):
        # Generate random float [x0, x1] pairs of data from  range [0 ... 2]
        xor_data = torch.randint(low=0, high=2, size=(self.data_size, 2), dtype=torch.float32)

        # Generate random noise for data
        xor_data_noise = self.noise_std_deviation * torch.randn(xor_data.shape)

        # Data labeling - assing expected value d to each data pair
        # Here we cast each data from pair to int and generate xor result
        labels = [xor_item[0].to(int) ^ xor_item[1].to(int) for xor_item in xor_data]

        # Store combined data + noise
        xor_data_with_noise = xor_data + xor_data_noise
        self.data_inputs = xor_data_with_noise

        # Convert results to float numbers
        labels_converted_to_numbers = labels
        self.data_labels = [label.to(torch.long) for label in labels]

    def __len__(self):
        return self.data_size

    def __getitem__(self, idx):
        return [self.data_inputs[idx], self.data_labels[idx]]

# Use generator to generate 300 training data sets
xor_training_data = XORDataCreator(300, 0.1)

#Print some data
print(xor_training_data[121])


#Create neuron chain and define its archotecture
import torch.nn as nn


# nm.Module represents single - way 3 layers (one hidden layer) neuron chain (neutral network)
class ClassifierModel(nn.Module):
    
    # nn.Linear is a linear transformation from each neurons of input layer to next layer. The transformation will do a transform operations with wages, scaling wages to best-fit form.
    # The transformation is like: neuron_input = Wn*Xn + W(n+1)*X(n+1) + ...
    # Activation function Tanh is a hiperbolic tangens function, is otuput is [-1 ... 1] That will transform neuton input calculated in linear transformation from first step.
    def __init__(self, inputs_number, hidden_layer_neurons_number, outputs_number) -> None:
        super().__init__()
        self.first_layer_to_hidden_transformation = nn.Linear(inputs_number, hidden_layer_neurons_number)
        self.activation_function = nn.Tanh()
        self.hidden_layer_to_output_transformation = nn.Linear(hidden_layer_neurons_number, outputs_number)
    
    # That function defines what shall be done for each layer of a network. That actions will be done on each layer - prepare and wage input signal, apply transform function, prepare output.
    def forward(self, input):
        x = self.first_layer_to_hidden_transformation(input)
        x = self.activation_function(x)
        x = self.hidden_layer_to_output_transformation(x)
        return x

    def __init__(self, inputs_number, hidden_layer_neurons_number, outputs_number) -> None:
        super().__init__()
        self.first_layer_to_hidden_transformation = nn.Linear(inputs_number, hidden_layer_neurons_number)
        self.activation_function = nn.Tanh()
        self.hidden_layer_to_output_transformation = nn.Linear(hidden_layer_neurons_number, outputs_number)




# Now we create a procedure for training the network

import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter
 
class Net():
 
    def __init__(self) -> None:
        self.loss_calculation_model = None
        self.optimizer = None
        self.data_loader = XORDataCreator(data_size=250, noise_std_deviation=0.1)
 
    def train_and_log(self, model: ClassifierModel, epochs_num: int=150):
        # Sprawdźmy czy możemy wykorzystać GPU poprzez pakiet CUDA celem przyspieszenia obliczeń
        gpu_available = torch.cuda.is_available()
        # W przypadku możliwości ustawmy 'device' na GPU
        device = torch.device('cuda') if gpu_available else torch.device('cpu')
 
        # Inicjalizacja
        self.loss_calculation_model = nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
 
        # Załadujmy nasz model do GPU jeśli jest dostępne
        model.to(device)
        # Ustawmy model w tryb treningowy (funkcjonalność odziedziczona po klasie nn.Module)
        model.train()
 
        # Inicjalizacja loggera TensorBoard, logi zapisujemy do folderu 'logs'
        tensorboard_logger = SummaryWriter('logs/')
        tensorboard_initialized = False
 
        # Pętla treningowa (pobierz paczkę danych treningowych)
        for current_epoch in range(epochs_num):
            epoch_loss = 0.0
            for data_inputs, data_labels in self.data_loader:
                # Załadujmy nasze dane do GPU jeśli jest w użyciu
                data_inputs = data_inputs.to(device)
                data_labels = data_labels.to(device)
 
                if not tensorboard_initialized:
                    # Inicjalizacja grafu odbywa się tylko raz, kolekcja data_inputs się nie zmienia,
                    # nie ma potrzeby inicjalizować ponownie
                    tensorboard_logger.add_graph(model, data_inputs)
                    tensorboard_initialized = True
 
                # Przeprocedujmy dane wejściowe przez nasz model
                predicted_output = model(data_inputs)
                predicted_output = predicted_output[0]
 
                # Obliczmy wartość funkcji straty (jak bardzo nasz model się pomylił)
                loss = self.loss_calculation_model(predicted_output, data_labels.float())
 
                # Wyzerujmy wartość gradientu na wszelki wypadek
                self.optimizer.zero_grad()
 
                # Dokonajmy propagacji wstecznej błędu
                loss.backward()
 
                # Zaktualizujmy wagi sieci na podstawie obliczonego gradientu
                self.optimizer.step()
 
                # Obliczenie średniej pomyłki obecnej iteracji treningowej
                epoch_loss += loss.item()
 
                # Dodanie kolejnego punktu na wykresie obrazującym błąd sieci
                tensorboard_logger.add_scalar('blad', epoch_loss, global_step = current_epoch + 1)
 
        tensorboard_logger.close()
 
    def set_optimizer(self, optimizer) -> None:
        self.optimizer = optimizer
 
    def set_loss_calc_model(self, loss_calc_model) -> None:
        self.loss_calculation_model = loss_calc_model
 
    def get_training_data(self) -> XORDataCreator:
        return self.data_loader
