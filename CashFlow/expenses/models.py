# models.py

from django.db import models
from django.utils import timezone

USD_TO_LL_RATE = 89500  # Exchange rate

class Budget(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Budget of ${self.amount} added on {self.date_added.date()}"


class Expense(models.Model):
    USD = 'USD'
    LL = 'LL'
    CURRENCY_CHOICES = [
        (USD, 'USD'),
        (LL, 'L.L.'),
    ]

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    date_added = models.DateTimeField(default=timezone.now)

    @property
    def amount_in_usd(self):
        # Convert the amount to USD and round to 2 decimal places
        if self.currency == self.USD:
            return round(self.amount, 2)  # Already in USD
        return round(self.amount / USD_TO_LL_RATE, 2)  # Convert L.L. to USD

    def __str__(self):
        return f"Expense of ${self.amount_in_usd:.2f} (USD) on {self.date_added.date()}"

    @classmethod
    def total_spent(cls):
        return sum(expense.amount_in_usd for expense in cls.objects.all())

    @classmethod
    def total_budget(cls):
        return sum(budget.amount for budget in Budget.objects.all())

    @classmethod
    def balance(cls):
        return cls.total_budget() - cls.total_spent()
