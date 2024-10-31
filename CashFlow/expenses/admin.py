# admin.py

from django.contrib import admin
from .models import Budget, Expense

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('amount', 'date_added')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'currency', 'amount_in_usd', 'date_added')

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        # Pass total budget, total spent, and balance to the template
        extra_context['total_budget'] = Expense.total_budget()
        extra_context['total_spent'] = Expense.total_spent()
        extra_context['balance'] = Expense.balance()
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Budget, BudgetAdmin)
admin.site.register(Expense, ExpenseAdmin)
