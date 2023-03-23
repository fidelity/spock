# -*- coding: utf-8 -*-

# Copyright FMR LLC <opensource@fidelity.com>
# SPDX-License-Identifier: Apache-2.0

"""Creates the spock config interface that wraps attr"""

import sys
from typing import Dict

import attr

from spock.backend.typed import katra
from spock.exceptions import _SpockInstantiationError, _SpockUndecoratedClass
from spock.utils import _is_spock_instance, contains_return, vars_dict_non_dunder


def _base_attr(cls, kw_only, make_init, dynamic):
    """Map type hints to katras

    Connector function that maps type hinting style to the defined katra style which uses the more strict
    attr.ib() definition

    Handles dynamic decorators which allows for inheritance of non @spock decorated classes

    Args:
        cls: basic class def
        dynamic: allows inherited classes to not be @spock decorated

    Returns:
        bases: all the base classes
        attrs_dict: the current dictionary of attr.attribute values
        merged_annotations: dictionary of type annotations

    """
    # Since we are not using the @attr.s decorator we need to get the parent classes for inheritance
    # We do this by using the mro and grabbing anything that is not the first and last indices in the list and wrapping
    # it into a tuple
    bases = ()
    base_annotation = {}
    base_defaults = {}
    base_optional = {}
    if len(cls.__mro__[1:-1]) > 0:
        # Get bases minus self and python class object
        bases = list(cls.__mro__[1:-1])
        for idx, base_cls in enumerate(bases):
            if not _is_spock_instance(base_cls) and not dynamic:
                raise _SpockUndecoratedClass(
                    f"Class `{base_cls.__name__}` was not decorated with the @spock decorator "
                    f"and `dynamic={dynamic}` was set for child class `{cls.__name__}` -- Please remedy one of these"
                )
            elif not _is_spock_instance(base_cls) and dynamic:
                bases[idx] = _process_class(base_cls, kw_only, make_init, dynamic)
        bases = tuple(bases)
        base_annotation = {}
        for val in bases:
            for attribute in val.__attrs_attrs__:
                # Since we are moving left to right via the MRO only update if not currently present
                # this maintains parity to how the MRO is handled in base python
                if attribute.name not in base_annotation:
                    if "type" in attribute.metadata:
                        base_annotation.update(
                            {attribute.name: attribute.metadata["og_type"]}
                        )
                    else:
                        base_annotation.update(
                            {attribute.name: val.__annotations__[attribute.name]}
                        )
                    if "optional" in attribute.metadata:
                        base_optional.update(
                            {attribute.name: attribute.metadata["optional"]}
                        )
        base_defaults = {
            attribute.name: attribute.default
            for val in bases
            for attribute in val.__attrs_attrs__
            if attribute.default is not (None or attr.NOTHING)
        }
    # Merge the annotations -- always override as this is the lowest level of the MRO
    if hasattr(cls, "__annotations__"):
        new_annotations = {k: v for k, v in cls.__annotations__.items()}
    else:
        new_annotations = {}
    merged_annotations = {**base_annotation, **new_annotations}

    cls_attrs = set()
    hooks = set()
    # Iterate through the bases first
    for val in bases:
        # Get the underlying attribute defs
        cls_attrs.update(set(vars_dict_non_dunder(val).keys()))
        # If it's an attr class -- add the underlying annotations
        if attr.has(val):
            cls_attrs.update(set(attr.fields_dict(val).keys()))
        # Add the underlying annotations
        if hasattr(cls, "__annotations__"):
            cls_attrs.update(set(val.__annotations__.keys()))

    # Then on the class itself get everything not from the parents
    # Set attributes
    cls_attrs.update(set(vars_dict_non_dunder(cls).keys()))
    # Annotated attributes
    cls_attrs.update(set(new_annotations.keys()))
    # Attr defined attributes
    if attr.has(cls):
        cls_attrs.update(set(attr.fields_dict(cls).keys()))

    # Make sure the lengths align -- if they don't then something isn't annotated
    # throw an exception and print the set diff (cls should always have more than the
    # merged set)
    if len(cls_attrs) != len(merged_annotations):
        # Get the merged keys set
        merged_set = set(merged_annotations.keys())
        raise _SpockInstantiationError(
            f"Class {cls.__name__} contains attributes without type annotations. "
            f"Please add type annotations to the following attributes: "
            f"{cls_attrs - merged_set}"
        )

    # Make a blank attrs dict for new attrs
    attrs_dict = {}
    for k, v in merged_annotations.items():
        # If the cls has the attribute then a default was set
        if hasattr(cls, k):
            default = getattr(cls, k)
        elif k in base_defaults:
            default = base_defaults[k]
        else:
            default = None
        # If the parent was optional then set the child to optional
        optional = False
        if k in base_optional:
            optional = base_optional[k]
        attrs_dict.update(
            {k: katra(typed=v, default=default, inherit_optional=optional)}
        )
    return bases, attrs_dict, merged_annotations


def _handle_hooks(
    cls,
    bases,
):
    """Handles creating a single function for all hooks from the given class and
    all its parents

    Args:
        cls: basic class definition

    Returns:
        function that contains all necessary hooks

    """

    # Check if the base classes have any hook functions
    hooks = [
        val.__attrs_post_init__ for val in bases if hasattr(val, "__attrs_post_init__")
    ]
    # maps = [val.__maps__ for val in bases if hasattr(val, "__maps__")]
    # Copy over the post init function -- borrow a bit from attrs library to add the
    # __post__hook__ method and/or the __maps__ method (via a shim method) to the init
    # call via `"__attrs_post_init__"`
    if hasattr(cls, "__post_hook__") or hasattr(cls, "__maps__") or (len(hooks) > 0):
        # Force the post_hook function to have no explict return
        if hasattr(cls, "__post_hook__") and contains_return(cls.__post_hook__):
            raise _SpockInstantiationError(
                f"__post_hook__ function contains an explict return. This function "
                f"cannot return any values (i.e. requires an implicit None return)"
            )
        if hasattr(cls, "__maps__") and not contains_return(cls.__maps__):
            raise _SpockInstantiationError(
                f"__maps__ function is missing an explict return. This function "
                f"needs to explicitly return any type of values"
            )
        # if there are parent hooks we need to map them into a function
        if len(hooks) > 0:
            # Create a shim function to combine __post_hook__ and __maps__
            # in addition to the parental hooks
            def __shim__(self):
                if hasattr(cls, "__post_hook__"):
                    cls.__post_hook__(self)
                # Call the parents hooks
                all_hooks = [val(self) for val in hooks]
                # Pop any None values
                all_hooks = [val for val in all_hooks if val is not None]
                # Add in the given hook
                if hasattr(cls, "__maps__"):
                    all_hooks = [cls.__maps__(self)] + all_hooks
                if len(all_hooks) == 1:
                    all_hooks = all_hooks[0]
                # Set maps to the mapped values
                object.__setattr__(self, "_maps", all_hooks)

        else:
            # Create a shim function to combine __post_hook__ and __maps__
            def __shim__(self):
                if hasattr(cls, "__post_hook__"):
                    cls.__post_hook__(self)
                if hasattr(cls, "__maps__"):
                    object.__setattr__(self, "_maps", cls.__maps__(self))
                    return cls.__maps__(self)
                else:
                    return None

    else:

        def __shim__(self):
            ...

    return __shim__


def _process_class(cls, kw_only: bool, make_init: bool, dynamic: bool):
    """Process a given class

    Args:
        cls: basic class definition
        kw_only: set kwarg only
        make_init: make an init function
        dynamic: allows inherited classes to not be @spock decorated

    Returns:
        cls with attrs dunder methods added

    """
    # Handles the MRO and gets old annotations
    bases, attrs_dict, merged_annotations = _base_attr(cls, kw_only, make_init, dynamic)
    # if hasattr(cls, "__post_hook__"):
    #     attrs_dict.update({"__post_hook__": cls.__post_hook__})
    # if hasattr(cls, "__maps__"):
    #     attrs_dict.update({"__maps__": cls.__maps__})
    # Map the __shim__ function into __attrs_post_init__
    attrs_dict.update({"__attrs_post_init__": _handle_hooks(cls, bases)})
    # Dynamically make an attr class
    obj = attr.make_class(
        name=cls.__name__,
        bases=bases,
        attrs=attrs_dict,
        kw_only=kw_only,
        frozen=True,
        auto_attribs=True,
        init=make_init,
    )
    # For each class we dynamically create we need to register it within the system
    # modules for pickle to work
    setattr(sys.modules["spock"].backend.config, obj.__name__, obj)
    # Swap the __doc__ string from cls to obj
    obj.__doc__ = cls.__doc__
    # Set the __init__ function
    # Handle __annotations__ from the MRO
    obj.__annotations__ = merged_annotations
    return obj


def spock_attr(
    maybe_cls=None,
    kw_only=True,
    make_init=True,
    dynamic=False,
):
    """Map type hints to katras

    Connector function that maps type hinting style to the defined katra style which uses the more strict
    attr.ib() definition -- this allows us to attach the correct validators for types before the attrs class is
    built

    Args:
        maybe_cls: maybe a basic class def maybe None depending on call type
        kw_only: Make all attributes keyword-only
        make_init: bool, define a __init__() method
        dynamic: allows inherited classes to not be @spock decorated -- will automatically cast parent classes to a
            spock class by traversing the MRO

    Returns:
        cls: attrs class that is frozen and kw only
    """

    def wrap(cls):
        return _process_class(
            cls, kw_only=kw_only, make_init=make_init, dynamic=dynamic
        )

    # Note: Taken from dataclass/attr definition(s)
    # maybe_cls's type depends on the usage of the decorator.  It's a class
    # if it's used as `@spock` but ``None`` if used as `@spock()`.
    if maybe_cls is None:
        return wrap
    else:
        return wrap(maybe_cls)
