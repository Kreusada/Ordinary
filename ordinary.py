"""Encoding tools for a largely compatible encryption system based on the interpolation of character and ordinal values.

decode() - decode Ordinary into standard text.
encode() - encode a string into Ordinary.
parse() - raises an OrdinalError if the provided text is not provided in Ordinary form.
safeparse() - return a bool based on whether the provided text is not provided in Ordinary form.
set_delimiter() - sets the delimiter used by the encoder.
get_delimiter() - gets the set Ordinary delimiter.

There's also the temporary_delimiter function, used to temporarily set the delimiter instead of making
the change permanent. This should be used as a context manager. When exiting the context manager, the delimiter
will be restored to its previous state, like so:

with ordinary.temporary_delimiter("C"):
    print(ordinary.get_delimiter())
    >>> "C"
    print(ordinary.encode("hello"))
    >>> 72C101C108C108C111C32C119C111C114C108C100C33
print(ordinary.get_delimiter())
>>> "-"

"""

import contextlib

MAX_RANGE = 1114112
_delimiter = "-"
__version__ = "2.0.0"


class OrdinalError(ValueError):
    pass


@contextlib.contextmanager
def temporary_delimiter(delimiter: str, *, after: str = None):
    """Set a temporary delimiter.

    Ordinary's delimiter will be restored to
    it's previous state after. Use this function
    as a context manager.
    """
    global _delimiter
    current = _delimiter
    set_delimiter(delimiter)
    try:
        yield
    finally:
        if after is None:
            _delimiter = current
        else:
            # We want to clarify this is as a result
            # of the after kwarg, so we make this amendment :)
            try:
                set_delimiter(after)
            except (TypeError, ValueError) as exc:
                raise exc(f"after {exc}") from None


del contextlib


def set_delimiter(delimiter: str = None, /) -> None:
    """Sets the delimiter used by the encoder."""
    if delimiter is None:
        delimiter = "-"
    else:
        if not isinstance(delimiter, str):
            raise TypeError("delimiter must be str")
        if len(delimiter) != 1:
            raise ValueError("delimiter length must be 1")
        if delimiter.isdigit():
            raise ValueError("delimeter must be a non numeric character")
    global _delimiter
    _delimiter = delimiter


def get_delimiter() -> str:
    """Gets the set Ordinary delimiter."""
    return _delimiter


def parse(text: str) -> None:
    """Parses the given Ordinary to make sure it is syntactically correct."""
    text = _delimiter.join(text.splitlines())
    split = text.split(_delimiter)
    for i in range(len(split)):
        if not (n := split[i]).isdigit():
            raise OrdinalError("value '%s' at position %s is not a digit" % (n, i))
        if int(n) not in range(MAX_RANGE):
            raise OrdinalError("value '%s' at position %s is not in range(%s)" % (n, i, MAX_RANGE))


def safeparse(text: str) -> bool:
    """Parses the given Ordinary, returning bool instead of raising."""
    try:
        parse(text)
    except OrdinalError:
        return False
    else:
        return True


def encode(text: str, *, cutoff: int = None):
    """Encode a string into Ordinary.

    Use the cutoff kwarg to control the number of ords per row.
    """
    i = tuple(map(lambda x: str(ord(x)), text))
    if not (cutoff is None or isinstance(cutoff, int)):
        raise ValueError("cutoff kwarg must be None or int")
    if cutoff is None or cutoff >= len(i):
        return _delimiter.join(i)
    ret = ""
    for x in [i[x : x + cutoff] for x in range(0, len(i), cutoff)]:
        ret += _delimiter.join(x) + "\n"
    return ret


def decode(text: str):
    """Decode Ordinary into standard text."""
    text = _delimiter.join(map(str.strip, text.splitlines())).strip()
    parse(text)
    return "".join(map(lambda x: chr(int(x)), text.split(_delimiter)))
