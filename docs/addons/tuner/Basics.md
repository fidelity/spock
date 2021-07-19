# Tune Basics

Just like the basic `spock` functionality, hyper-parameters are defined via a class based solution. All parameters 
must be defined in a class or multiple classes by decorating with the `@spockTuner` decorator. Parameters are defined 
as one of the two basic types, `RangeHyperParameter` or `ChoiceHyperParameter`. 

Once built (with a specific backend), all parameters can be found within an automatically generated namespace 
object that contains both the fixed and sampled parameters that can be accessed with the given `@spock` or 
`@spockTuner` class names.

### Supported Hyper-Parameter Types
`spock` supports the two following types for hyper-parameters, `RangeHyperParameter` or `ChoiceHyperParameter`.

The `RangeHyperParameter` type is used for hyper-parameters that are to be drawn from a sampled range of `int` or 
`float` while the `ChoiceHyperParameter` type is used for hyper-parameters that are to be sampled from a discrete set 
of values that can be of base type `int`, `float`, `bool`, or `str`.

`RangeHyperParameter` requires the following inputs:
* type: string of either int or float depending on the needed type
* bounds: a tuple of two values that define the lower and upper bound of the range (int or float)
* log_scale: boolean to activate log scaling of the range

`ChoiceHyperParameter` requires the following inputs:
* type: string of either int, float, bool, str depending on the needed type
* choices: a list of any length that contains the discrete values to sample from

### Defining a spockTuner Class

Let's start building out a very simple example (logistic regression of iris w/ sklearn) that we will continue to use 
within the tutorial: `tune.py`

Tune functions exactly the same as base `spock` functionality. We import the basic units of functionality 
from `spock.addons.tune`, define our class using the `@spockTuner` decorator, and define our parameters with 
supported argument types. We also pull in the sample iris data from sklearn.

```python
from spock.addons.tune import ChoiceHyperParameter
from spock.addons.tune import RangeHyperParameter
from spock.addons.tune import spockTuner
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


@spockTuner
class LogisticRegressionHP:
    c: RangeHyperParameter
    solver: ChoiceHyperParameter

# Load the iris data
X, y = load_iris(return_X_y=True)

# Split the Iris data
X_train, X_valid, y_train, y_valid = train_test_split(X, y)

```

The `@spockTuner` decorated classes are passed to the `ConfigArgBuilder` in the exact same way as basic `@spock` 
decorated classes. This returns a `spock` builder object which can be used to call different methods.

```python
attrs_obj = ConfigArgBuilder(
    LogisticRegressionHP,
    desc="Example Logistic Regression Hyper-Parameter Tuning",
)
```


### Creating a Configuration File

Just like basic spock functionality, values in `spock` are set primarily using external configuration files. For our
hyper-parameters we just defined above our `tune.yaml` file might look something like this (remember each class requires
specific inputs):

```yaml
# Hyper-parameter config
LogisticRegressionHP:
  c:
    bounds:
    - 0.01
    - 10.0
    log_scale: true
    type: float
  solver:
    choices:
    - lbfgs
    - saga
    type: str
```


### Continuing

The rest of the docs are backend specific so refer to the correct backend specific documentation.