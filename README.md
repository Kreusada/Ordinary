# Ordinary

Encoding tools for a largely compatible encryption system based on
the interpolation of character and ordinal values.

This library was designed for reverse compatible encryption of characters,
meaning you can encrypt or shelter information using this encoder.

Ordinary gets it's name from "ordinal", the name given to the numeric equivalent
of a single character. In Ordinary, ordinals are joined together with a hyphen delimeter to
generate numeric strings otherwise referred to as "Ordinary strings".

### Methods

- `encode()`
    
    Use the encode method to encode standard text into ordinary.

    ```py
    encode("Hello world!")
    >>> 72-101-108-108-111-32-119-111-114-108-100-33
    ```

    For pretty formatting, encode may take the ``cutoff`` kwarg,
    which specifies the number of ordinal files per line. This
    is handy when writing to files. It defaults to None, meaning
    it will just remain a continuous line. This is fine for shorter encodings.

    ```py
    encode("Hello world!", cutoff=5)
    >>> 72-101-108-108-111
        32-119-111-114-108
        100-33
    ```

- `decode()`

    The reverse of `encode()`. Self-explanatory, really.

    ```py
    decode("72-101-108-108-111-32-119-111-114-108-100-33")
    >>> "Hello world!"

- `parse()`

    Parses the given Ordinary to make sure that it is valid.
    This function is always used by `decode()`. If there is a syntactical
    error with the provided Ordinary, OrdinalError will be raised. Otherwise,
    nothing will be returned.

    ```py
    parse("72-101-108-108-111-32-119-111-114-108-100-33")
    >>> None
    parse("72-101-108-108-111-32-AAAAAA-111-114-108-100-33")
    >>> OrdinalError: value 'AAAAAA' at position 6 is not a digit
    ```

- `safeparse()`

    Implements `parse()`, but returns bool instead of raising, or returning
    None. This may be more useful if you're not wanting to raise exceptions
    in your program.

    ```py
    safeparse("72-101-108-108-111-32-119-111-114-108-100-33")
    >>> True
    safeparse("72-101-BOO-108-111-32-119-111-114-108-100-33")
    >>> False
    ```

### Installation

Install using the recommended installer, Pip.

```sh
pip install ordinary
```
