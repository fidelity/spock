---
sidebar_label: saver
title: backend.saver
---

Handles prepping and saving the Spock config

## BaseSaver Objects

```python
class BaseSaver(BaseHandler)
```

Base class for saving configs

Contains methods to build a correct output payload and then writes to file based on the file
extension

*Attributes*:

    _writers: maps file extension to the correct i/o handler
    _s3_config: optional S3Config object to handle s3 access

#### dict\_payload

```python
def dict_payload(payload)
```

Clean up the config payload so it can be returned as a dict representation

*Args*:

    payload: dirty payload

*Returns*:

    clean_dict: cleaned output payload

#### save

```python
def save(payload, path, file_name=None, create_save_path=False, extra_info=True, file_extension=".yaml", tuner_payload=None, fixed_uuid=None)
```

Writes Spock config to file

Cleans and builds an output payload and then correctly writes it to file based on the
specified file extension

*Args*:

    payload: current config payload
    path: path to save
    file_name: name of file (will be appended with .spock.cfg.file_extension) -- falls back to uuid if None
    create_save_path: boolean to create the path if non-existent
    extra_info: boolean to write extra info
    file_extension: what type of file to write
    tuner_payload: tuner level payload (unsampled)
    fixed_uuid: fixed uuid to allow for file overwrite

*Returns*:

    None

#### \_clean\_up\_values

```python
@abstractmethod
def _clean_up_values(payload)
```

Clean up the config payload so it can be written to file

*Args*:

    payload: dirty payload

*Returns*:

    clean_dict: cleaned output payload

#### \_clean\_tuner\_values

```python
@abstractmethod
def _clean_tuner_values(payload)
```

Cleans up the base tuner payload that is not sampled

*Args*:

    payload: dirty payload

*Returns*:

    clean_dict: cleaned output payload

#### \_clean\_output

```python
def _clean_output(out_dict)
```

Clean up the dictionary so it can be written to file

*Args*:

    out_dict: cleaned dictionary
    extra_info: boolean to add extra info

*Returns*:

    clean_dict: cleaned output payload

#### \_recursive\_tuple\_to\_list

```python
def _recursive_tuple_to_list(value)
```

Recursively turn tuples into lists

Recursively looks through tuple(s) and convert to lists

*Args*:

    value: value to check and set typ if necessary
    typed: type of the generic alias to check against

*Returns*:

    value: updated value with correct type casts

## AttrSaver Objects

```python
class AttrSaver(BaseSaver)
```

Base class for saving configs for the attrs backend

Contains methods to build a correct output payload and then writes to file based on the file
extension

*Attributes*:

    _writers: maps file extension to the correct i/o handler

#### \_recursively\_handle\_clean

```python
def _recursively_handle_clean(payload, out_dict, parent_name=None, all_cls=None)
```

Recursively works through spock classes and adds clean data to a dictionary

Given a payload (Spockspace) work recursively through items that don&#x27;t have parents to catch all
parameter definitions while correctly mapping nested class definitions to their base level class thus
allowing the output markdown to be a valid input file

*Args*:

    payload: current payload (namespace)
    out_dict: output dictionary
    parent_name: name of the parent spock class if nested
    all_cls: all top level spock class definitions

*Returns*:

    out_dict: modified dictionary with the cleaned data

