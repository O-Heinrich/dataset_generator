from difflib import unified_diff

def compare_trimmedFiles(actualPath, expectedPath):
    """Compares the two files in the given paths, ignoring any empty/whitespace lines"""
    actualLines = readTrimmedFile(actualPath)
    expectedLines = readTrimmedFile(expectedPath)

    diff = list(unified_diff(expectedLines, actualLines))
    assert diff == [], "Unexpected file contents:\n" + "".join(diff)

def readTrimmedFile(path):
    with open(path, 'r') as file:
        result = [l for l in file.readlines() if l.strip()]
    return result
