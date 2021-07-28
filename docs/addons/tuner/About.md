# Hyper-Parameter Tuning Support

This series of docs will describe the basics of hyper-parameter support within `spock`. `spock` tries to be as hands-off 
as possible with the underlying backends that support hyper-parameter tuning and only provide a common and simplified
interface to define hyper-parameter tuning runs. The rest is left up to the user to define and handle, thus to not
handcuff the user into too simplified functionality.

All examples can be found [here](https://github.com/fidelity/spock/blob/master/examples).

### Installing

Install `spock` with the extra hyper-parameter tuning related dependencies.

```bash
pip install spock-config[tune]
```

### Supported Backends
* [Optuna](https://optuna.readthedocs.io/en/stable/index.html)

### WIP/Planned Backends
* [Ax](https://ax.dev/)