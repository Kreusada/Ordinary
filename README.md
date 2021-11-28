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

- `set_delimiter()`

    Sets the module's delimiter to use when encoding and decoding. The delimiter
    must meet the following criteria:

    * Must be a string
    * Must be a single character
    * Must not be a digit

    You can pass no argument to this function to reset it to the standard (`-`).

    ```py
    set_delimiter("C")
    >>> None
    encode("Hello world!")
    >>> "72C101C108C108C111C32C119C111C114C108C100C33"
    set_delimiter()
    encode("Hello world!")
    >>> "72-101-108-108-111-32-119-111-114-108-100-33"
    ```

- `get_delimiter()`

    Gets the modules current delimiter.

    ```py
    get_delimiter()
    >>> "-"
    set_delimiter("C")
    get_delimiter()
    >>> "C"
    ```

- `temporary_delimiter()`

    This function is to be used as a context manager. It sets the delimiter whilst
    the context manager is open.

    ```py
    with temporary_delimiter("C"):
        encode("Hello world!")
        >>> "72C101C108C108C111C32C119C111C114C108C100C33"
    encode("Hello world!")
    >>> "72-101-108-108-111-32-119-111-114-108-100-33"
    ```

    You can also use the `after` kwarg, used to define the delimiter that is set
    once the context manager has exited. It defaults to None, meaning it will remember
    the previously set delimiter and will instead set it to such delimiter.

    ```py
    get_delimiter()
    >>> "-"
    with temporary_delimiter("C", after="D"):
        ...
    get_delimiter()
    >>> "D"
    with temporary_delimiter("C"):
        ...
    get_delimiter()
    >>> "D"
    ```

### Installation

Install using the recommended installer, Pip.

```sh
pip install ordinary
```
