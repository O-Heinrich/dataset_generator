from faker import Faker
import re
from exceptions import InvalidGenerationException
from address import Address

from typing import Union
from typing import Match

def generateCompanyName(fake: Faker) -> str:
    return fake.company()

addressReg = r'^(.*) (\d+(?:[\-/]\d+|[a-z])?)\n(\d{5}) (.*?)\s*$'

def generateAddress(fake: Faker) -> Address:
    address: str = fake.address()
    matcher: Union[Match[str], None] = re.match(addressReg, address)
    if not matcher:
        raise InvalidGenerationException()
    return Address(matcher.group(1), matcher.group(2), matcher.group(3), matcher.group(4))