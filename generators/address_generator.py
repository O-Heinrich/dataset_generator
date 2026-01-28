from faker import Faker
from generators.helpers import generateRandomList
import re
from generators.exceptions import InvalidGenerationException
from generators.address import Address

def generateCompanyName(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    return fake.company()

def generateCompanyNameList(fake, size, unique=False, maxUniqueFailsMultiplier=3):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: fake.company(), size, unique, maxUniqueFailsMultiplier)

addressReg = r'^(.*) (\d+)\n(\d{5}) (.*?)\s*$'

def generateAddress(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    address = fake.address()
    matcher = re.match(addressReg, address)
    if not matcher:
        raise InvalidGenerationException()
    return Address(matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4))

def generateAddressList(fake, size):
    if not isinstance(fake, Faker):
        raise TypeError()
    addresses = []
    for _ in range(size):
        address = fake.address()
        matcher = re.match(addressReg, address)
        if not matcher:
            raise InvalidGenerationException()
        addresses.append(Address(matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4)))
    return addresses