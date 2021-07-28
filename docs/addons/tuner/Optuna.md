# Optuna Support

`spock` integrates with the Optuna hyper-parameter optimization framework through the provided
ask-and-run interface and the define-and-run API. See [docs](https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html#define-and-run).

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

### Defining the Backend

So let's continue in our Optuna specific version of `tune.py`:

It's important to note that you can still use the `@spock` decorator to define any non hyper-parameters! For 
posterity let's add some fixed parameters (those that are not part of hyper-parameter tuning) that we will use
elsewhere in our code. 

```python
from spock.config import spock

@spock
class BasicParams:
    n_trials: int
    max_iter: int
```

Now we need to tell `spock` that we intend on doing hyper-parameter tuning and which backend we would like to use. We
do this by calling the `tuner` method on the `ConfigArgBuilder` object passing in a configuration object for the
backend of choice (just like in basic functionality this is a chained command, thus the builder object will still be 
returned). For Optuna one uses `OptunaTunerConfig`. This config mirrors all options that would be passed into 
the `optuna.study.create_study` function call so that `spock` can setup the define-and-run API. (Note: The `@spockTuner` 
decorated classes are passed to the `ConfigArgBuilder` in the exact same way as basic `@spock` 
decorated classes.)

```python
from spock.addons.tune import OptunaTunerConfig

# Optuna config -- this will internally configure the study object for the define-and-run style which will be returned
# by accessing the tuner_status property on the ConfigArgBuilder object
optuna_config = OptunaTunerConfig(
    study_name="Iris Logistic Regression", direction="maximize"
)

# Use the builder to setup
# Call tuner to indicate that we are going to do some HP tuning -- passing in an optuna study object
attrs_obj = ConfigArgBuilder(
    LogisticRegressionHP,
    BasicParams,
    desc="Example Logistic Regression Hyper-Parameter Tuning",
).tuner(tuner_config=optuna_config)

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
useable parameters (defined with dot notation). For Optuna -- Under the hood `spock` uses the define-and-run Optuna 
interface -- thus it handles the underlying 'ask' call. The `spock` builder object has a `@property` called 
`tuner_status` that returns any necessary backend objects in a dictionary that the user needs to interface with. In the 
case of Optuna, this contains both the Optuna `study` and `trial` (as dictionary keys). We use the return of 
`tuner_status` to handle the 'tell' call based on the metric of interested (here just simple validation accuracy)

Continuing in `tune.py`:

```python
# Iterate through a bunch of optuna trials
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
        # Pull the study and trials object out of the return dictionary and pass it to the tell call using the study
        # object
        tuner_status["study"].tell(tuner_status["trial"], val_acc)
```