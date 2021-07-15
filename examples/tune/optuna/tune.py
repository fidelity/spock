# -*- coding: utf-8 -*-

"""A simple example using sklearn and Optuna support"""

# Spock ONLY supports the define-and-run style interface from Optuna
# https://optuna.readthedocs.io/en/stable/tutorial/20_recipes/009_ask_and_tell.html#define-and-run


from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from spock.addons.tune import spockTuner
from spock.addons.tune import (
    ChoiceHyperParameter,
    OptunaTunerConfig,
    RangeHyperParameter,
)
from spock.builder import ConfigArgBuilder
from spock.config import spock


@spock
class BasicParams:
    n_trials: int


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
    # as part of the call to sample()
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

    # Here we need some of the fixed parameters first so we can just call the generate fnc to grab all the fixed params
    # prior to starting the sampling process
    fixed_params = attrs_obj.generate()

    # Now we iterate through a bunch of optuna trials
    for _ in range(fixed_params.BasicParams.n_trials):
        # The crux of spock support -- call save w/ the add_tuner_sample flag to write the current draw to file and
        # then call save to return the composed Spockspace of the fixed parameters and the sampled parameters
        # Under the hood spock uses the define-and-run Optuna interface -- thus it handled the underlying 'ask' call
        # and returns the necessary trial object in the return dictionary to call 'tell' with the study object
        hp_attrs = attrs_obj.save(
            add_tuner_sample=True, user_specified_path="/tmp"
        ).sample()
        # Use the currently sampled parameters in a simple LogisticRegression from sklearn
        clf = LogisticRegression(
            C=hp_attrs.LogisticRegressionHP.c,
            solver=hp_attrs.LogisticRegressionHP.solver,
        )
        clf.fit(X_train, y_train)
        val_acc = clf.score(X_valid, y_valid)
        # Get the status of the tuner -- this dict will contain all the objects needed to update
        tuner_status = attrs_obj.tuner_status
        # Pull the study and trials object out of the return dictionary and pass it to the tell call using the study
        # object
        tuner_status["study"].tell(tuner_status["trial"], val_acc)
        print('hi')


if __name__ == "__main__":
    main()
