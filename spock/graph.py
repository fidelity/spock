# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles creation and ops for DAGs"""

from typing import Type

import attr

from spock.utils import _find_all_spock_classes


class Graph:
    """Class that holds graph methods for determining dependencies between spock classes

    Attributes:
        _input_classes: list of input classes that link to a backend
        _dag: graph of the dependencies between spock classes

    """

    def __init__(self, input_classes):
        """Init call for Graph class

        Args:
            input_classes: list of input classes that link to a backend
        """
        self._input_classes = input_classes
        # Build
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

    def _build(self):
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            dictionary of nodes and their edges

        """
        # Build a dictionary of all nodes (base spock classes)
        nodes = {val: [] for val in self.node_names}
        # Iterate thorough all of the base spock classes to get the dependencies and reverse dependencies
        for input_class in self.nodes:
            dep_names = {f"{v.__name__}" for v in _find_all_spock_classes(input_class)}
            for v in dep_names:
                if v not in self.node_names:
                    raise ValueError(
                        f"Missing @spock decorated class -- `{v}` was not passed as an *arg to "
                        f"ConfigArgBuilder"
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
