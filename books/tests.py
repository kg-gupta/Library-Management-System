from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from .models import Book


class BookModelTest(TestCase):

    def setUp(self):
        self.book = Book.objects.create(
            title='Python Programming',
            author='John Smith',
            isbn='1234567890123',
            category='Technology',
            year=2022,
            total_copies=3,
            available_copies=3
        )

    def test_book_str(self):
        self.assertEqual(
            str(self.book),
            'Python Programming by John Smith'
        )

    def test_book_is_available(self):
        self.assertTrue(self.book.is_available())

    def test_book_not_available_when_zero_copies(self):
        self.book.available_copies = 0
        self.book.save()
        self.assertFalse(self.book.is_available())


class BookViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = CustomUser.objects.create_user(
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
        self.book = Book.objects.create(
            title='Django for Beginners',
            author='Jane Doe',
            isbn='9876543210123',
            category='Technology',
            year=2023,
            total_copies=2,
            available_copies=2
        )

    def test_book_list_accessible_without_login(self):
        response = self.client.get(reverse('books:list'))
        self.assertEqual(response.status_code, 200)

    def test_book_detail_accessible(self):
        response = self.client.get(
            reverse('books:detail', args=[self.book.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django for Beginners')

    def test_student_cannot_add_book(self):
        self.client.login(username='student1', password='TestPass@123')
        response = self.client.post(reverse('books:add'), {
            'title': 'Test Book',
            'author': 'Author',
            'isbn': '1111111111111',
            'category': 'Fiction',
            'year': 2023,
            'total_copies': 1,
            'available_copies': 1,
        })
        self.assertRedirects(response, reverse('books:list'))
        self.assertEqual(Book.objects.count(), 1)

    def test_admin_can_add_book(self):
        self.client.login(username='admin1', password='AdminPass@123')
        response = self.client.post(reverse('books:add'), {
            'title': 'New Book',
            'author': 'New Author',
            'isbn': '5555555555555',
            'category': 'Science',
            'year': 2023,
            'total_copies': 2,
            'available_copies': 2,
        })
        self.assertEqual(Book.objects.count(), 2)

    def test_book_search_works(self):
        response = self.client.get(
            reverse('books:list') + '?q=Django'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django for Beginners')