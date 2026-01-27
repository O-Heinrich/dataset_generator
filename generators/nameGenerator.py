from faker import Faker
from generators.helpers import generateRandomList

def generateFirstName(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    return fake.first_name()

def generateFirstNameList(fake, size, unique=False, maxUniqueFailsMultiplier=3):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: fake.first_name(), size, unique, maxUniqueFailsMultiplier)

def generateLastName(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    return fake.last_name()

def generateLastNameList(fake, size, unique=False, maxUniqueFailsMultiplier=3):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: fake.last_name(), size, unique, maxUniqueFailsMultiplier)

def generateFullName(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    return fake.name()

def generateFullNameList(fake, size, unique=False, maxUniqueFailsMultiplier=3):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: fake.name(), size, unique, maxUniqueFailsMultiplier)