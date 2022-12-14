import pytest

@pytest.mark.django_db
def test_user_user_factory(user_factory):
   user = user_factory(has_default_group=True)
   assert user.username == 'JohnDoe_0'
   assert user.email == 'JohnDoe_0@mail.com'
   assert user.check_password('pass')
   assert user.groups.count() == 1