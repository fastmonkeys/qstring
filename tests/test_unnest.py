from typing import List, Tuple

import pytest

import qstring


@pytest.mark.parametrize(
    ('obj', 'expected'),
    [
        (
            {'': ''},
            [('', '')]
        ),
        (
            {'foo': ''},
            [('foo', '')]
        ),
        (
            {'': 'bar'},
            [('', 'bar')]
        ),
        (
            {'foo': 'bar'},
            [('foo', 'bar')]
        ),
        (
            {'foo': 'äö'},
            [('foo', 'äö')]
        ),
        (
            {'foo': '', 'bar': ''},
            [('foo', ''), ('bar', '')]
        ),
        (
            {'foo': ['1', '2']},
            [('foo', '1'), ('foo', '2')]
        ),
        (
            {'foo': '1', 'bar': '2'},
            [('foo', '1'), ('bar', '2')]
        ),
        (
            {'x': {'y': '1'}},
            [('x[y]', '1')]
        ),
        (
            {'x': {'y': {'z': '1'}}},
            [('x[y][z]', '1')]
        ),
    ]
)
def test_unnest(obj: qstring.Nested, expected: List[Tuple[str, str]]) -> None:
    assert qstring.unnest(obj) == expected
