# Run

In summary, we have constructed the four basic pieces of `spock`.

1. A `spock` class that defines our parameters (Basics)
2. Generated the `spock` namespace object (Building)
3. Referenced `spock` parameters in other code (Building)
4. Created a configuration file (Configuration Files)

Now we can run our basic neural network example.

### Running Our Code

To run `tutorial.py` we pass the path to the configuration file as a command line argument:

```shell
python tutorial.py --config tutorial.yaml
```

### Help

To get help for parameters need to run our `tutorial.py` script:

```shell
python tutorial.py --help
```



The complete basic example can be found [here](https://github.com/fidelity/spock/blob/master/examples).