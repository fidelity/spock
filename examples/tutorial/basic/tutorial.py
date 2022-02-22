from enum import Enum
from typing import List, Tuple

import torch
from basic_nn import BasicNet

from spock import SpockBuilder
from spock import spock


class Activation(Enum):
    """Options for activation functions

    Attributes:
        relu: relu activation
        gelu: gelu activation
        tanh: tanh activation
    """

    relu = "relu"
    gelu = "gelu"
    tanh = "tanh"


@spock
class ModelConfig:
    """Main model configuration for a basic neural net

    Attributes:
        save_path: spock special keyword -- path to write out spock config state
        n_features: number of data features
        dropout: dropout rate for each layer
        hidden_sizes: hidden size for each layer
        activation: choice from the Activation enum of the activation function to use
    """

    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int, int, int]
    activation: Activation


def main():
    # A simple description
    description = "spock Basic Tutorial"
    # Build out the parser by passing in Spock config objects as *args after description
    config = (
        SpockBuilder(ModelConfig, desc=description, create_save_path=True)
        .save(file_extension=".toml")
        .generate()
    )
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    test_data = torch.rand(10, config.ModelConfig.n_features)
    result = basic_nn(test_data)
    print(result)


if __name__ == "__main__":
    main()
