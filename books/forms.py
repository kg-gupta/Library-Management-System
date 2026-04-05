from django import forms
from .models import Book

CATEGORY_CHOICES = [
    ('', 'Select a category'),
    ('Fiction', 'Fiction'),
    ('Non-Fiction', 'Non-Fiction'),
    ('Science', 'Science'),
    ('Technology', 'Technology'),
    ('Mathematics', 'Mathematics'),
    ('History', 'History'),
    ('Biography', 'Biography'),
    ('Self-Help', 'Self-Help'),
    ('Reference', 'Reference'),
    ('Other', 'Other'),
]

class BookForm(forms.ModelForm):
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'category',
            'publisher', 'year', 'total_copies',
            'available_copies', 'cover_image', 'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'year': forms.NumberInput(attrs={'min': 1000, 'max': 2099}),
        }