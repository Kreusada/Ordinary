"""Encoding tools for a largely compatible encryption system based on the interpolation of character and ordinal values.

decode() - decode Ordinary into standard text.
encode() - encode a string into Ordinary.
parse() - raises an OrdinalError if the provided text is not provided in Ordinary form.
safeparse() - return a bool based on whether the provided text is not provided in Ordinary form.

"""

MAX_RANGE = 1114112
DELIMETER = "-"

__version__ = "1.0.0"


class OrdinalError(ValueError):
    pass


def parse(text: str) -> None:
    """Parses the given Ordinary to make sure it is syntactically correct."""
    text = DELIMETER.join(text.splitlines())
    split = text.split(DELIMETER)
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
        return DELIMETER.join(i)
    ret = ""
    for x in [i[x : x + cutoff] for x in range(0, len(i), cutoff)]:
        ret += DELIMETER.join(x) + "\n"
    return ret


def decode(text: str):
    """Decode Ordinary into standard text."""
    text = DELIMETER.join(text.splitlines())
    parse(text)
    return "".join(map(lambda x: chr(int(x)), text.split(DELIMETER)))


def _main():
    """
    main script for ordinary

    does not use cutoff kwarg when encoding
    """
    def inner():
        import sys
        argv = sys.argv[1:]
        if argv:
            if argv[0] not in ("encode", "decode"):
                raise RuntimeError("Please provide 'encode' or 'decode' with arguments.")
            if not argv[1:]:
                raise RuntimeError(f"Please provide arguments for the {argv[0]} command.")
            return globals()[argv[0]](" ".join(argv[1:]))
        else:
            command = input("Would you like to encode or decode?\n>>> ").lower()
            if command not in ("encode", "decode"):
                raise RuntimeError("Please only provide either encode or decode.")
            text = input(f"Now type the text that you would like to {command}:\n>>> ")
            return globals()[command](text)
    
    try:
        code = inner()
    except (OrdinalError, RuntimeError) as e:
        print(str(e))
    except KeyboardInterrupt:
        print("~~")
    else:
        print("\n" + code)


if __name__ == "__main__":
    _main()
