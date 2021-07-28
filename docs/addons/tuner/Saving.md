# Saving Hyper-Parameter Configs -- Base, Samples, and Best

`spock` provides the capability to save the configuration for each stage of hyper-parameter tuning.

### Saving Base Hyper-Parameter Definitions

First, if we wanted to save the configuration state of the defined hyper-parameter ranges (i.e. the definitions of the 
parameters that are not sampled) we simply chain the `save()` call post `tuner()` call just like we did with basic 
`spock` usage. If there are defined hyper-parameters from `@spockTuner` these will automatically get written into the 
markdown file along with the fixed parameters.

For instance in `tune.py`:

```python

# Chain the .save call which will dump the hyper-parameter definitions to the configuration file
attrs_obj = ConfigArgBuilder(
        LogisticRegressionHP,
        BasicParams,
        desc="Example Logistic Regression Hyper-Parameter Tuning",
).tuner(tuner_config=optuna_config).save(user_specified_path='/tmp')
```

Would result in the following YAML file:

```yaml
 BasicParams:
   max_iter: 150
   n_trials: 10
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

### Saving Individual Hyper-Parameter Samples

If we want to save each individual hyper-parameter sample we again use the `save()` call with the addition of the 
`add_tuner_sample=True` keyword arg and chain it before the`sample()` call. The order might be slightly confusing 
but this is to allow all methods to return the builder object except for hte `sample()` and `generate()` calls 
which returns a `Spockspace`. The saver will append `hp.sample.[0-9+]` to the filename to identify each sample 
configuration.

For instance in `tune.py`:

```python

# Now we iterate through a bunch of optuna trials
for _ in range(fixed_params.BasicParams.n_trials):
    hp_attrs = attrs_obj.save(
        add_tuner_sample=True, user_specified_path="/tmp"
    ).sample()
```

Would result in `n_trials` files named `hp.sample.[0-9]+.{uuid}.spock.cfg`. For instance opening a file named
`hp.sample.1.d1cc7a30-10f0-4d2c-b076-513fe3494566.spock.cfg.yaml` we would see the first sample set of the 
hyper-parameters:

```yaml
 BasicParams:
   max_iter: 150
   n_trials: 10
 LogisticRegressionHP:
   c: 0.21495978453310358
   solver: lbfgs
```

### Saving the Best Hyper-Parameter Samples

If we want to keep track of the current/final best hyper-parameter set based on the optimization metric we use the
`save_best()` call on the builder object. This function takes all the same arguments as the `save()` method but
maintains only a single configuration file that is the current/final best hyper-parameter configuration. The saver will 
append `hp.best.` to the filename to identify the best configuration. Note: Make sure this function is only called post
all backend handling (in the case of Optuna -- the 'tell' call) for the sample or else an exception will be raised as
the best configuration will not yet be registered.

For instance in `tune.py`:

```python
# Now we iterate through a bunch of optuna trials
for _ in range(fixed_params.BasicParams.n_trials):
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
    # Always save the current best set of hyper-parameters
    attrs_obj.save_best(user_specified_path='/tmp')
```