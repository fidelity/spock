# -*- coding: utf-8 -*-

"""A simple example using sklearn and Ax support"""

# Spock ONLY supports the service style API from Ax
# https://ax.dev/docs/api.html


from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from spock.addons.tune import (
    ChoiceHyperParameter,
    AxTunerConfig,
    RangeHyperParameter,
    spockTuner,
)
from spock.builder import ConfigArgBuilder
from spock.config import spock


@spock
class BasicParams:
    n_trials: int
    max_iter: int


@spockTuner
class LogisticRegressionHP:
    c: RangeHyperParameter
    solver: ChoiceHyperParameter


def main():
    # Load the iris data
    X, y = load_iris(return_X_y=True)

    # Split the Iris data
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    # Optuna config -- this will internally spawn the study object for the define-and-run style which will be returned
    # by accessing the tuner_status property on the ConfigArgBuilder object
    ax_config = AxTunerConfig(
        objective_name='accuracy',
        minimize=False
    )

    # Use the builder to setup
    # Call tuner to indicate that we are going to do some HP tuning -- passing in an optuna study object
    attrs_obj = (
        ConfigArgBuilder(
            LogisticRegressionHP,
            BasicParams,
            desc="Example Logistic Regression Hyper-Parameter Tuning -- Ax Backend",
        )
        .tuner(tuner_config=ax_config)
        .save(user_specified_path="/tmp/ax")
    )

    # Here we need some of the fixed parameters first so we can just call the generate fnc to grab all the fixed params
    # prior to starting the sampling process
    fixed_params = attrs_obj.generate()

    # Now we iterate through a bunch of optuna trials
    for _ in range(fixed_params.BasicParams.n_trials):
        # The crux of spock support -- call save w/ the add_tuner_sample flag to write the current draw to file and
        # then call sample to return the composed Spockspace of the fixed parameters and the sampled parameters
        # Under the hood spock uses the define-and-run Optuna interface -- thus it handled the underlying 'ask' call
        # and returns the necessary trial object in the return dictionary to call 'tell' with the study object
        hp_attrs = attrs_obj.save(
            add_tuner_sample=True, user_specified_path="/tmp/ax"
        ).sample()
        # Use the currently sampled parameters in a simple LogisticRegression from sklearn
        clf = LogisticRegression(
            C=hp_attrs.LogisticRegressionHP.c,
            solver=hp_attrs.LogisticRegressionHP.solver,
            max_iter=hp_attrs.BasicParams.max_iter,
        )
        clf.fit(X_train, y_train)
        val_acc = clf.score(X_valid, y_valid)
        # Get the status of the tuner -- this dict will contain all the objects needed to update
        tuner_status = attrs_obj.tuner_status
        # Pull the study and trials object out of the return dictionary and pass it to the tell call using the study
        # object
        tuner_status['client'].complete_trial(
            trial_index=tuner_status['trial_index'],
            raw_data={'accuracy': (val_acc, 0.0)}
        )
        # Always save the current best set of hyper-parameters
        attrs_obj.save_best(user_specified_path="/tmp/ax")

    # Grab the best config and metric
    best_config, best_metric = attrs_obj.best
    print(f"Best HP Config:\n{best_config}")
    print(f"Best Metric: {best_metric}")


if __name__ == "__main__":
    main()
