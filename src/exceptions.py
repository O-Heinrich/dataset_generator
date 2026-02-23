class InvalidGenerationException(Exception):
    pass

class DuplicateTablenameException(Exception):
    def __str__(self):
        return "Cannot have the same name for different tables within one generation."