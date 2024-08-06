from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=18,
        default=0
    )

    def __str__(self):
        return f'{self.label}:{self.balance}'


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet,
        related_name='transactions',
        on_delete=models.CASCADE
    )
    txid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=18)

    def __str__(self):
        return f'{self.txid}:{self.amount}'
