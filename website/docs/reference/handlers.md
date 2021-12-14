---
sidebar_label: handlers
title: handlers
---

I/O handlers for various file formats

## Handler Objects

```python
class Handler(ABC)
```

Base class for file type loaders

ABC for loaders

#### load

```python
def load(path: Path, s3_config=None) -> typing.Dict
```

Load function for file type

This handles s3 path conversion for all handler types pre load call

*Args*:

    path: path to file
    s3_config: optional s3 config object if using s3 storage

*Returns*:

    dictionary of read file

#### \_post\_process\_config\_paths

```python
@staticmethod
def _post_process_config_paths(payload)
```

Transform path string into path object

#### \_load

```python
@abstractmethod
def _load(path: str) -> typing.Dict
```

Private load function for file type

*Args*:

    path: path to file

*Returns*:

    dictionary of read file

#### save

```python
def save(out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: Path, name: str, create_path: bool = False, s3_config=None)
```

Write function for file type

This will handle local or s3 writes with the boolean is_s3 flag. If detected it will conditionally import
the necessary addons to handle the upload

*Args*:

    out_dict: payload to write
    info_dict: info payload to write
    path: path to write out
    name: spock generated file name
    create_path: boolean to create the path if non-existent (for non S3)
    s3_config: optional s3 config object if using s3 storage

*Returns*:

#### \_save

```python
@abstractmethod
def _save(out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str) -> str
```

Write function for file type

*Args*:

    out_dict: payload to write
    info_dict: info payload to write
    path: path to write out

*Returns*:

#### \_handle\_possible\_s3\_load\_path

```python
@staticmethod
def _handle_possible_s3_load_path(path: Path, s3_config=None) -> typing.Union[str, Path]
```

Handles the possibility of having to handle loading from a S3 path

Checks to see if it detects a S3 uri and if so triggers imports of s3 functionality and handles the file
download

*Args*:

    path: spock config path
    s3_config: optional s3 configuration object

*Returns*:

    path: current path for the configuration file

#### \_handle\_possible\_s3\_save\_path

```python
@staticmethod
def _handle_possible_s3_save_path(path: Path, name: str, create_path: bool, s3_config=None) -> typing.Tuple[str, bool]
```

Handles the possibility of having to save to a S3 path

Checks to see if it detects a S3 uri and if so generates a tmp location to write the file to pre-upload

*Args*:

    path: save path
    name: spock generated file name
    create_path: create the path for non s3 data
    s3_config: s3 config object

*Returns*:

#### write\_extra\_info

```python
@staticmethod
def write_extra_info(path, info_dict)
```

Writes extra info to commented newlines

*Args*:

    path: path to write out
    info_dict: info payload to write

*Returns*:

## YAMLHandler Objects

```python
class YAMLHandler(Handler)
```

YAML class for loading YAML config files

Base YAML class

#### \_load

```python
def _load(path: str) -> typing.Dict
```

YAML load function

*Args*:

    path: path to YAML file

*Returns*:

    base_payload: dictionary of read file

#### \_save

```python
def _save(out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str)
```

Write function for YAML type

*Args*:

    out_dict: payload to write
    info_dict: info payload to write
    path: path to write out

*Returns*:

## TOMLHandler Objects

```python
class TOMLHandler(Handler)
```

TOML class for loading TOML config files

Base TOML class

#### \_load

```python
def _load(path: str) -> typing.Dict
```

TOML load function

*Args*:

path: path to TOML file

**Returns**:

  
- `base_payload` - dictionary of read file

#### \_save

```python
def _save(out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str)
```

Write function for TOML type

*Args*:

    out_dict: payload to write
    info_dict: info payload to write
    path: path to write out

*Returns*:

## JSONHandler Objects

```python
class JSONHandler(Handler)
```

JSON class for loading JSON config files

Base JSON class

#### \_load

```python
def _load(path: str) -> typing.Dict
```

JSON load function

*Args*:

path: path to JSON file

**Returns**:

  
- `base_payload` - dictionary of read file

#### \_save

```python
def _save(out_dict: typing.Dict, info_dict: typing.Optional[typing.Dict], path: str)
```

Write function for JSON type

*Args*:

    out_dict: payload to write
    info_dict: info payload to write
    path: path to write out

*Returns*:

