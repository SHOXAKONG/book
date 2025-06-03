from django.contrib import admin
from .models import Author, Book, Cart, Blog, Code

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'date_birth')
    search_fields = ('fullname',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'count', 'genre', 'add_to_cart')
    list_filter = ('genre', 'author')
    search_fields = ('title', 'author__fullname')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'took_date', 'book_count')
    list_filter = ('took_date',)
    search_fields = ('user__username', 'book__title')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'updated')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('code_number', 'user', 'expired_data')
    list_filter = ('expired_data',)
    search_fields = ('user__username', 'code_number')

