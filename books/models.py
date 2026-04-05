from django.db import models
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200, blank=True)
    year = models.IntegerField()
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True
    )
    description = models.TextField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_copies > 0

    class Meta:
        ordering = ['title']
