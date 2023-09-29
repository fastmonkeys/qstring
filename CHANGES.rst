Changelog
---------

1.0.0 (not yet released)
^^^^^^^^^^^^^^^^^^^^^^^^

- Added support for Python 3.8 to 3.12.
- Added type hints for the project.
- Use modern packaging metadata with ``pyproject.toml``.
- Use ``pdm.backend`` as build backend.
- Changed ``qstring.nest`` to use ``dict`` in the returned nested object instead
  of ``OrderedDict``. ``dict`` retains insertion order since Python 3.7, so
  ``OrderedDict`` usage was redundant here.
- Fixed a bug in ``qstring.nest`` where it returned an incorrect value when
  there were more than two query parameters with the same name.

  Before::

      >>> qtstring.nest([('foo', '1'), ('foo', '2'), ('foo', '3')])
      {'foo': [['1', '2'], '3']}

  After::

      >>> qtstring.nest([('foo', '1'), ('foo', '2'), ('foo', '3')])
      {'foo': ['1', '2', '3']}

- Removed support for Python 2.7 and 3.7 or earlier.
- Removed ``future`` dependency.
- Removed the ``__version__`` attribute. Use
  ``importlib.metadata.version("qstring")`` instead

0.2.1 (March 24, 2017)
^^^^^^^^^^^^^^^^^^^^^^

- Fixed ``qstring.unnest`` when values contain non-ASCII characters.


0.2.0 (September 1, 2015)
^^^^^^^^^^^^^^^^^^^^^^^^^

- Changed ``qstring.nest`` to maintain the order of the given parameters in the
  returned nested object by returning ``OrderedDict`` instead of ``dict``.


0.1.0 (July 14, 2015)
^^^^^^^^^^^^^^^^^^^^^

- Initial public release.
