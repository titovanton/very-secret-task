from django.db import transaction
from rest_framework.exceptions import ValidationError

from wallets.serializers import TransactionSerializer
from wallets.models import Wallet


def update_balance_with_transaction(
    serializer: TransactionSerializer
) -> None:
    """
    We expect that serializer is valid, so we don't
    need to check wallet existence.
    """

    wallet_id = serializer.validated_data['wallet'].id
    amount = serializer.validated_data['amount']

    with transaction.atomic():
        # Lock the wallet row for update
        wallet = Wallet.objects.select_for_update(
        ).only('balance').get(id=wallet_id)

        # Check if the wallet balance will be negative
        new_balance = wallet.balance + amount
        if new_balance < 0:
            raise ValidationError(
                'Insufficient funds in the wallet.'
            )

        # Create a new transaction
        serializer.save()

        # Update the wallet balance
        wallet.balance += amount
        wallet.save()
