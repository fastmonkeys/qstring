from collections import OrderedDict

import pytest

import qstring


@pytest.mark.parametrize(
    ('obj', 'expected'),
    [
        (
            OrderedDict([('', '')]),
            [('', '')]
        ),
        (
            OrderedDict([('foo', '')]),
            [('foo', '')]
        ),
        (
            OrderedDict([('', 'bar')]),
            [('', 'bar')]
        ),
        (
            OrderedDict([('foo', 'bar')]),
            [('foo', 'bar')]
        ),
        (
            OrderedDict([('foo', ''), ('bar', '')]),
            [('foo', ''), ('bar', '')]
        ),
        (
            OrderedDict([('foo', ['1', '2'])]),
            [('foo', '1'), ('foo', '2')]
        ),
        (
            OrderedDict([('foo', '1'), ('bar', '2')]),
            [('foo', '1'), ('bar', '2')]
        ),
        (
            OrderedDict([('x', OrderedDict([('y', '1')]))]),
            [('x[y]', '1')]
        ),
        (
            OrderedDict([
                ('x', OrderedDict([
                    ('y', OrderedDict([('z', '1')]))
                ]))
            ]),
            [('x[y][z]', '1')]
        ),
    ]
)
def test_unnest(obj, expected):
    assert qstring.unnest(obj) == expected
