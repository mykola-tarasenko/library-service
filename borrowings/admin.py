# Register your models here.
from django.contrib import admin

from borrowings.models import Borrowing


@admin.register(Borrowing)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        "book",
        "user__email",
        "borrow_date",
        "expected_return_date",
        "actual_return_date",
    )
