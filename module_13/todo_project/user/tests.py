from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User


class RegistrationTest(TestCase):

    def _register_user(self, username, password):
        response = self.client.post(
            reverse('auth:register'),
            data=dict(username=username, password=password)
        )
        return response

    def test_redirect(self):
        response = self.client.get(reverse('todo:index'))
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.headers['Location'],
            reverse('auth:login') + '?next=/todo/'
        )

    def test_register(self):
        username = 'test'
        response = self._register_user(username, 'test')
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.headers['Location'],  reverse('auth:login'))
        user = User.objects.filter(username=username).first()
        self.assertTrue(user)

    def test_login(self):
        username = 'test'
        password = 'test'
        self._register_user(username, password)
        response = self.client.post(
            reverse('auth:login'),
            data=dict(username=username, password=password)
        )
        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(response.headers['Location'], reverse('todo:index'))

        response = self.client.get(
            reverse('todo:index'),
        )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 4)
        self.assertTrue(isinstance(tasks, QuerySet))
