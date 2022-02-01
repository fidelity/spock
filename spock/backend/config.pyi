from typing import Any, Callable, Dict, List, Tuple, TypeVar, Union, overload

from attr import attrib, field

_T = TypeVar("_T")
_C = TypeVar("_C", bound=type)
SavePath: SavePath

# Note: from here
# https://github.com/python-attrs/attrs/blob/main/src/attr/__init__.pyi

# Static type inference support via __dataclass_transform__ implemented as per:
# https://github.com/microsoft/pyright/blob/main/specs/dataclass_transforms.md
# This annotation must be applied to all overloads of "spock_attr"

# NOTE: This is a typing construct and does not exist at runtime.  Extensions
# wrapping attrs decorators should declare a separate __dataclass_transform__
# signature in the extension module using the specification linked above to
# provide pyright support -- this currently doesn't work in PyCharm
def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]: ...
@overload
@__dataclass_transform__(kw_only_default=True, field_descriptors=(attrib, field))
def spock_attr(
    maybe_cls: _C,
    kw_only: bool = True,
    make_init: bool = True,
    dynamic: bool = False,
) -> _C: ...
@overload
@__dataclass_transform__(kw_only_default=True, field_descriptors=(attrib, field))
def spock_attr(
    maybe_cls: None = ...,
    kw_only: bool = True,
    make_init: bool = True,
    dynamic: bool = False,
) -> Callable[[_C], _C]: ...
def _base_attr(
    cls: _C,
    kw_only: bool = ...,
    make_init: bool = ...,
    dynamic: bool = ...,
) -> (List[_C], Dict, Dict): ...
