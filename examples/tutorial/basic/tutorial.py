from basic_nn import BasicNet
from enum import Enum
from spock.args import SavePath
from spock.builder import ConfigArgBuilder
from spock.config import spock
import torch
from typing import List
from typing import Tuple


class Activation(Enum):
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


@spock
class ModelConfig:
    save_path: SavePath
    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int]
    activation: Activation


def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(
        ModelConfig, desc=description, create_save_path=True).save(file_extension='.toml').generate()
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    test_data = torch.rand(10, config.ModelConfig.n_features)
    result = basic_nn(test_data)
    print(result)


if __name__ == '__main__':
    main()
