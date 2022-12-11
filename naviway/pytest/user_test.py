from django.urls import reverse
from django.contrib.auth.models import User
import uuid
import pytest

# тест просто подключения к БД
@pytest.mark.django_db
def test_reg_us():
    pass


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('user', 'user@mail.com', 'password')
  assert User.objects.count() == 1


# подключение неавторизованного, тут разрешено, если страница запрещена 302 код ответа от сервера
@pytest.mark.django_db
def test_view_unauthorized(client):
   url = reverse('cardbasic')
   response = client.get(url)
   assert response.status_code == 302

# главная страница разрешена неавторизованным
@pytest.mark.django_db
def test_view_as_admin2(client):
   url = reverse('home')
   response = client.get(url)
   assert response.status_code == 200

# авторизованный - как admin
@pytest.mark.django_db
def test_view_as_admin(admin_client):
   url = reverse('cardbasic')
   response = admin_client.get(url)
   assert response.status_code == 200


# дальше видимо не годится страница входа - возможно у мну ее нету
# @pytest.fixture
# def create_user(db, django_user_model, test_password):
#     def make_user(**kwargs):
#         kwargs['password'] = test_password
#         if 'username' not in kwargs:
#             kwargs['username'] = str(uuid.uuid4())
#         return django_user_model.objects.create_user(**kwargs)
#     return make_user
#
# @pytest.mark.django_db
# def test_user_detail(client, create_user):
#    user = create_user(username='someone')
#    url = reverse('arh', kwargs={'pk': user.pk})
#    response = client.get(url)
#    assert response.status_code == 200
#    assert 'someone' in response.content
#
# @pytest.mark.django_db
# def test_superuser_detail(client, create_user):
#    admin_user = create_user(
#        username='custom-admin-name',
#        is_staff=True, is_superuser=True
#    )
#    url = reverse(
#        'superuser-detail-view', kwargs={'pk': admin_user.pk}
#    )
#    response = client.get(url)
#    assert response.status_code == 200
#    assert 'custom-admin-name' in response.content