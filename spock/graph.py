# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles creation and ops for DAGs"""

import sys
from typing import Type

from spock.utils import _find_all_spock_classes


class Graph:
    """Class that holds graph methods for determining dependencies between spock classes

    Attributes:
        _input_classes: list of input classes that link to a backend
        _dag: graph of the dependencies between spock classes
        _lazy: attempts to lazily find @spock decorated classes registered within sys.modules["spock"].backend.config

    """

    def __init__(self, input_classes, lazy: bool):
        """Init call for Graph class

        Args:
            input_classes: list of input classes that link to a backend
            lazy: attempts to lazily find @spock decorated classes registered within sys.modules["spock"].backend.config
        """
        self._input_classes = input_classes
        self._lazy = lazy
        # Maybe find classes lazily -- roll them into the input class tuple
        # make sure to cast as a set first since the lazy search might find duplicate references
        if self._lazy:
            # Lazily find base classes
            self._input_classes = (
                *self._input_classes,
                *set(self._lazily_find_classes(self._input_classes)),
            )
            # Lazily find any parents that are missing
            self._input_classes = (
                *self._input_classes,
                *set(self._lazily_find_parents()),
            )
        # Build -- post lazy eval
        self._dag = self._build()
        # Validate (No cycles in DAG)
        if self._has_cycles() is True:
            raise ValueError(
                "Cycle detected within the spock class dependency DAG...\n"
                "Please correct your @spock decorated classes by removing any cyclic references"
            )

    @property
    def dag(self):
        """Returns the DAG"""
        return self._dag

    @property
    def nodes(self):
        """Returns the input_classes/nodes"""
        return self._input_classes

    @property
    def node_names(self):
        """Returns the node names"""
        return {f"{k.__name__}" for k in self.nodes}

    @property
    def node_map(self):
        return {f"{k.__name__}": k for k in self.nodes}

    @property
    def roots(self):
        """Returns the roots of the dependency graph"""
        return [self.node_map[k] for k, v in self.dag.items() if len(v) == 0]

    @property
    def topological_order(self):
        return self._topological_sort()

    @staticmethod
    def _yield_class_deps(classes):
        """Generator to iterate through nodes and find dependencies

        Args:
            classes: list of classes to iterate through

        Yields:
            tuple or the base input class and the current name of the dependent class

        """
        for input_class in classes:
            dep_names = {f"{v.__name__}" for v in _find_all_spock_classes(input_class)}
            for v in dep_names:
                yield input_class, v

    def _lazily_find_classes(self, classes):
        """Searches within the spock sys modules attributes to lazily find @spock decorated classes

        These classes have been decorated with @spock but might not have been passes into the ConfigArgBuilder so
        this allows for 'lazy' lookup of these classes to make the call to ConfigArgBuilder a little less verbose
        when there are a lot of spock classes

        Returns:
            tuple of any lazily discovered classes

        """
        # Iterate thorough all of the base spock classes to get the dependencies and reverse dependencies
        lazy_classes = []
        for _, v in self._yield_class_deps(classes):
            if (
                hasattr(sys.modules["spock"].backend.config, v)
                and getattr(sys.modules["spock"].backend.config, v) not in classes
            ):
                print(
                    f"Lazy evaluation found a @spock decorated class named `{v}` within the registered types of "
                    f"sys.modules['spock'].backend.config -- Attempting to use the class "
                    f"`{getattr(sys.modules['spock'].backend.config, v)}` within the SpockBuilder"
                )
                # Get the lazily discovered class
                lazy_class = getattr(sys.modules["spock"].backend.config, v)
                # Recursive check the lazy class for other lazy classes
                dependent_lazy_classes = self._lazily_find_classes([lazy_class])
                # extend the list if the recursive check finds any other lazy classes
                if len(dependent_lazy_classes) > 0:
                    lazy_classes.extend(dependent_lazy_classes)
                lazy_classes.append(lazy_class)
        return tuple(lazy_classes)

    def _lazily_find_parents(self):
        """Searches within the current set of input_classes (@spock decorated classes) to lazily find any parents

        Given that lazy inheritance means that the parent classes won't be included (since they are cast to spock
        classes within the decorator and the MRO is handled internally) this allows the lazy flag to find those parent
        classes and add them to the SpockBuilder *args (input classes).

        Returns:
            tuple of any lazily discovered classes

        """
        lazy_parents = {}
        for v in self._input_classes:
            # Check if the MRO is long enough to have bases
            if len(v.__mro__[1:-1]) > 0:
                bases = list(v.__mro__[1:-1])
                for base in bases:
                    cls_name = base.__name__
                    if (cls_name not in self.node_names) and (
                        cls_name not in lazy_parents.keys()
                    ):
                        print(
                            f"Lazy evaluation found a @spock decorated parent class named `{cls_name}` within the "
                            f"registered types of sys.modules['spock'].backend.config -- Appending the class "
                            f"`{getattr(sys.modules['spock'].backend.config, cls_name)}` to the SpockBuilder..."
                        )
                        lazy_parents.update({base.__name__: base})
        return tuple(lazy_parents.values())

    def _build(self):
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            dictionary of nodes and their edges

        """
        # Build a dictionary of all nodes (base spock classes)
        nodes = {val: [] for val in self.node_names}
        # Iterate thorough all of the base spock classes to get the dependencies and reverse dependencies
        for input_class, v in self._yield_class_deps(self._input_classes):
            if v not in self.node_names:
                raise ValueError(
                    f"Missing @spock decorated class -- `{v}` was not passed as an *arg to "
                    f"ConfigArgBuilder and/or could not be found via lazy evaluation (currently lazy=`{self._lazy}`) "
                    f"within sys.modules['spock'].backend.config"
                )
            nodes.get(v).append(input_class)
        nodes = {key: set(val) for key, val in nodes.items()}
        return nodes

    def _has_cycles(self):
        """Uses DFS to check for cycles within the spock dependency graph

        Returns:
            boolean if a cycle is found

        """
        # DFS w/ recursion stack for DAG cycle detection
        visited = {key: False for key in self.dag.keys()}
        all_nodes = list(visited.keys())
        recursion_stack = {key: False for key in self.dag.keys()}
        # Recur for all edges
        for node in all_nodes:
            if visited.get(node) is False:
                # Surface the recursive checks
                if self._cycle_dfs(node, visited, recursion_stack) is True:
                    return True
        return False

    def _cycle_dfs(self, node: Type, visited: dict, recursion_stack: dict):
        """DFS via a recursion stack for cycles

        Args:
            node: current graph node (spock class type)
            visited: dictionary of visited nodes
            recursion_stack: dictionary that is the recursion stack that is used to find cycles

        Returns:
            boolean if a cycle is found

        """
        # Update the visited nodes
        visited.update({node: True})
        # Update recursion stack
        recursion_stack.update({node: True})
        # Recur through the edges
        for val in self.dag.get(node):
            if visited.get(val) is False:
                # The the recursion returns True then work it up the stack
                if self._cycle_dfs(val, visited, recursion_stack) is True:
                    return True
            # If the vertex is already in the recursion stack then we have a cycle
            elif recursion_stack.get(val) is True:
                return True
        # Reset the stack for the current node if we've completed the DFS from this node
        recursion_stack.update({node: False})
        return False

    def _topological_sort(self):
        # DFS for topological sort
        # https://en.wikipedia.org/wiki/Topological_sorting
        visited = {key: False for key in self.node_names}
        all_nodes = list(visited.keys())
        stack = []
        for node in all_nodes:
            if visited.get(node) is False:
                self._topological_sort_dfs(node, visited, stack)
        stack.reverse()
        return stack

    def _topological_sort_dfs(self, node, visited, stack):
        # Update the visited dict
        visited.update({node: True})
        # Recur for all edges
        for val in self._dag.get(node):
            if visited.get(val.__name__) is False:
                self._topological_sort_dfs(val.__name__, visited, stack)
        stack.append(node)
