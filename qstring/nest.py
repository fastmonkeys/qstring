import collections
import re

from . import exc


def nest(params):
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
    nested = collections.OrderedDict()
    params = _convert_params_list_to_dict(params)
    for key, value in params.items():
        try:
            obj = _parse_parameter(key, value)
        except exc.ParseError:
            obj = {key: value}
        _merge(nested, obj)
    return nested


def _convert_params_list_to_dict(params_list):
    params_dict = collections.OrderedDict()
    for key, value in params_list:
        if key in params_dict:
            params_dict[key] = [params_dict[key], value]
        else:
            params_dict[key] = value
    return params_dict


def _parse_parameter(key, value):
    return _ParameterParser().parse(key, value)


class _ParameterParser(object):
    def parse(self, key, value):
        self.key = key
        self.value = value
        self.tokens = list(self._tokenize(key))
        key = self._match_name()
        return collections.OrderedDict([(key, self._parse_object())])

    def _tokenize(self, input):
        for value in re.split(r'([\[\]])', input):
            if value == '[':
                yield _Token('LEFT BRACKET', value)
            elif value == ']':
                yield _Token('RIGHT BRACKET', value)
            elif value:
                yield _Token('NAME', value)

    def _parse_object(self):
        if not self.tokens:
            return self.value
        key = self._match_object()
        return collections.OrderedDict([(key, self._parse_object())])

    def _match_name(self):
        token, = self._match('NAME')
        return token.value

    def _match_object(self):
        _, token, _ = self._match('LEFT BRACKET', 'NAME', 'RIGHT BRACKET')
        return token.value

    def _match(self, *expected_types):
        tokens = self.tokens[:len(expected_types)]
        types = tuple(t.type for t in tokens)
        if types != expected_types:
            raise exc.ParseError(self.key)
        self.tokens = self.tokens[len(expected_types):]
        return tokens


_Token = collections.namedtuple('_Token', ['type', 'value'])


def _merge(target, source):
    items = source.items()
    for key, value in items:
        if key in target:
            _check_parameter_type(dict, key, value)
            _check_parameter_type(type(target[key]), key, value)
            value = _merge(target[key], value)
        target[key] = value
    return target


def _check_parameter_type(expected_type, param, value):
    if not isinstance(value, expected_type):
        raise exc.ParameterTypeError(
            'Expected {expected} (got {got}) for param {param!r}'.format(
                expected=expected_type.__name__,
                got=type(value).__name__,
                param=param
            )
        )
