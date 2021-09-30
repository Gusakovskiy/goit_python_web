from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.timezone import now

manager = models.Manager()

_PRIVATE_ACCOUNT = 'P'
_BUSINESS_ACCOUNT = 'B'
_ACCOUNT_CHOICES = (
    (_PRIVATE_ACCOUNT, 'Private'),
    (_BUSINESS_ACCOUNT, 'Business'),
)


def _default_end():
    return now() + timedelta(days=30)


class TodayManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        today = now().replace(hour=0, minute=0, second=0, microsecond=0)
        return qs.filter(create__gte=today).order_by('created')


class FinanceAccount(models.Model):
    name = models.TextField()
    type = models.CharField(
        max_length=1,
        choices=_ACCOUNT_CHOICES,
    )
    # ONE TO ONE RELATION SHIP
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User personal account",
        related_name="accounts",
    )


class Budget(models.Model):
    start = models.DateTimeField(
        default=now,
        verbose_name="Start of the budget",
    )
    end = models.DateTimeField(
        default=_default_end,
        verbose_name="End of the budget",
    )
    balance = models.DecimalField(
        default=Decimal(0),
        max_digits=10,
        decimal_places=2,
    )
    start_balance = models.DecimalField(
        default=Decimal(0),
        max_digits=10,
        decimal_places=2,
    )
    account = models.ForeignKey(
        FinanceAccount,
        on_delete=models.CASCADE,
        verbose_name="User personal account",
        related_name="budgets",
    )


class TransactionCategory(models.Model):
    name = models.TextField(verbose_name="Name of category")
    code = models.CharField(max_length=10)


class Transaction(models.Model):
    created = models.DateTimeField(
        default=now,
        verbose_name="Created timestamp"
    )
    amount = models.DecimalField(
        null=False,
        max_digits=10,
        decimal_places=2,
    )
    budget = models.ForeignKey(
        Budget,
        on_delete=models.CASCADE,
        verbose_name="Transaction in the budget",
        related_name="transactions",
    )
    categories = models.ManyToManyField(TransactionCategory)
    # categories = models.ManyToManyField(
    # TransactionCategory,
    # through='TransactionThroughCategory'
    # )

    objects = models.Manager()
    today_objects = TodayManager()


class TransactionThroughCategory(models.Model):
    person = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    group = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    created = models.DateField(default=now)


# model inheritance abstract True
# instance manager manager = models.Manager()
# queryset: https://docs.djangoproject.com/en/3.2/ref/models/querysets/
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#queryset-api
#   lazy
#   example queries
#   limiting and slicing LIMIT and OFFSET
#   len and count
#   values, only, values_list
# N+1 problems https://docs.djangoproject.com/en/3.2/ref/models/querysets/#prefetch-related
# select_related
# prefetch_related
#


