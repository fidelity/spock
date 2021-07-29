# Motivation

### Why Spock?

`spock` arose out of a few observations within the Artificial Intelligence Center of Excellence at Fidelity. 

#### Modern ML Models == Spaghetti Parameters

During research and development of machine learning (ML) models (especially deep learning models) the total 
number of configuration parameters within a codebase can quickly spiral out of control: data-related parameters, 
model hyper-parameters, logging parameters, i/o parameters, etc. After writing `parser.add_argument()` for the 1000th 
time we figured there had to be a better way to manage the complex configurations needed for modern ML models. 

In addition, we found a lot of open source ML/DL models (e.g. 
[NVIDIA OpenSeq2Seq](https://github.com/NVIDIA/OpenSeq2Seq)) that had mind-boggling spaghetti parameter definitions.
Just figuring out the configurations in order to run, modify, or re-implement an open-source model/library was 
becoming a minefield in and of itself.

#### Finding a Consistent Solution

Looking across an fast-moving enterprise scale AI organization, we noticed a pretty fractured set of 
configuration management practices across the organization (and even within groups). 

We saw some pretty bad practices like the hard-coding of parameters within scripts, functions, modules, ... e.g.:

```python
def my_function(args):
    my_parameter = 10
    # do something with my_parameter
    ...
```

Not only is this just bad practice but it is also not reproducible (your parameters become dependent on branch and 
commit) and really isn't helpful for a collaborative codebase. Additionally, it and makes monitoring, re-training, 
and/or deployment a nightmare. 

We saw a lot of colleagues taking an easy way out e.g.:

```python
### in config.py ###
PARAMETER_1 = 10
PARAMETER_2 = 'relu'

### in function.py ###
from config import *

def my_function(arg_1 = PARAMETER_1):
  # do something with arg_1
  ...
```
 
Almost just as bad of practice as above but at least self-contained. It still is hard to reproduce and code and
and parameters are still just as intertwined.

Those who tried some configuration/parameter management resorted to re-implementing the same boilerplate code e.g.:

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--foo', help='foo help')
args = parser.parse_args()
```

Better practice to bring parameters in from the command line (or even an external INI file using configparser) but
the amount of boilerplate is high and it's pretty tedious to manage more than 10+ parameters.

On top of all of this, most parameter definitions were *mutable* meaning that they can be changed within code blocks (on 
purpose or by accident) leading to dangerous and unexpected behavior. 

#### What Does spock Do To Resolve These Observations?

Thus, the idea of of `spock` was born... A simple, understandable, and lightweight library to manage complex parameter 
configurations during Python development. Anyone familiar with Python and knows how to define a basic class object can 
use `spock` (or if they don't there is plenty of documentation and tutorials on classes).

### Other Libraries

There are other open source complex configuration libraries available for Python. We think that `spock` fits
within this space by providing a simple and lightweight configuration management library in comparison to other 
libraries. The main two that fill a similar role as `spock` are:

#### [gin-config](https://github.com/google/gin-config)
> Provides a lightweight configuration framework for Python, based on dependency injection

`gin-config` does a lot of things and does them pretty well. However, we found that `gin-config`'s dependency 
injection and heavy use of decorators just didn't fit what we wanted. Dynamic injection provides a less verbose
configuration solution, but can lack reproducibility depending on where and how parameters are defined. In addition, 
the pretty large 'kitchen sink' of different ways to manage configurations isn't simple nor lightweight enough of a 
solution.

#### [Hydra](https://github.com/facebookresearch/hydra)
> A framework for elegantly configuring complex applications

At the time we started building `spock` Hydra wasn't available. Hydra is similar to `spock` but is more restrictive in 
its functionality and syntax. Similar to `gin-config` parameters are dynamically injected via a decorator which limits
type checking, reproducibility, and traceability. In addition, `Hydra` doesn't support inheritance which was a big
motivator for creating a new solution.
