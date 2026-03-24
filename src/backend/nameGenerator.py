from faker import Faker

def generateFirstName(fake: Faker) -> str:
    return fake.first_name()

def generateLastName(fake: Faker) -> str:
    return fake.last_name()

def generateFullName(fake: Faker) -> str:
    return fake.name()