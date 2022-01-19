# Drop In Replacement For Argparser

`spock` can easily be used as a drop in for argparser. This means that all parameter definitions as required to come in 
from the command line or from setting defaults within the `@spock` decorated classes.

### Automatic Command-Line Argument Generation

`spock` will automatically generate command line arguments for each parameter, unless the `no_cmd_line=True` flag is 
passed to the `SpockBuilder`. Let's create a simple example to demonstrate:

```python
from spock import spock
from typing import Optional

@spock
class ExampleConfig:
    read_path: str = '/tmp'
    date: int
    cache_path: Optional[str]
```

Given these definitions, `spock` will automatically generate a command-line argument (via an internally maintained 
argparser) for each parameter within each `@spock` decorated class. The syntax follows simple dot notation 
of `--classname.parameter`. Thus, for our sample classes above, `spock` will automatically generate the following 
valid command-line arguments:

```shell
--ExampleConfig.read_path *value*
--ExampleConfig.date *value*
--ExampleConfig.cache_path *value*
```

### Use Spock via the Command-Line

Simply do not pass a `-c` or `--config` argument at the command line and instead pass in all values to the 
automatically generated cmd-line arguments.

```bash
$ python simple.py --ExampleConfig.read_path /my/file/path --ExampleConfig.date 1292838124 \
--ExampleConfig.cache_path /path/to/cache/dir
```