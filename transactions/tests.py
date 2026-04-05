from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from accounts.models import CustomUser
from books.models import Book
from .models import BorrowRecord


class BorrowReturnTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.student = CustomUser.objects.create_user(
            username='student1',
            password='TestPass@123',
            role=CustomUser.STUDENT,
            member_id='MEM001'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Author',
            isbn='1234567890123',
            category='Science',
            year=2022,
            total_copies=2,
            available_copies=2
        )
        self.client.login(
            username='student1', password='TestPass@123'
        )

    def test_student_can_borrow_book(self):
        response = self.client.get(
            reverse('transactions:borrow', args=[self.book.pk])
        )
        self.book.refresh_from_db()
        self.assertEqual(BorrowRecord.objects.count(), 1)
        self.assertEqual(self.book.available_copies, 1)

    def test_cannot_borrow_same_book_twice(self):
        self.client.get(
            reverse('transactions:borrow', args=[self.book.pk])
        )
        self.client.get(
            reverse('transactions:borrow', args=[self.book.pk])
        )
        self.assertEqual(BorrowRecord.objects.count(), 1)

    def test_cannot_borrow_unavailable_book(self):
        self.book.available_copies = 0
        self.book.save()
        self.client.get(
            reverse('transactions:borrow', args=[self.book.pk])
        )
        self.assertEqual(BorrowRecord.objects.count(), 0)

    def test_student_can_return_book(self):
        self.client.get(
            reverse('transactions:borrow', args=[self.book.pk])
        )
        record = BorrowRecord.objects.first()
        self.client.post(
            reverse('transactions:return', args=[record.pk])
        )
        record.refresh_from_db()
        self.assertEqual(record.status, 'returned')
        self.book.refresh_from_db()
        self.assertEqual(self.book.available_copies, 2)

    def test_due_date_is_14_days_from_today(self):
        self.client.get(
            reverse('transactions:borrow', args=[self.book.pk])
        )
        record = BorrowRecord.objects.first()
        expected_due = date.today() + timedelta(days=14)
        self.assertEqual(record.due_date, expected_due)


class FineCalculationTest(TestCase):

    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student1',
            password='TestPass@123',
            role=CustomUser.STUDENT,
            member_id='MEM001'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Author',
            isbn='1234567890001',
            category='Science',
            year=2022,
            total_copies=1,
            available_copies=1
        )

    def test_no_fine_when_returned_on_time(self):
        record = BorrowRecord.objects.create(
            user=self.student,
            book=self.book,
            due_date=date.today() + timedelta(days=5),
            return_date=date.today(),
            status='returned'
        )
        self.assertEqual(record.calculate_fine(), 0)

    def test_fine_calculated_correctly_for_late_return(self):
        record = BorrowRecord.objects.create(
            user=self.student,
            book=self.book,
            due_date=date.today() - timedelta(days=5),
            return_date=date.today(),
            status='returned'
        )
        self.assertEqual(record.calculate_fine(), 10.0)

    def test_fine_is_zero_for_on_time_return(self):
        record = BorrowRecord.objects.create(
            user=self.student,
            book=self.book,
            due_date=date.today(),
            return_date=date.today(),
            status='returned'
        )
        self.assertEqual(record.calculate_fine(), 0)