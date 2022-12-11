from django import urls
import pytest
import requests

# test - ответы сервера по указанным страницам, адреса берутся из urls
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


def test_no_render():
    response = requests.get('https://navigatorway.com/testout/')
    assert response.status_code == 404