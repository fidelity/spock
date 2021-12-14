---
sidebar_label: builder
title: builder
---

Handles the building/saving of the configurations from the Spock config classes

## ConfigArgBuilder Objects

```python
class ConfigArgBuilder()
```

Automatically generates dataclass instances from config file(s)

This class builds out necessary arguments from *args classes, reads
the arguments from specified config file(s), and subsequently (via chained
call to generate) generates each class instance based on the necessary
field values for each backend class instance

*Attributes*:

    _args: all command line args
    _arg_namespace: generated argument namespace
    _builder_obj: instance of a BaseBuilder class
    _dict_args: dictionary args from the command line
    _payload_obj: instance of a BasePayload class
    _saver_obj: instance of a BaseSaver class
    _tune_payload_obj: payload for tuner related objects -- instance of TunerPayload class
    _tune_obj: instance of TunerBuilder class
    _tuner_interface: interface that handles the underlying library for sampling -- instance of TunerInterface
    _tuner_state: current state of the hyper-parameter sampler
    _tune_namespace: namespace that hold the generated tuner related parameters
    _sample_count: current call to the sample function
    _fixed_uuid: fixed uuid to write the best file to the same path

#### \_\_init\_\_

```python
def __init__(*args, *, configs: typing.Optional[typing.List] = None, desc: str = "", no_cmd_line: bool = False, s3_config=None, **kwargs, ,)
```

Init call for ConfigArgBuilder

*Args*:

    *args: tuple of spock decorated classes to process
    configs: list of config paths
    desc: description for help
    no_cmd_line: turn off cmd line args
    s3_config: s3Config object for S3 support
    **kwargs: keyword args

#### \_\_call\_\_

```python
def __call__(*args, **kwargs)
```

Call to self to allow chaining

*Args*:

    *args: non-keyword args
    **kwargs: keyword args

*Returns*:

    ConfigArgBuilder: self instance

#### generate

```python
def generate()
```

Generate method that returns the actual argument namespace


*Returns*:

    argument namespace consisting of all config classes

#### tuner\_status

```python
@property
def tuner_status()
```

Returns a dictionary of all the necessary underlying tuner internals to report the result

#### best

```python
@property
def best()
```

Returns a Spockspace of the best hyper-parameter config and the associated metric value

#### sample

```python
def sample()
```

Sample method that constructs a namespace from the fixed parameters and samples from the tuner space to
generate a Spockspace derived from both

*Returns*:

    argument namespace(s) -- fixed + drawn sample from tuner backend

#### tuner

```python
def tuner(tuner_config)
```

Chained call that builds the tuner interface for either optuna or ax depending upon the type of the tuner_obj

*Args*:

    tuner_config: a class of type optuna.study.Study or AX****

*Returns*:

    self so that functions can be chained

#### \_print\_usage\_and\_exit

```python
def _print_usage_and_exit(msg=None, sys_exit=True, exit_code=1)
```

Prints the help message and exits

*Args*:

    msg: message to print pre exit

*Returns*:

    None

#### \_handle\_tuner\_objects

```python
@staticmethod
def _handle_tuner_objects(tune_args, s3_config, kwargs)
```

Handles creating the tuner builder object if @spockTuner classes were passed in

*Args*:

    tune_args: list of tuner classes
    s3_config: s3Config object for S3 support
    kwargs: optional keyword args

*Returns*:

    tuner builder object or None

#### \_verify\_attr

```python
@staticmethod
def _verify_attr(args: typing.Tuple)
```

Verifies that all the input classes are attr based

*Args*:

    args: tuple of classes passed to the builder

*Returns*:

    None

#### \_strip\_tune\_parameters

```python
@staticmethod
def _strip_tune_parameters(args: typing.Tuple)
```

Separates the fixed arguments from any hyper-parameter arguments

*Args*:

    args: tuple of classes passed to the builder

*Returns*:

    fixed_args: list of fixed args
    tune_args: list of args destined for a tuner backend

#### \_handle\_cmd\_line

```python
def _handle_cmd_line()
```

Handle all cmd line related tasks

Config paths can enter from either the command line or be added in the class init call
as a kwarg (configs=[]) -- also trigger the building of the cmd line overrides for each fixed and
tunable objects

*Returns*:

    args: namespace of args

#### \_build\_override\_parsers

```python
def _build_override_parsers(desc)
```

Creates parsers for command-line overrides

Builds the basic command line parser for configs and help then iterates through each attr instance to make
namespace specific cmd line override parsers -- handles calling both the fixed and tunable objects

*Args*:

    desc: argparser description

*Returns*:

    args: argument namespace

#### \_get\_from\_kwargs

```python
@staticmethod
def _get_from_kwargs(args, configs)
```

Get configs from the configs kwarg

*Args*:

    args: argument namespace
    configs: config kwarg

*Returns*:

    args: arg namespace

#### \_get\_payload

```python
def _get_payload(payload_obj, input_classes, ignore_args: typing.List)
```

Get the parameter payload from the config file(s)

Calls the various ways to get configs and then parses to retrieve the parameter payload - make sure to call
deep update so as to not lose some parameters when only partially updating the payload

*Args*:

    payload_obj: current payload object to call
    input_classes: classes to use to get payload
    ignore_args: args that were decorated for hyper-parameter tuning

*Returns*:

    payload: dictionary of parameter values

#### \_save

```python
def _save(payload, file_name: str = None, user_specified_path: Path = None, create_save_path: bool = True, extra_info: bool = True, file_extension: str = ".yaml", tuner_payload=None, fixed_uuid=None)
```

Private interface -- saves the current config setup to file with a UUID

*Args*:

    payload: Spockspace to save
    file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to just uuid if None
    user_specified_path: if user provides a path it will be used as the path to write
    create_save_path: bool to create the path to save if called
    extra_info: additional info to write to saved config (run date and git info)
    file_extension: file type to write (default: yaml)
    tuner_payload: tuner level payload (unsampled)
    fixed_uuid: fixed uuid to allow for file overwrite

*Returns*:

    self so that functions can be chained

#### save

```python
def save(file_name: str = None, user_specified_path: typing.Union[Path, str] = None, create_save_path: bool = True, extra_info: bool = True, file_extension: str = ".yaml", add_tuner_sample: bool = False)
```

Saves the current config setup to file with a UUID

*Args*:

    file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to just uuid if None
    user_specified_path: if user provides a path it will be used as the path to write
    create_save_path: bool to create the path to save if called
    extra_info: additional info to write to saved config (run date and git info)
    file_extension: file type to write (default: yaml)
    append_tuner_state: save the current tuner sample to the payload

*Returns*:

    self so that functions can be chained

#### save\_best

```python
def save_best(file_name: str = None, user_specified_path: Path = None, create_save_path: bool = True, extra_info: bool = True, file_extension: str = ".yaml")
```

Saves the current best config setup to file

*Args*:

    file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to just uuid if None
    user_specified_path: if user provides a path it will be used as the path to write
    create_save_path: bool to create the path to save if called
    extra_info: additional info to write to saved config (run date and git info)
    file_extension: file type to write (default: yaml)

*Returns*:

    self so that functions can be chained

#### config\_2\_dict

```python
@property
def config_2_dict()
```

Dictionary representation of the arg payload

