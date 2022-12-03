# from navigator.naviway.views2 import check_navi
# from .. import views
from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
import pytest

# test по идее тестирует ответы сервера по указанным страницам, адреса берутся из urls
@pytest.mark.django_db
@pytest.mark.parametrize('param', [
    ('home'),
    ('content'),
    ('arh'),
    ('tehtarget'),
    ('tehnik'),
    ('tehnikcource'),
    ('tehnik_one'),
    ('login'),
    ('registr'),
    ('logout'),
])
def test_render_views(client, param):
    if param == 'tehnikcource' or param == 'tehnik' or param == 'tehnik_one':
        temp_url = urls.reverse(param, args=[11])
    elif param == 'content':
        temp_url = urls.reverse(param, args=['book_nav'])
    else:
        temp_url = urls.reverse(param)
    print(temp_url)
    resp = client.get(temp_url)
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_as_admin(admin_client):
   url = urls.reverse('home')
   response = admin_client.get(url)
   assert response.status_code == 200

@pytest.mark.django_db
def test_reg_us():
    pass


@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('user', 'user@mail.com', 'password')
  assert User.objects.count() == 1


@pytest.fixture
def test_password():
    return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)
    return make_user

# дальше что то видимо со страницей входа (login не работает видимо)
@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('user', 'user@mail.com', 'password')
  assert User.objects.count() == 1

@pytest.mark.django_db
def test_user_detail(client, create_user):
   user = create_user(username='someone')
   url = urls.reverse('registr', kwargs={'pk': user.pk})
   response = client.get(url)
   assert response.status_code == 200
   assert 'someone' in response.content

@pytest.mark.django_db
def test_superuser_detail(client, create_user):
   admin_user = create_user(
       username='custom-admin-name',
       is_staff=True, is_superuser=True
   )
   url = urls.reverse('registr', kwargs={'pk': admin_user.pk})
   response = client.get(url)
   assert response.status_code == 200
   assert 'custom-admin-name' in response.content
