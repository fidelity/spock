# Saving

The current configuration of running python code can be saved to file by chaining the `save()` method before 
the `generate()` call to the `ConfigArgBuilder` class. `spock` supports two ways to specify the path to write and the
output file can be either YAML, TOML, or JSON (via the `file_extension` keyword argument).

### Specify spock Special Parameter Type

We simply specify a `SavePathOptArg` in a spock config, which is a special argument type that is used to set the 
save path from a configuration file.

Adding to: `tutorial.py`

```python
@spock_config
class ModelConfig:
    save_path: SavePathOptArg
    n_features: IntArg
    dropout: ListArg[float]
    hidden_sizes: TupleArg[int]
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'])
```

And adding in the chained `save()` call...

```python
def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, desc=description).save(file_extension='.toml').generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)
```

Adding the output path to our configuration file: `tutorial.yaml`

```yaml
################
# tutorial.yaml
################
# Special Key
save_path: /tmp
# ModelConfig
n_features: 64
dropout: [0.2, 0.1]
hidden_sizes: [32, 32, 16]
activation: relu
```

### Specify Path In-Line

Here we simply specify the path when calling the `save()` method. In: `tutorial.yaml`

```python
def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, desc=description).save(user_specified_path='/tmp').generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)
```

### Does the Directory Exit

In either case, if the save path does not exist, it will not be created by default. To change this behavior, 
set `create_save_path` when creating the builder.

In: `tutorial.py`

```python
def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, desc=description, create_save_path=True).save().generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)
```