# Configuration Files

Values in `spock` are set using external configuration files.

### Supported Configuration Formats

#### YAML
* Requires file extension of `.yaml`.
* Supported using the external `PyYAML` library. 

#### TOML
* Requires file extension of `.toml`.
* Supported using the external `toml` library.

#### JSON
* Requires file extension of `.json`.
* Supported using the built-in `json` module.

### Creating a Configuration File

Recall that we defined our `spock` class as such:

```python
@spock_config
class ModelConfig:
    n_features: IntArg
    dropout: ListArg[float]
    hidden_sizes: TupleArg[int]
    activation: ChoiceArg(choice_set=['relu', 'gelu', 'tanh'])
```

Note that all of the types of our parameters `IntArg`, `ListArg`, `TupleArg`, and `ChoiceArg` are required types. This
means that if we do not specify values for these parameters in our configuration file `spock` will throw an exception. 

Let's create our configuration file using the YAML standard: `tutorial.yaml`

```yaml
################
# tutorial.yaml
################
# ModelConfig
n_features: 64
dropout: [0.2, 0.1]
hidden_sizes: [32, 32, 16]
activation: relu
```
