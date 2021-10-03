from decimal import Decimal

import django
django.setup()

from model_bakery import baker


def main():

    user = baker.make('auth.User')
    user.set_password('test')
    user.save()
    account = baker.make(
        'finance.FinanceAccount',
        user=user
    )
    budget = baker.make(
        'finance.Budget',
        account=account,
        start_balance=Decimal(-14.0)
    )
    transaction = baker.make(
        'finance.Transaction',
        budget=budget,
        amount=Decimal(-14.0),
    )


if __name__ == '__main__':
    main()