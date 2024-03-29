# -*- coding: utf-8 -*-
import torch.nn as nn


class BasicNet(nn.Module):
    def __init__(self, model_config):
        super(BasicNet, self).__init__()
        # Make a dictionary of activation functions to select from
        self.act_fncs = {"relu": nn.ReLU, "gelu": nn.GELU, "tanh": nn.Tanh}
        self.use_act = self.act_fncs.get(model_config.activation)()
        # Define the layers manually (avoiding list comprehension for clarity)
        self.layer_1 = nn.Linear(model_config.n_features, model_config.hidden_sizes[0])
        self.layer_2 = nn.Linear(
            model_config.hidden_sizes[0], model_config.hidden_sizes[1]
        )
        self.layer_3 = nn.Linear(
            model_config.hidden_sizes[1], model_config.hidden_sizes[2]
        )
        # Define some dropout layers
        self.dropout = []
        if model_config.dropout is not None:
            self.dropout = [nn.Dropout(val) for val in model_config.dropout]
        # Define the output layer
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # x is the data input
        # Layer 1
        # Linear
        x = self.layer_1(x)
        # Activation
        x = self.use_act(x)
        # Dropout
        if len(self.dropout) != 0:
            x = self.dropout[0](x)
        # Layer 2
        # Linear
        x = self.layer_2(x)
        # Activation
        x = self.use_act(x)
        # Dropout
        if len(self.dropout) != 0:
            x = self.dropout[1](x)
        # Layer 3
        # Linear
        x = self.layer_3(x)
        # Softmax
        output = self.softmax(x)
        return output
