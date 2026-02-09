class TooManyUniqueFailsException(Exception):
    def __str__(self):
        return "Failed to generate unique values"

class InvalidGenerationException(Exception):
    pass