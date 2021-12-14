# Saving

The current configuration of running python code can be saved to file by chaining the `save()` method before 
the `generate()` call to the `ConfigArgBuilder` class. `spock` supports two different ways to specify the write path 
and supports multiple output formats (YAML, TOML, or JSON -- via the `file_extension` keyword argument). Most 
importantly, the saved markdown file can be used as the configuration input to reproduce prior runtime configurations.

### What Does spock Save?

By default `spock` will append extra information (via the `extra_info` kwarg) as well as the entire state of the 
configuration object. Extra info includes:

  - Git Info: Branch, Commit ID (SHA-1), Commit Date, Status (e.g. dirty), Origin
  - Python Info: Executable Path, Version, Script Entrypoint
  - Run Information: Date, Time
  - Env Information: Machine FQDN, Run w/ Docker, Run w/ Kubernetes 
  - Spock Version

For instance, here is an example of the `tutorial.py` saved `.toml` output:

```toml
# Spock Version: v2.1.5+0.gf9bf3bc.dirty
# Machine FQDN: XXXXX.yyy.com
# Python Executable: /Users/XXXXX/.virtualenvs/spock/bin/python
# Python Version: 3.8.5
# Python Script: /XXXX/open_source/spock/examples/tutorial/basic/tutorial.py
# Run Date: 2021-05-24
# Run Time: 13:33:41
# Run w/ Docker: False
# Run w/ Kubernetes: False
# Git Branch: master
# Git Commit: f9bf3bca0098a98b994eaa2aeb257f0023704e32
# Git Date: 2021-05-10 10:33:56-04:00
# Git Status: DIRTY
# Git Origin: https://github.com/fidelity/spock.git

[ModelConfig]
save_path = "/tmp"
n_features = 64
dropout = [ 0.2, 0.1,]
hidden_sizes = [ 32, 32, 16,]
activation = "relu"
```

### Specify spock Special Parameter Type

We simply specify a `SavePath` in a spock config, which is a special argument type that is used to set the 
save path from a configuration file.

Adding to: `tutorial.py`

```python
class Activation(Enum):
    relu = 'relu'
    gelu = 'gelu'
    tanh = 'tanh'


@spock
class ModelConfig:
    save_path: SavePath
    n_features: int
    dropout: List[float]
    hidden_sizes: Tuple[int, int, int]
    activation: Activation
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
    config = ConfigArgBuilder(ModelConfig, desc=description).save(create_save_path=True).generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)
```

### Override UUID Filename

By default `spock` uses an automatically generated UUID as the filename when saving. This can be overridden with the
`file_name` keyword argument. The specified filename will be appended with .spock.cfg.file_extension (e.g. .yaml, 
.toml or. json).

In: `tutorial.py`

```python
def main():
    # A simple description
    description = 'spock Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, desc=description).save(file_name='cool_name_here').generate()
    # One can now access the Spock config object by class name with the returned namespace
    # For instance...
    print(config.ModelConfig)
```