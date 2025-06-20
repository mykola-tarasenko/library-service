from django.contrib import admin

from books.models import Book


@admin.register(Book)
class CityAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "cover", "inventory", "daily_fee")
    search_fields = ("title", "author")
