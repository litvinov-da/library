from django.db import models
from django.urls import reverse
import uuid


class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self) -> str:
        return str(self.name)

    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание")
    isbn = models.CharField(
        'ISBN', 
        max_length=13,
        unique=True,
        help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>'
        )
    genre = models.ManyToManyField(Genre,
        help_text="Выберите жанр книги")

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
        help_text="Уникальный ID для каждой книги")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Доступность книги'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self) -> str:
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField(null=True, blank=True)
    date_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"

    