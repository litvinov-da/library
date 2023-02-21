from django.contrib import admin
from .models import Genre, Book, BookInstance, Author

admin.site.register(Genre)


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name', 'first_name',
        'date_birth', 'date_death'
    )

    fields = [
        'first_name', 'last_name', ('date_birth', 'date_death')
    ]

admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.StackedInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'display_genre'
    )

    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = (
        'status', 'due_back'
    )

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        })
    )

