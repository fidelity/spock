from basic_nn import BasicNet
from spock.args import *
from spock.builder import ConfigArgBuilder
from spock.config import spock_config
import torch


@spock_config
class ModelConfig:
    save_path: SavePathOptArg
    n_features: IntArg
    dropout: ListArg[float]
    hidden_sizes: TupleArg[int]
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'])


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
