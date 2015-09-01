import pytest

import qstring
from qstring.nest import _merge


@pytest.mark.parametrize(
    ('obj', 'expected'),
    [
        ([], {}),
        ([('', '')], {'': ''}),
        ([('foo', '')], {'foo': ''}),
        ([('', 'bar')], {'': 'bar'}),
        ([('foo', 'bar')], {'foo': 'bar'}),
        ([('foo', ''), ('bar', '')], {'foo': '', 'bar': ''}),
        ([('foo', '1'), ('foo', '2')], {'foo': ['1', '2']}),
        ([('foo', '1'), ('bar', '2')], {'foo': '1', 'bar': '2'}),
        ([('x[y]', '1')], {'x': {'y': '1'}}),
        ([('x[y][z]', '1')], {'x': {'y': {'z': '1'}}}),
        ([('x[]', '1')], {'x[]': '1'}),
        ([('x[', '1')], {'x[': '1'}),
        ([('x]', '1')], {'x]': '1'}),
        ([('x[]]', '1')], {'x[]]': '1'}),
        ([('x[[]', '1')], {'x[[]': '1'}),
    ]
)
def test_nest(obj, expected):
    assert qstring.nest(obj) == expected


def test_nest_maintains_order():
    nested = qstring.nest([
        ('a', '1'),
        ('b[a]', '1'),
        ('b[b]', '2'),
        ('b[c]', '3'),
        ('c[a][a]', '1'),
        ('c[a][b]', '2'),
        ('c[a][c]', '3'),
    ])
    assert list(nested.keys()) == ['a', 'b', 'c']
    assert list(nested['b'].keys()) == ['a', 'b', 'c']
    assert list(nested['c']['a'].keys()) == ['a', 'b', 'c']


@pytest.mark.parametrize(('target', 'source', 'expected'), [
    (
        {'a': '1'},
        {},
        {'a': '1'}
    ),
    (
        {'a': '1'},
        {'b': '2'},
        {'a': '1', 'b': '2'}
    ),
    (
        {'a': '1'},
        {'b': {'c': '2'}},
        {'a': '1', 'b': {'c': '2'}}
    ),
    (
        {'a': {'b': '1'}},
        {'a': {'c': '2'}},
        {'a': {'b': '1', 'c': '2'}}
    ),
])
def test_merge(target, source, expected):
    assert _merge(target, source) == expected


@pytest.mark.parametrize(
    ('target', 'source', 'error'),
    [
        (
            {'x': '1'},
            {'x': {'y': '2'}},
            "Expected str (got dict) for param 'x'",
        ),
        (
            {'x': {'y': '1'}},
            {'x': '2'},
            "Expected dict (got str) for param 'x'",
        ),
        (
            {'x': ['1', '2']},
            {'x': {'y': '3'}},
            "Expected list (got dict) for param 'x'",
        ),
        (
            {'x': {'y': '3'}},
            {'x': ['1', '2']},
            "Expected dict (got list) for param 'x'",
        ),
    ]
)
def test_merge_error(target, source, error):
    with pytest.raises(qstring.ParameterTypeError) as exc_info:
        _merge(target, source)
    assert str(exc_info.value) == error
