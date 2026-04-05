from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser


class UserRegistrationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_registration_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')

    def test_student_can_register(self):
        response = self.client.post(self.register_url, {
            'username': 'teststudent',
            'first_name': 'Test',
            'last_name': 'Student',
            'email': 'test@test.com',
            'password1': 'TestPass@123',
            'password2': 'TestPass@123',
        })
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.first()
        self.assertEqual(user.role, CustomUser.STUDENT)

    def test_duplicate_username_fails(self):
        CustomUser.objects.create_user(
            username='existing', password='pass@1234'
        )
        response = self.client.post(self.register_url, {
            'username': 'existing',
            'password1': 'TestPass@123',
            'password2': 'TestPass@123',
        })
        self.assertEqual(CustomUser.objects.count(), 1)


class UserLoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')
        self.user = CustomUser.objects.create_user(
            username='student1',
            password='TestPass@123',
            role=CustomUser.STUDENT,
            member_id='MEM001'
        )
        self.admin = CustomUser.objects.create_user(
            username='admin1',
            password='AdminPass@123',
            role=CustomUser.ADMIN,
            member_id='MEM002'
        )

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_student_login_redirects_to_books(self):
        response = self.client.post(self.login_url, {
            'username': 'student1',
            'password': 'TestPass@123',
        })
        self.assertRedirects(response, reverse('books:list'))

    def test_admin_login_redirects_to_dashboard(self):
        response = self.client.post(self.login_url, {
            'username': 'admin1',
            'password': 'AdminPass@123',
        })
        self.assertRedirects(response, reverse('dashboard:home'))

    def test_wrong_password_fails(self):
        response = self.client.post(self.login_url, {
            'username': 'student1',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)