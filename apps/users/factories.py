import factory
from factory.django import DjangoModelFactory

from apps.users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("email",)

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    is_active = True
    school = factory.Faker("company")
