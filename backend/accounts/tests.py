from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse


User = get_user_model()


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.login_url = reverse('accounts:login')

    def test_user_exists(self):
        self.assertEqual(self.user, User.objects.get(username='testuser'))

    def test_user_login(self):
        logged_in = self.client.login(username='testuser', password='testpass123')
        user = get_user(self.client)
        
        self.assertTrue(logged_in)
        self.assertTrue(user.is_authenticated)


    def test_user_login_with_username(self):
        response = self.client.post(
            self.login_url, 
            {
                'username': 'testuser',
                'password': 'testpass123'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_login_with_email(self):
        response = self.client.post(
            self.login_url, 
            {
                'username': 'testuser@example.com',
                'password': 'testpass123'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('accounts:login')
        self.logout_url = reverse('accounts:logout')

        self.client.post(
            self.login_url,
            {
                'username': 'testuser',
                'password': 'testpass123',
            },
        )

    def test_logout_with_post_request(self):
        response = self.client.post(self.logout_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout_with_get_request(self):
        response = self.client.get(self.logout_url)

        self.assertEqual(response.status_code, 405)
