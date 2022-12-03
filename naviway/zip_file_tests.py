
# from django import test

# Create your tests here.
# class URLTests(test.TestCase):
#     def test_homepage(self):
#         response = self.client.get('/mine/pytest --version')
#         self.assertEqual(response.status_code, 404)

from django.test import TestCase

from .models import Podhod


class PodhodModelTests(TestCase):

    def test_absolute_url_is_correct(self):
        new_category = Podhod(name='Первый пост', slug='first-post')
        new_category.save()
        self.assertEqual(new_category.get_absolute_url(), '/category/first-post/')
