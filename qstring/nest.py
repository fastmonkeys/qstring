import re
from typing import Dict, Generator, List, Literal, NamedTuple, Tuple, Union

from . import exc

Nested = Dict[str, Union[str, List[str], 'Nested']]

def nest(params: List[Tuple[str, str]]) -> Nested:
    """
    Create a nested object from a list of query string parameters.

    Examples::

        >>> nest([('foo[bar]', 'baz')])
        {'foo': {'bar': 'baz'}}

        >>> nest([('x[y]', '1'), ('x[y]', '2')])
        {'x': {'y': ['1', '2']}}

    :param params:
        a list of query string parameter where each item is a tuple
        representing a key-value pair.

    :raises qstring.ParameterTypeError:
        if parameters of conflicting types are given.
    """
    nested: Nested = {}
    params_dict = _convert_params_list_to_dict(params)
    for key, value in params_dict.items():
        try:
            obj = _parse_parameter(key, value)
        except exc.ParseError:
            obj = {key: value}
        _merge(nested, obj)
    return nested


def _convert_params_list_to_dict(
    params_list: List[Tuple[str, str]]
) -> Dict[str, Union[str, List[str]]]:
    params_dict: Dict[str, Union[str, List[str]]] = {}
    for key, value in params_list:
        if key in params_dict:
            old_value = params_dict[key]
            params_dict[key] = (
                old_value + [value]
                if isinstance(old_value, list)
                else [old_value, value]
            )
        else:
            params_dict[key] = value
    return params_dict


def _parse_parameter(key: str, value: Union[str, List[str]]) -> Nested:
    return _ParameterParser().parse(key, value)


_TokenType = Literal['LEFT BRACKET', 'RIGHT BRACKET', 'NAME']

class _Token(NamedTuple):
    type: _TokenType
    value: str


class _ParameterParser:
    def parse(self, key: str, value: Union[str, List[str]]) -> Nested:
        self.key = key
        self.value = value
        self.tokens = list(self._tokenize(key))
        key = self._match_name()
        return {key: self._parse_object()}

    def _tokenize(self, input: str) -> Generator[_Token, None, None]:
        for value in re.split(r'([\[\]])', input):
            if value == '[':
                yield _Token('LEFT BRACKET', value)
            elif value == ']':
                yield _Token('RIGHT BRACKET', value)
            elif value:
                yield _Token('NAME', value)

    def _parse_object(self) -> Union[str, List[str], Nested]:
        if not self.tokens:
            return self.value
        key = self._match_object()
        return {key: self._parse_object()}

    def _match_name(self) -> str:
        token, = self._match('NAME')
        return token.value

    def _match_object(self) -> str:
        _, token, _ = self._match('LEFT BRACKET', 'NAME', 'RIGHT BRACKET')
        return token.value

    def _match(self, *expected_types: _TokenType) -> List[_Token]:
        tokens = self.tokens[:len(expected_types)]
        types = tuple(t.type for t in tokens)
        if types != expected_types:
            raise exc.ParseError(self.key)
        self.tokens = self.tokens[len(expected_types):]
        return tokens


def _merge(target: Nested, source: Nested) -> Nested:
    items = source.items()
    for key, value in items:
        if key in target:
            if not isinstance(value, dict):
                raise exc.ParameterTypeError(
                    'Expected dict (got {got}) for param {param!r}'.format(
                        got=type(value).__name__,
                        param=key
                    )
                )
            target_value = target[key]
            if not isinstance(target_value, dict):
                raise exc.ParameterTypeError(
                    'Expected {expected} (got dict) for param {param!r}'.format(
                        expected=type(target_value).__name__,
                        param=key
                    )
                )
            value = _merge(target_value, value)
        target[key] = value
    return target
