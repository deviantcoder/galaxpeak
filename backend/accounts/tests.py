from django.test import TestCase
from django.contrib.auth import get_user_model, get_user
from django.urls import reverse


User = get_user_model()


class TestUserLogin(TestCase):
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


class TestUserLogout(TestCase):
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


class TestUserSignup(TestCase):
    def setUp(self):
        self.signup_url = reverse('accounts:signup')
        self.login_url = reverse('accounts:login')

    def send_signup_post_request(self, email, username, password1, password2, follow=True):
        response = self.client.post(
            self.signup_url,
            {
                'email': email,
                'username': username,
                'password1': password1,
                'password2': password2,
            },
            follow=follow
        )
        return response

    def test_user_signup(self):
        response = self.send_signup_post_request(
            'testuser@example.com', 'testuser', 'testpass123', 'testpass123'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_created_in_database(self):
        self.send_signup_post_request(
            'testuser@example.com', 'testuser', 'testpass123', 'testpass123'
        )
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_authenticated_user_cannot_access_signup_page(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        
        response = self.client.post(
            self.login_url, 
            {
                'username': 'testuser',
                'password': 'testpass123'
            },
            follow=True
        )

        response = self.client.get(self.signup_url)
        self.assertTrue(response.status_code, 302)

        response = self.client.get(self.signup_url, follow=True)
        self.assertTrue(response.status_code, 200)
        self.assertRedirects(response, reverse('accounts:test'))

    def test_signup_passwords_dont_match(self):
        response = self.send_signup_post_request(
            'testuser@example.com', 'testuser', 'testpass123', '123testpass'
        )
        self.assertIn(
            "password fields didn’t match",
            response.context.get('form').errors.get('password2')[0]
        )

    def test_signup_username_already_taken(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

        response = self.send_signup_post_request(
            'testuser2@example.com', 'testuser', 'testpass123', 'testpass123'
        )
        self.assertIn(
            "already exists",
            response.context.get('form').errors.get('username')[0]
        )
    
    def test_signup_email_already_taken(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

        response = self.send_signup_post_request(
            'testuser@example.com', 'testuser2', 'testpass123', 'testpass123'
        )
        self.assertIn(
            "already exists",
            response.context.get('form').errors.get('email')[0]
        )

    def test_signup_invalid_email(self):
        response = self.send_signup_post_request(
            'testuser@', 'testuser', 'testpass123', 'testpass123'
        )
        self.assertIn(
            "Enter a valid email address.",
            response.context.get('form').errors.get('email')[0]
        )
    
    def test_new_user_logged_in_after_signup(self):
        response = self.send_signup_post_request(
            'testuser@example.com', 'testuser', 'testpass123', 'testpass123'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, 'testuser')

    def test_signup_form_contains_csrf(self):
        response = self.client.get(self.signup_url)
        self.assertContains(response, 'csrfmiddlewaretoken')
