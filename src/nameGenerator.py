from faker import Faker
from helpers import generateRandomList

def generateFirstName(fake: Faker) -> str:
    return fake.first_name()

def generateFirstNameList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[str]:
    return generateRandomList(lambda: fake.first_name(), size, unique, maxUniqueFailsMultiplier)

def generateLastName(fake: Faker) -> str:
    return fake.last_name()

def generateLastNameList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[str]:
    return generateRandomList(lambda: fake.last_name(), size, unique, maxUniqueFailsMultiplier)

def generateFullName(fake: Faker) -> str:
    return fake.name()

def generateFullNameList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[str]:
    return generateRandomList(lambda: fake.name(), size, unique, maxUniqueFailsMultiplier)