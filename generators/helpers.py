from generators.exceptions import TooManyUniqueFailsException

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