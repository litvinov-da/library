from django.contrib import admin
from .models import Genre, Book, BookInstance, Author

admin.site.register(Genre)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'last_name', 'first_name',
        'date_birth', 'date_death'
    )

    ordering = ['last_name', 'first_name']

    fieldsets = (
        ('Имя и фамилия', {
            'fields': ('last_name', 'first_name')
        }),
        ('Годы жизни', {
            'fields': ('date_birth', 'date_death'),
            'description': ('Введите дату рождения и смерти.\
                            при отсутствии даты смерти оставьте поле пустым.')
        })
    )


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'display_genre', 'lang'
    )

    ordering = ['author']

    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = (
        'status', 'due_back', 'imprint'
    )
    list_display = (
        'book', 'status', 'borrower', 'due_back', 'id'
    )

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back', 'borrower'),
            'description': ("Статус книги, дата её возвращения и кем была занята (если была занята).")
        })
    )
