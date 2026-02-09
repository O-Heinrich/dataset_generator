from exceptions import TooManyUniqueFailsException

def generateRandomList(randomGenerator, size, unique=False, maxUniqueFailsMultiplier=3):
    if not callable(randomGenerator):
        raise TypeError()
    if not unique:
        return [randomGenerator() for _ in range(size)]
    result = set()
    count = 0
    while len(result) < size:
        result.add(randomGenerator())
        count += 1
        if count > size * maxUniqueFailsMultiplier:
            raise TooManyUniqueFailsException()
    return list(result)

def stringify(thing, sep=", "):
    if isinstance(thing, str):
        return f'"{thing}"'
    elif isinstance(thing, list):
        return sep.join([stringify(x) for x in thing])
    else:
        return str(thing)