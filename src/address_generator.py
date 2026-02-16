from faker import Faker
from helpers import generateRandomList
import re
from exceptions import InvalidGenerationException
from address import Address

from typing import Union
from typing import Match

def generateCompanyName(fake: Faker) -> str:
    return fake.company()

def generateCompanyNameList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[str]:
    return generateRandomList(lambda: fake.company(), size, unique, maxUniqueFailsMultiplier)

addressReg = r'^(.*) (\d+(?:[\-/]\d+|[a-z])?)\n(\d{5}) (.*?)\s*$'

def generateAddress(fake: Faker) -> Address:
    address: str = fake.address()
    matcher: Union[Match[str], None] = re.match(addressReg, address)
    if not matcher:
        raise InvalidGenerationException()
    return Address(matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4))

def generateAddressList(fake: Faker, size: int) -> list[Address]:
    addresses: list[Address] = []
    for _ in range(size):
        address = fake.address()
        matcher = re.match(addressReg, address)
        if not matcher:
            raise InvalidGenerationException(address + " is not a valid address")
        addresses.append(Address(matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4)))
    return addresses