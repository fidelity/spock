from basic_nn import BasicNet
from spock.args import *
from spock.builder import ConfigArgBuilder
from spock.config import spock_config
import torch


@spock_config
class ModelConfig:
    save_path: SavePathOptArg
    n_features: IntArg
    dropout: ListOptArg[float]
    hidden_sizes: TupleArg[int] = TupleArg.defaults((32, 32, 32))
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'], default='relu')
    optimizer: ChoiceArg(choice_set=['SGD', 'Adam'])
    cache_path: StrOptArg


@spock_config
class DataConfig:
    batch_size: IntArg = 2
    n_samples: IntArg = 8
    cache_path: StrOptArg


@spock_config
class OptimizerConfig:
    lr: FloatArg = 0.01
    n_epochs: IntArg = 2
    grad_clip: FloatOptArg


@spock_config
class SGDConfig(OptimizerConfig):
    weight_decay: FloatArg
    momentum: FloatArg
    nesterov: BoolArg


def train(x_data, y_data, model, model_config, data_config, optimizer_config):
    if model_config.optimizer == 'SGD':
        optimizer = torch.optim.SGD(model.parameters(), lr=optimizer_config.lr, momentum=optimizer_config.momentum,
                                    nesterov=optimizer_config.nesterov)
    elif model_config.optimizer == 'Adam':
        optimizer = torch.optim.Adam(model.parameters(), lr=optimizer_config.lr)
    else:
        raise ValueError(f'Optimizer choice {optimizer_config.optimizer} not available')
    n_steps_per_epoch = data_config.n_samples % data_config.batch_size
    for epoch in range(optimizer_config.n_epochs):
        for i in range(n_steps_per_epoch):
            # Ugly data slicing for simplicity
            x_batch = x_data[i * n_steps_per_epoch:(i + 1) * n_steps_per_epoch, ]
            y_batch = y_data[i * n_steps_per_epoch:(i + 1) * n_steps_per_epoch, ]
            optimizer.zero_grad()
            output = model(x_batch)
            loss = torch.nn.CrossEntropyLoss(output, y_batch)
            loss.backward()
            if optimizer_config.grad_clip:
                torch.nn.utils.clip_grad_value(model.parameters(), optimizer_config.grad_clip)
            optimizer.step()
        print(f'Finished Epoch {epoch+1}')


def main():
    # A simple description
    description = 'spock Advanced Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, DataConfig, SGDConfig, desc=description).generate()
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    x_data = torch.rand(config.DataConfig.n_samples, config.ModelConfig.n_features)
    y_data = torch.randint(0, 3, (config.DataConfig.n_samples,))
    # Run some training
    train(x_data, y_data, basic_nn, config.ModelConfig, config.DataConfig, config.SGDConfig)


if __name__ == '__main__':
    main()
