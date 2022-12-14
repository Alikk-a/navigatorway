from django.contrib.auth.models import User, Group
import pytest
import factory
from factory.django import DjangoModelFactory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'JohnDoe_{n}')
    email = factory.Sequence(lambda n: f'JohnDoe_{n}@mail.com')
    password = factory.PostGenerationMethodCall(
        'set_password', 'pass'
    )

    @factory.post_generation
    def has_default_group(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            default_group, _ = Group.objects.get_or_create(
                name='group'
            )
            self.groups.add(default_group)