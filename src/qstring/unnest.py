from typing import List, Tuple, Union

from qstring.nest import Nested


def unnest(obj: Nested) -> List[Tuple[str, str]]:
    """
    Create a list of query string parameters from a nested object.

    Examples::

        >>> unnest({'foo': {'bar': 'baz'}})
        [('foo[bar]', 'baz')]

        >>> unnest({'x': {'y': ['1', '2']}})
        [('x[y]', '1'), ('x[y]', '2')]
    """
    return _unnest(obj)


def _unnest(
    obj: Union[Nested, List[str], str], prefix: str = ""
) -> List[Tuple[str, str]]:
    if isinstance(obj, dict):
        params = []
        for key, value in obj.items():
            params.extend(
                _unnest(obj=value, prefix=prefix + "[" + key + "]" if prefix else key)
            )
        return params
    elif isinstance(obj, list):
        return [(prefix, value) for value in obj]
    else:
        return [(prefix, str(obj))]
