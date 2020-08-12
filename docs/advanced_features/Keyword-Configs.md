# Keyword Configs

`spock` supports adding and/or overriding the config file path(s) normally specified via the command line argument `-c`
with keyword arguments.

### Specifying The Config Keyword Argument

Let's pass in the `yaml` configuration file via the config keyword argument instead of at the command line. Simply
add the `config` keyword argument to the `ConfigArgBuilder`. Note: This is not the recommended best practice as it
creates a dependency between code and configuration files. Please use the `-c` command line argument whenever possible.
The `config` keyword arg should be used *ONLY* when necessary.

Editing our definition in: `tutorial.py`

```python
...

def main():
    # A simple description
    description = 'spock Advanced Tutorial'
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, DataConfig, SGDConfig, desc=description, config=['./tutorial.yaml']).generate()
    # Instantiate our neural net using
    basic_nn = BasicNet(model_config=config.ModelConfig)
    # Make some random data (BxH): H has dim of features in
    x_data = torch.rand(config.DataConfig.n_samples, config.ModelConfig.n_features)
    y_data = torch.randint(0, 3, (config.DataConfig.n_samples,))
    # Run some training
    train(x_data, y_data, basic_nn, config.ModelConfig, config.DataConfig, config.SGDConfig)

```

Now to run `tutorial.py` we don't need to pass a command line argument:

```bash
$ python tutorial.py
```

### Specifying The Config Keyword Argument & The No Command Line Flag

So if the `config` keyword arg is not recommended why do we support it? Mainly for two reasons:
- Programmatic access to configuration files for other code/infrastructure (e.g. dispatching jobs from a work queue 
that might need to be parametrized) 
- To prevent command line arg clashes with other python code/libraries that might use the same or similar syntax (e.g. 
FastAPI)

For instance, let's say we were wrapping our simple neural net example into an async REST API (using something 
like [FastAPI](https://fastapi.tiangolo.com/) and a message queue such as redis). The FastAPI docker 
[image](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker) has it's own set of command line arguments that get
called and will clash with `spock`. Therefore we need to pass the configuration file(s) through the `config` keyword
argument and deactivate the command line argument.

For instance, we create a route for our basic neural network (shown below). We add the `no_cmd_line=True` flag to the 
`ConfigArgBuilder` to prevent `spock` from references command line arguments:

```python
@api.post("/inference/",  status_code=201)
def create_job(*, data: schemata.Inference):
    # Build out the parser by passing in Spock config objects as *args after description
    config = ConfigArgBuilder(ModelConfig, DataConfig, SGDConfig, desc=description, config=['./tutorial.yaml'], 
                              no_cmd_line=True).generate()
    # Let's assume we have a model loading function based on our params
    basic_nn = LoadBasicNet(model_config=config.ModelConfig)
    # Make a prediction
    y = basic_nn(data.x)
    # Return the predictions
    return_schema = schemata.InferenceReturn(
        y=y,
    )
    return return_schema
```

