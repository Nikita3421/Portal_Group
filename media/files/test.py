import csv
from faker import Faker
from random import randint

fake = Faker('uk_UA')

with open('names.csv', 'w', newline='',encoding='utf-8') as csvfile:
    fieldnames = ['name', 'amount']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    print(fake.name())
    writer.writeheader()
    for i in range(100):
        writer.writerow({'name': str(fake.name()), 'amount': str(randint(1,100))})


