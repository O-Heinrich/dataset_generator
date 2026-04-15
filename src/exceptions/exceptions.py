class InvalidGenerationException(Exception):
    """
    Exception thrown in backend, when a value that was generated turns out to be invalid for any reason.
    """
    pass

class DuplicateTablenameException(Exception):
    """
    Exception thrown in backend, when input dictionary contains the same tablename more than once.
    """
    def __str__(self):
        return "Cannot have the same name for different tables within one generation."