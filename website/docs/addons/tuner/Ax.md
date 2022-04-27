# Ax Support

`spock` integrates with the Ax optimization framework through the provided Service API. See 
[docs](https://ax.dev/api/service.html#module-ax.service.ax_client) for `AxClient` info.

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

### Defining the Backend

So let's continue with our Ax specific version of `tune.py`:

It's important to note that you can still use the `@spock` decorator to define any non hyper-parameters! For 
posterity let's add some fixed parameters (those that are not part of hyper-parameter tuning) that we will use
elsewhere in our code. 

```python
from spock import spock

from spock.addons.tune import (
    ChoiceHyperParameter,
    RangeHyperParameter,
    spockTuner,
)

@spock
class BasicParams:
    n_trials: int
    max_iter: int


@spockTuner
class LogisticRegressionHP:
    c: RangeHyperParameter
    solver: ChoiceHyperParameter
```

Now we need to tell `spock` that we intend on doing hyper-parameter tuning and which backend we would like to use. We
do this by calling the `tuner` method on the `SpockBuilder` object passing in a configuration object for the
backend of choice (just like in basic functionality this is a chained command, thus the builder object will still be 
returned). For Ax one uses `AxTunerConfig`. This config mirrors all options that would be passed into 
the `AxClient` constructor and the `AxClient.create_experiment`function call so that `spock` can setup the 
Service API. (Note: The `@spockTuner`decorated classes are passed to the `SpockBuilder` in the exact same 
way as basic `@spock`decorated classes.)

```python
from spock import SpockBuilder
from spock.addons.tune import AxTunerConfig

# Ax config -- this will internally spawn the AxClient service API style which will be returned
# by accessing the tuner_status property on the SpockBuilder object -- note here that we need to define the
# objective name that the client will expect to be within the data dictionary when completing trials 
ax_config = AxTunerConfig(objective_name="accuracy", minimize=False)

# Use the builder to setup
# Call tuner to indicate that we are going to do some HP tuning -- passing in an ax study object
attrs_obj = SpockBuilder(
    LogisticRegressionHP,
    BasicParams,
    desc="Example Logistic Regression Hyper-Parameter Tuning -- Ax Backend",
).tuner(tuner_config=ax_config)

```

### Generate Functionality Still Exists

To get the set of fixed parameters (those that are not hyper-parameters) one simply calls the `generate()` function
just like they would for normal `spock` usage to get the fixed parameter `spockspace`. 

Continuing in `tune.py`:

```python

# Here we need some of the fixed parameters first so we can just call the generate fnc to grab all the fixed params
# prior to starting the sampling process
fixed_params = attrs_obj.generate()
```

### Sample as an Alternative to Generate

The `sample()` call is the crux of `spock` hyper-parameter tuning support. It draws a hyper-parameter sample from the 
underlying backend sampler and combines it with fixed parameters and returns a single `Spockspace` with all 
usable parameters (defined with dot notation). For Ax -- Under the hood `spock` uses the Service API (with 
an `AxClient`) -- thus it handles the underlying call to get the next trial. The `spock` builder object has a 
`@property` called `tuner_status` that returns any necessary backend objects in a dictionary that the user needs to 
interface with. In the case of Ax, this contains both the `AxClient` and `trial_index` (as dictionary keys). We use 
the return of`tuner_status` to handle trial completion via the `complete_trial` call based on the metric of interested 
(here just the simple validation accuracy -- remember during `AxTunerConfig` instantiation we set the `objective_name`
to 'accuracy' -- we also set the SEM to 0.0 since we are not using it for this example)

See [here](https://ax.dev/api/service.html#ax.service.ax_client.AxClient.complete_trial) for Ax documentation on
completing trials.

Continuing in `tune.py`:

```python
# Iterate through a bunch of ax trials
for _ in range(fixed_params.BasicParams.n_trials):
        # Call sample on the spock object 
        hp_attrs = attrs_obj.sample()
        # Use the currently sampled parameters in a simple LogisticRegression from sklearn
        clf = LogisticRegression(
            C=hp_attrs.LogisticRegressionHP.c,
            solver=hp_attrs.LogisticRegressionHP.solver,
            max_iter=hp_attrs.BasicParams.max_iter
        )
        clf.fit(X_train, y_train)
        val_acc = clf.score(X_valid, y_valid)
        # Get the status of the tuner -- this dict will contain all the objects needed to update
        tuner_status = attrs_obj.tuner_status
        # Pull the AxClient object and trial index out of the return dictionary and call 'complete_trial' on the
        # AxClient object with the correct raw_data that contains the objective name
        tuner_status["client"].complete_trial(
            trial_index=tuner_status["trial_index"],
            raw_data={"accuracy": (val_acc, 0.0)},
        )
```