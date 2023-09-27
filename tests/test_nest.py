from typing import List, Tuple

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
        ([('foo', '1'), ('foo', '2'), ('foo', '3')], {'foo': ['1', '2', '3']}),
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
def test_nest(obj: List[Tuple[str, str]], expected: qstring.Nested) -> None:
    assert qstring.nest(obj) == expected


def test_nest_maintains_order() -> None:
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

    b = nested['b']
    assert isinstance(b, dict)
    assert list(b.keys()) == ['a', 'b', 'c']

    c = nested['c']
    assert isinstance(c, dict)

    c_a = c['a']
    assert isinstance(c_a, dict)
    assert list(c_a.keys()) == ['a', 'b', 'c']


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
def test_merge(
    target: qstring.Nested,
    source: qstring.Nested,
    expected: qstring.Nested
) -> None:
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
def test_merge_error(
    target: qstring.Nested,
    source: qstring.Nested,
    error: str
) -> None:
    with pytest.raises(qstring.ParameterTypeError) as exc_info:
        _merge(target, source)
    assert str(exc_info.value) == error
