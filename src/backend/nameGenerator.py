from faker import Faker

def generateFirstName(fake: Faker) -> str:
    """Generates a random first name using the given Faker."""
    return fake.first_name()

def generateLastName(fake: Faker) -> str:
    """Generates a random last name using the given Faker."""
    return fake.last_name()

def generateFullName(fake: Faker) -> str:
    """Generates a random full name (first and last name) using the given Faker."""
    return fake.name()