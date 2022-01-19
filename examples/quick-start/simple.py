from typing import List

from spock import SpockBuilder
from spock import spock


@spock
class BasicConfig:
    """Basic spock configuration for example purposes

    Attributes:
        parameter: simple boolean that flags rounding
        fancy_parameter: parameter that multiplies a value
        fancier_parameter: parameter that gets added to product of val and fancy_parameter
        most_fancy_parameter: values to apply basic algebra to

    """

    parameter: bool
    fancy_parameter: float
    fancier_parameter: float
    most_fancy_parameter: List[int]


def add_namespace(config):
    # Lets just do some basic algebra here
    val_sum = sum(
        [
            (config.fancy_parameter * val) + config.fancier_parameter
            for val in config.most_fancy_parameter
        ]
    )
    # If the boolean is true let's round
    if config.parameter:
        val_sum = round(val_sum)
    return val_sum


def add_by_parameter(multiply_param, list_vals, add_param, tf_round):
    # Lets just do some basic algebra here
    val_sum = sum([(multiply_param * val) + add_param for val in list_vals])
    # If the boolean is true let's round
    if tf_round:
        val_sum = round(val_sum)
    return val_sum


def main():
    # Chain the generate function to the class call
    config = SpockBuilder(BasicConfig, desc="Quick start example").generate()
    # One can now access the Spock config object by class name with the returned namespace
    print(config.BasicConfig.parameter)
    # And pass the namespace to our first function
    val_sum_namespace = add_namespace(config.BasicConfig)
    print(val_sum_namespace)
    # Or pass by parameter
    val_sum_parameter = add_by_parameter(
        config.BasicConfig.fancy_parameter,
        config.BasicConfig.most_fancy_parameter,
        config.BasicConfig.fancier_parameter,
        config.BasicConfig.parameter,
    )
    print(val_sum_parameter)


if __name__ == "__main__":
    main()
