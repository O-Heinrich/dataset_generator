from faker import Faker

# Default to german words/names
localization = "de_DE"

fake = Faker(localization)

for i in range(10):
    date = fake.currency()
    print(date, type(date))