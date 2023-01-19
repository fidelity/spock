# -*- coding: utf-8 -*-

# SPDX-License-Identifier: Apache-2.0

"""Helper functions for Spock"""

from typing import Dict, List, Optional, Tuple, Union

from spock.backend.saver import AttrSaver
from spock.backend.wrappers import Spockspace
from spock.exceptions import _SpockValueError
from spock.utils import _C, _is_spock_instance


def to_dict(
    objs: Union[_C, List[_C], Tuple[_C, ...]], saver: Optional[AttrSaver] = AttrSaver()
) -> Dict[str, Dict]:
    """Converts spock classes from a Spockspace into their dictionary representations

    Args:
        objs: single spock class or an iterable of spock classes
        saver: optional saver class object

    Returns:
        dictionary where the class names are keys and the values are the dictionary
        representations
    """
    if isinstance(objs, (List, Tuple)):
        obj_dict = {}
        for val in objs:
            if not _is_spock_instance(val):
                raise _SpockValueError(
                    f"Object is not a @spock decorated class object -- "
                    f"currently `{type(val)}`"
                )
            obj_dict.update({type(val).__name__: val})
    elif _is_spock_instance(objs):
        obj_dict = {type(objs).__name__: objs}
    else:
        raise _SpockValueError(
            f"Object is not a @spock decorated class object -- "
            f"currently `{type(objs)}`"
        )
    return saver.dict_payload(Spockspace(**obj_dict))
