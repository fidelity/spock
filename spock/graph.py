# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Handles creation and ops for DAGs"""

import sys
from abc import ABC, abstractmethod, abstractproperty
from typing import Dict, Generator, List, Set, Tuple, Union

from spock.backend.resolvers import VarResolver
from spock.exceptions import _SpockInstantiationError, _SpockVarResolverError
from spock.utils import _C, _find_all_spock_classes


class BaseGraph(ABC):
    """Class that holds graph methods

    Attributes:
        _dag: graph of the dependencies between spock classes
    """

    def __init__(self, dag: Dict, whoami: str):
        """Init call for Graph class

        Args:
            dag: a directed acyclic graph as a dictionary (keys -> nodes, values -> edges)
            whoami: str value of whom the caller is
        """
        self._dag = dag
        self._whoami = whoami
        # Validate (No cycles in DAG)
        if self._has_cycles() is True:
            raise _SpockInstantiationError(
                f"Cycle detected within the constructed DAG from {self._whoami} - "
                f"Please remove any cyclic references. DAG Dictionary {{Node: Edges}} "
                f"`{self.dag}`"
            )

    @property
    def dag(self):
        """Returns the DAG"""
        return self._dag

    @property
    @abstractmethod
    def nodes(self):
        """Returns the nodes"""
        pass

    @property
    def node_names(self):
        """Returns the node names"""
        return {f"{k.__name__}" for k in self.nodes}

    @property
    def node_map(self):
        """Returns a map of the node names to the underlying classes"""
        return {f"{k.__name__}": k for k in self.nodes}

    @property
    def reverse_map(self):
        """Returns a map from the underlying classes to the node names"""
        return {k: f"{k.__name__}" for k in self.nodes}

    @property
    def roots(self):
        """Returns the roots of the dependency graph"""
        return [self.node_map[k] for k, v in self.dag.items() if len(v) == 0]

    @property
    def topological_order(self):
        """Returns the topological sort of the DAG"""
        return self._topological_sort()

    @abstractmethod
    def _build(self) -> Dict:
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            dictionary of nodes and their edges

        """
        pass

    def _has_cycles(self) -> bool:
        """Uses DFS to check for cycles within the given graph

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

    def _cycle_dfs(self, node: str, visited: Dict, recursion_stack: Dict) -> bool:
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
            if visited.get(self.reverse_map[val]) is False:
                # The recursion returns True then works it up the stack
                if (
                    self._cycle_dfs(self.reverse_map[val], visited, recursion_stack)
                    is True
                ):
                    return True
            # If the vertex is already in the recursion stack then we have a cycle
            elif recursion_stack.get(self.reverse_map[val]) is True:
                return True
        # Reset the stack for the current node if we've completed the DFS from this node
        recursion_stack.update({node: False})
        return False

    def _topological_sort(self) -> List:
        """Topologically sorts the DAG

        Returns:
            list of topological order

        """
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

    def _topological_sort_dfs(self, node: str, visited: Dict, stack: List) -> None:
        """Depth first search

        Args:
            node: current node
            visited: visited nodes
            stack: order of graph

        Returns:

        """
        # Update the visited dict
        visited.update({node: True})
        # Recur for all edges
        for val in self._dag.get(node):
            val_name = val.__name__ if hasattr(val, "__name__") else val
            if visited.get(val_name) is False:
                self._topological_sort_dfs(val_name, visited, stack)
        stack.append(node)


class MergeGraph(BaseGraph):
    """Class that allows for merging of multiple graphs

    Attributes:
        _input_classes: list of input classes that link to a backend
        _args: variable nuber of graphs to merge
        _dag: graph of the dependencies between spock classes

    """

    def __init__(self, *args: Dict, input_classes: List):
        """

        Args:
            *args: variable number of graphs to merge
            input_classes: list of input classes that link to a backend
        """
        self._args = args
        self._input_classes = input_classes
        merged_dag = self._build()
        super().__init__(merged_dag, whoami="Merged Graph")

    @staticmethod
    def _merge_inputs(*args: Dict):
        """Merges multiple graphs into a single dependency graph

        Args:
            *args: variable number of graphs to merge

        Returns:
            dictionary of the merged dependency graphs

        """
        key_set = {k for arg in args for k in arg.keys()}
        super_dict = {k: set() for k in key_set}
        for arg in args:
            for k, v in arg.items():
                super_dict[k].update(v)
        return super_dict

    @property
    def nodes(self):
        """Returns the input_classes/nodes"""
        return self._input_classes

    def _build(self) -> Dict:
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            dictionary of nodes and their edges

        """
        return self._merge_inputs(*self._args)


class SelfGraph(BaseGraph):

    var_resolver = VarResolver()

    def __init__(self, cls: _C, fields: Dict):
        self._cls = cls
        self._fields = fields
        tmp_dag, self._ref_map = self._build()
        super(SelfGraph, self).__init__(tmp_dag, whoami="Self Variable Reference Graph")

    @property
    def node_names(self):
        return {k.name for k in self._cls.__attrs_attrs__}

    @property
    def node_map(self):
        """Returns a map of the node names to the underlying classes"""
        return {k: k for k in self.nodes}

    @property
    def reverse_map(self):
        """Returns a map from the underlying classes to the node names"""
        return {k: k for k in self.nodes}

    @property
    def nodes(self):
        return [k.name for k in self._cls.__attrs_attrs__]

    def resolve(self) -> Tuple[Dict, Set]:
        """Resolves variable references by searching thorough the current spock_space

        Args:

        Returns:
            field dictionary containing the resolved values and a set containing all
            changed variables to delay casting post resolution

        """
        # Iterate in topo order
        for k in self.topological_order:
            # get the self dependent values and swap within the fields dict
            for v in self.dag[k]:
                typed_val, _ = self.var_resolver.resolve_self(
                    value=self._fields[v],
                    set_value=self._fields[k],
                    ref_match=self._ref_map[v][k],
                    name=v,
                )
                self._fields[v] = typed_val
        # Get a set of all changed variables
        return self._fields, set(self._ref_map.keys())

    def _build(self) -> Tuple[Dict, Dict]:
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            dictionary of nodes and their edges

        """
        # Build a dictionary of all nodes (attributes in the class)
        v_e = {val: [] for val in self.node_names}
        ref_map = {}
        for k, v in self._fields.items():
            # ref_map.update({k: {}})
            # Can only check against str types
            if isinstance(v, str):
                # Check if there is a regex match
                if self.var_resolver.detect(v, str):
                    # Get the matched reference
                    return_list = self.var_resolver.get_regex_match_reference(v)
                    for typed_ref, _, annotation, match_val in return_list:
                        dep_cls, dep_val = typed_ref.split(".")
                        if dep_cls == self._cls.__name__:
                            v_e.get(dep_val).append(k)
                            if k not in ref_map.keys():
                                ref_map.update({k: {}})
                            ref_map[k].update({dep_val: match_val})
                            # ref_map.update({k: match_val})
        return {key: set(val) for key, val in v_e.items()}, ref_map


class VarGraph(BaseGraph):
    """Class that helps with variable resolution by mapping dependencies

    Attributes:
        _input_classes: list of input classes that link to a backend
        _cls_fields_tuple: tuple of cls and the given field dict
        _dag: graph of the dependencies between spock classes
        var_resolver: cls instance of the variable resolver
       ref_map: dictionary of the references that need to be mapped to a value

    """

    var_resolver = VarResolver()

    def __init__(self, cls_fields_list: List[Tuple[_C, Dict]], input_classes: List):
        """

        Args:
            cls_fields_list: tuple of cls and the given field dict
            input_classes: list of input classes that link to a backend
        """
        self._cls_fields_tuple = cls_fields_list
        self._input_classes = input_classes
        tmp_dag, self.ref_map = self._build()
        super().__init__(tmp_dag, whoami="Class Variable Reference Graph")

    @property
    def cls_names(self):
        """Returns the set of class names"""
        return {spock_cls.__name__ for spock_cls, _ in self._cls_fields_tuple}

    @property
    def cls_values(self):
        """Returns a map of the class name and the underlying classes"""
        return {
            spock_cls.__name__: spock_cls for spock_cls, _ in self._cls_fields_tuple
        }

    @property
    def cls_map(self):
        """Returns a map between the class names and the field dictionaries"""
        return {
            spock_cls.__name__: fields for spock_cls, fields in self._cls_fields_tuple
        }

    @property
    def nodes(self):
        """Returns the input_classes/nodes"""
        return self._input_classes

    @property
    def ref_2_resolve(self) -> Set:
        """Returns the values that need to be resolved"""
        return set(self.ref_map.keys())

    def resolve(self, spock_cls: str, spock_space: Dict) -> Tuple[Dict, Set]:
        """Resolves variable references by searching thorough the current spock_space

        Args:
            spock_cls: name of the spock class
            spock_space: current spock_space to look for the underlying value

        Returns:
            field dictionary containing the resolved values and a set containing all
            changed variables to delay casting post resolution

        """
        # First we check for any needed variable resolution
        changed_vars = set()
        if spock_cls in self.ref_2_resolve:
            # iterate over the mapped refs to swap values -- using the var resolver
            # to get the correct values
            for ref in self.ref_map[spock_cls]:
                typed_val, _ = self.var_resolver.resolve(
                    value=self.cls_map[spock_cls][ref["val"]],
                    value_type=getattr(
                        self.node_map[spock_cls].__attrs_attrs__, ref["val"]
                    ).type,
                    ref=ref,
                    spock_space=spock_space,
                )
                # Swap the value to the replaced version
                self.cls_map[spock_cls][ref["val"]] = typed_val
            # Get a set of all changed variables
            changed_vars = {n["val"] for n in self.ref_map[spock_cls]}
        # Return the field dict
        return self.cls_map[spock_cls], changed_vars

    def _build(self) -> Tuple[Dict, Dict]:
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            tuple of dictionary of nodes and their edges and well as the dictionary
            map between the references

        """
        # Build a dictionary of all nodes (base spock classes)
        nodes = {val: [] for val in self.node_names}
        node_ref = {val: [] for val in self.node_names}
        node_ref = {}
        # Iterate through the tuples and see if there are any var refs
        # in the fields
        for spock_cls, fields in self._cls_fields_tuple:
            ref_map = []
            for k, v in fields.items():
                # Can only check against str types
                if isinstance(v, str):
                    # Check if there is a regex match
                    if self.var_resolver.detect(v, str):
                        # Get the matched reference
                        return_list = self.var_resolver.get_regex_match_reference(v)
                        for typed_ref, _, annotation, match_val in return_list:
                            dep_cls, dep_val = typed_ref.split(".")
                            # Make sure the ref is an actual spock class
                            if dep_cls not in self.node_names:
                                raise _SpockVarResolverError(
                                    f"Reference to missing @spock decorated class -- "
                                    f"`{dep_cls}` was not passed as an *arg to "
                                    f"SpockBuilder and/or could not be found via lazy "
                                    f"evaluation within "
                                    f"sys.modules['spock'].backend.config"
                                )
                            # Only add non-self deps -- as we are resolving between
                            # class dependencies here. We will resolve self deps
                            # elsewhere
                            if dep_cls != spock_cls.__name__:
                                nodes.get(dep_cls).append(spock_cls)
                                # Map the value names such that we can use them later
                                # post sort
                                ref_map.append(
                                    {
                                        "val": k,
                                        "class": dep_cls,
                                        "class_val": dep_val,
                                        "matched": match_val,
                                    }
                                )
                        # Append the dependent mapped names to the class name
                        if len(ref_map) > 0:
                            node_ref.update({spock_cls.__name__: ref_map})
                            # node_ref.get(spock_cls.__name__).append(ref_map)
        nodes = {key: set(val) for key, val in nodes.items()}
        return nodes, node_ref


class Graph(BaseGraph):
    """Class that holds graph methods for determining dependencies between spock classes

    Attributes:
        _input_classes: list of input classes that link to a backend
        _dag: graph of the dependencies between spock classes
        _lazy: attempts to lazily find @spock decorated classes registered within
        sys.modules["spock"].backend.config

    """

    def __init__(self, input_classes: List, lazy: bool):
        """Init call for Graph class

        Args:
            input_classes: list of input classes that link to a backend
            lazy: attempts to lazily find @spock decorated classes registered within
            sys.modules["spock"].backend.config
        """
        self._input_classes = input_classes
        self._lazy = lazy
        # Maybe find classes lazily -- roll them into the input class tuple
        # make sure to cast as a set first since the lazy search might find duplicate
        # references
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
        super().__init__(self._build(), whoami="Class Reference Graph")

    @property
    def nodes(self):
        """Returns the input_classes/nodes"""
        return self._input_classes

    @staticmethod
    def _yield_class_deps(classes: Union[List, Tuple]) -> Generator[Tuple, None, None]:
        """Generator to iterate through nodes and find dependencies

        Args:
            classes: list or tuple of classes to iterate through

        Yields:
            tuple or the base input class and the current name of the dependent class

        """
        for input_class in classes:
            dep_names = {f"{v.__name__}" for v in _find_all_spock_classes(input_class)}
            for v in dep_names:
                yield input_class, v

    def _lazily_find_classes(self, classes: List) -> Tuple:
        """Searches within the spock sys modules attributes to lazily find @spock
        decorated classes

        These classes have been decorated with @spock but might not have been passes
        into the ConfigArgBuilder so
        this allows for 'lazy' lookup of these classes to make the call to
        ConfigArgBuilder a little less verbose
        when there are a lot of spock classes

        Returns:
            tuple of any lazily discovered classes

        """
        # Iterate thorough each of the base spock classes to get the dependencies and
        # reverse dependencies
        lazy_classes = []
        for _, v in self._yield_class_deps(classes):
            if (
                hasattr(sys.modules["spock"].backend.config, v)
                and getattr(sys.modules["spock"].backend.config, v) not in classes
            ):
                print(
                    f"Lazy evaluation found a @spock decorated class named `{v}` "
                    f"within the registered types of "
                    f"sys.modules['spock'].backend.config -- Attempting to use the "
                    f"class `{getattr(sys.modules['spock'].backend.config, v)}` "
                    f"within the SpockBuilder"
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

    def _lazily_find_parents(self) -> Tuple:
        """Searches within the current set of input_classes (@spock decorated classes)
        to lazily find any parents

        Given that lazy inheritance means that the parent classes won't be included
        (since they are cast to spock
        classes within the decorator and the MRO is handled internally) this allows
        the lazy flag to find those parent
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
                            f"Lazy evaluation found a @spock decorated parent class "
                            f"named `{cls_name}` within the "
                            f"registered types of sys.modules['spock'].backend.config "
                            f"-- Appending the class "
                            f"`{getattr(sys.modules['spock'].backend.config, cls_name)}`"
                            f" to the SpockBuilder..."
                        )
                        lazy_parents.update({base.__name__: base})
        return tuple(lazy_parents.values())

    def _build(self) -> Dict:
        """Builds a dictionary of nodes and their edges (essentially builds the DAG)

        Returns:
            dictionary of nodes and their edges

        """
        # Build a dictionary of all nodes (base spock classes)
        nodes = {val: [] for val in self.node_names}
        # Iterate through all of the base spock classes to get the dependencies
        # and reverse dependencies
        for input_class, v in self._yield_class_deps(self._input_classes):
            if v not in self.node_names:
                raise ValueError(
                    f"Missing @spock decorated class -- `{v}` was not passed "
                    f"as an *arg to "
                    f"SpockBuilder and/or could not be found via lazy evaluation "
                    f"(currently lazy=`{self._lazy}`) "
                    f"within sys.modules['spock'].backend.config"
                )
            nodes.get(v).append(input_class)
        nodes = {key: set(val) for key, val in nodes.items()}
        return nodes
