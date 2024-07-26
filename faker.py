import main,models
from faker import Faker
faker=Faker()

db = next(main.get_db())
for _ in range(1000):
    fake_book = models.Books(
        name=faker.text(max_nb_chars=20),
        writer=faker.name(),
        number=faker.random_int(min=1, max=10000),
        published=faker.date_time_this_decade()
    )
    db.add(fake_book)
db.commit()
db.close()