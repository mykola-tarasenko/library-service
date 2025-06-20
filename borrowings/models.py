from django.contrib.auth import get_user_model
from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="borrowings"
    )

    def __str__(self):
        return f'{self.user} borrowed "{self.book}" on {self.borrow_date}'
