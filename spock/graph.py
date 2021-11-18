# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles creation and ops for DAGs"""

import attr
from copy import deepcopy
from spock.utils import _is_spock_instance, _check_iterable
from enum import EnumMeta


class Graph(object):
    def __init__(self, input_classes):
        self._input_classes = input_classes
        # Build
        self._class_dag, self._dep_dag = self._build()
        # Sort
        self._class_order = self._topological_sort()
        # Validate (No cycles in DAG)
        if self._check_for_cycles() is True:
            raise ValueError('Cycle detected within the spock class dependency DAG...\n'
                             'Please correct your @spock decorated classes by removing any cyclic references')

    def __call__(self, *args, **kwargs):
        return Graph(*args, **kwargs)

    @property
    def class_order(self):
        return self._class_order

    def _build(self):
        # Build a dictionary of all nodes (base spock classes)
        nodes = {val.__name__: [] for val in self._input_classes}
        # Deep copy for the dependency nodes (reverse direction)
        dep_nodes = deepcopy(nodes)
        # Iterate thorough all of the base spock classes to get the dependencies and reverse dependencies
        for input_class in self._input_classes:
            dep_classes = self._find_all_spock_classes(input_class)
            # Dependency nodes
            dep_nodes.get(input_class.__name__).extend(dep_classes)
            for v in dep_classes:
                nodes.get(v).append(input_class.__name__)
        nodes = {key: set(val) for key, val in nodes.items()}
        dep_nodes = {key: set(val) for key, val in dep_nodes.items()}
        return nodes, dep_nodes

    def _find_all_spock_classes(self, attr_class):
        # Get the top level dict
        dict_attr = attr.fields_dict(attr_class)
        # Dependent classes
        dep_classes = []
        for k, v in dict_attr.items():
            # Checks for direct spock/attrs instance
            if _is_spock_instance(v.type):
                dep_classes.append(v.type.__name__)
            # Check for enum of spock/attrs instance
            elif isinstance(v.type, EnumMeta) and self._check_4_spock_iterable(v.type):
                dep_classes.extend(self._get_enum_classes(v.type))
            # Check for List[@spock-class]
            elif v.type.__name__ == 'list' and _is_spock_instance(v.metadata["type"].__args__[0]):
                dep_classes.append(v.metadata["type"].__args__[0].__name__)
        return dep_classes

    @staticmethod
    def _check_4_spock_iterable(iter_obj):
        return _check_iterable(iter_obj=iter_obj)

    @staticmethod
    def _get_enum_classes(enum_obj):
        return [v.value.__name__ for v in enum_obj if _is_spock_instance(v.value)]

    @staticmethod
    def _get_list_classes(enum_obj):
        return [v.__name__ for v in enum_obj if _is_spock_instance(v)]

    def _check_for_cycles(self):
        # DFS w/ recursion stack for DAG cycle detection
        visited = {key: False for key in self._class_dag.keys()}
        all_nodes = list(visited.keys())
        recursion_stack = {key: False for key in self._class_dag.keys()}
        # Recur for all edges
        for node in all_nodes:
            if visited.get(node) is False:
                # Surface the recursive checks
                if self._cycle_dfs(node, visited, recursion_stack) is True:
                    return True
        return False

    def _topological_sort(self):
        # DFS for topological sort
        # https://en.wikipedia.org/wiki/Topological_sorting
        visited = {key: False for key in self._class_dag.keys()}
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
        for val in self._class_dag.get(node):
            if visited.get(val) is False:
                self._topological_sort_dfs(val, visited, stack)
        stack.append(node)

    def _cycle_dfs(self, node, visited, recursion_stack):
        # Update the visited nodes
        visited.update({node: True})
        # Update recursion stack
        recursion_stack.update({node: True})
        # Recur through the edges
        for val in self._class_dag.get(node):
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
