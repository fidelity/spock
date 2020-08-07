# Composing Configuration Files

`spock` supports hierarchical composition of configuration files with a simple syntax.


### Composing Two YAML Files

Going back to our example. Let's say we had a a portion of our configuration that does not change that often while
another portion changes frequently or are parameters that are being experimented with. For instance, let's say we have
finalized things related to our data set (although in our examples it is random... let's just imagine for now) but we are
still experimenting with our neural network parameters. 

Instead of maintaining multiple copies of configuration files where parameters related to the data set are not 
changing, we can compose two separate configuration files together. One static file related to the data set parameters 
and a more dynamic file that is changing. This separation helps keep errors from propagating into the static set of
data set related parameters.

For instance we can break our `tutorial.yaml` file into two.

First, let's split out the static data related parameters into: `data.yaml`

```yaml
################
# data.yaml
################
# DataConfig
batch_size: 2
n_samples: 8
DataConfig:
  cache_path: /home/user/cache/
```

And then in our second configuration file we can use the `config:` key to define the other configuration files we want
to compose into this configuration file: `changing.yaml`

```yaml
################
# changing.yaml
################
# Global
cache_path: /tmp/cache/
config: [/data.yaml]
# Special Key
save_path: /tmp
# ModelConfig
n_features: 64
dropout: [0.2, 0.1]
hidden_sizes: [32, 32, 16]
activation: relu
optimizer: SGD
# OptimizerConfig
lr: 0.01
n_epochs: 2
grad_clip: 5.0
# SGD Config
weight_decay: 1E-5
momentum: 0.9
--nesterov
```


### Warning 
You can add as many configuration files as you want to a `config` tag however be aware of circular dependencies (we
do not check for these yet) and that the lower a configuration file is in the order (i.e. later in the list) that
it will take precedence over the others.