from django.db import models
from django.urls import reverse
from django.contrib import admin
import uuid


class Genre(models.Model):
    """Genre model to represent genre of each book.

    Attributes
    ----------
    name : CharField
        The name of the genre, max_length = 200.

    Methods
    -------
    __str__ 
        returns string representation.
    """      

    name = models.CharField(max_length=200, help_text="Введите жанр книги")

    def __str__(self) -> str:
        """Return string representation as the name of the genre."""

        return str(self.name)


class Author(models.Model):
    """Author model class

    Has Meta class for ordering by (last_name, first_name).

    Attributes
    ----------
    first_name : CharField
        First name of the author, max_length = 100.
    last_name : CharField
        Last name of the author, max_length = 100.
    date_birth : DateField
        Date of the birth. Can be null and blank.
    date_death : DateField
        Date of the death (if the authord died). Can be null and blank

    Methods
    -------
    __str__
        Returns string representation as "{last name}, {first name}".
    get_absolute_url 
        Returns absolute url of each author.
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField(null=True, blank=True)
    date_death = models.DateField(null=True, blank=True)


    class Meta:
        ordering = ['last_name', 'first_name']


    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self) -> str:
        """Returns string representation as "{last name}, {first name}". """
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    """Book model to represent the book.

    Don't confuse with BookInstance class. Book class represents just a type of
    a book, just basic information, abstract book, whereas BookInstance class
    represents a real copy, physical one.

    Attributes
    ----------
    title : CharField
        The title of the book, max_length=200.
    author : ForeignKey
        The author of the book, can be null, on_delete = restrict.
        Point to author model class.
    summary : TextField
        Summary of the book, max_length=1000.
    isbn : CharField
        ISBN code. Must be unique for each book, max_length = 13.
    genre : ManyToManyField
        Point to Genre model class. Each book can have many genres.
        To print the genre(-s) on the site use display_genre method (see below). 
    LANGUAGES : list
        For choices for lang attribute.
        Description:
            'ru' : 'Russian'
            'en' : 'English'
            'de' : 'German'
            'es' : 'Spanish'
            'fr' : 'French'
            'it' : 'Italian'
    lang : CharField
        Get two character description from choices=LANGUAGES to show the language book written.

    Methods
    -------
    __str__
        Returns string representation as the title of the book.
    get_absolute_url 
        Returns absolute url of each book. Helpfull in admin site.
    display_genre
        Returns string representation of genres as 'Genre1, Genre2, ...'.
        Used in admin.py for representating genres of the book because
        ManyToManyFielf isn't supported in to print.
        For more information see https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#modeladmin-objects
    """

    title = models.CharField(
        max_length=200
        )
    author = models.ForeignKey(
        Author, 
        on_delete=models.RESTRICT, 
        null=True
        )
    summary = models.TextField(
        max_length=1000, 
        help_text="Введите краткое описание"
        )
    isbn = models.CharField(
        'ISBN', 
        max_length=13,
        unique=True,
        help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>'
        )
    genre = models.ManyToManyField(
        Genre,
        help_text="Выберите жанр книги"
        )

    LANGUAGES = (
        ('ru', 'Russian'),
        ('en', 'English'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('it', 'Italian'),
    )

    lang = models.CharField(
        max_length=2,
        choices=LANGUAGES,
        help_text="Выберите язык, на котором написана книга.",
        default='ru'
        )


    def __str__(self) -> str:
        """Returns string representation as title of the book."""

        return str(self.title)

    def get_absolute_url(self):
        """Returns absolute url of each book."""

        return reverse('book-detail', args=[str(self.id)])

    @admin.display(description="Жанры книги")
    def display_genre(self) -> str:
        """Returns string containing all genres book has
        
        Format of string: "GenreName1, GenreName2, ..."
        """

        return ', '.join(genre.name for genre in self.genre.all())


class BookInstance(models.Model):
    """The model of a physical copy of the book.

    uuid package must be imported because of the models.UUIDField. Has class Meta for ordering
    by (last_name, first_name).

    Attributes
    ----------
    id : UUIDField
        Primary key, a unique ID for each instance of the book, calculated by uuid4.
    book : ForeignKey
        Point to the corresponding book. on_delete = restrict, can be null.
    imprint : CharField
        Represents the imprint the book was printed in. max_length=200
    due_back : DateField
        Date when the book must be given back. Can be null and blank
    LOAN_STATUS : list
        List to be given as choices for status attribute.
        Description:
            'm' : 'Maintenance'
            'o' : 'On loan'
            'a' : 'Available'
            'r' : 'Reserved'
    status : CharField
        Status of the book. Can be blank, default : 'm', choices : LOAN_STATUS

    Methods
    -------
    __str__
        Returns string representation as "{ID} ({Title of the corresponding book})" 
    """

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        help_text="Уникальный ID для каждой книги"
        )
    book = models.ForeignKey(
        'Book', 
        on_delete=models.RESTRICT, 
        null=True
        )
    imprint = models.CharField(
        max_length=200
        )
    due_back = models.DateField(
        null=True, 
        blank=True
        )

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
        ordering = ['status']


    def __str__(self) -> str:
        """Returns string representation as "{ID} ({Title of the corresponding book})" """

        return f"{self.id} ({self.book.title})"