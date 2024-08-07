"""
Here are several notes:

1) I didn't see anything related to a user system in the task,
which is why I omitted permissions.

2) Both ViewSets will handle only GET and POST requests,
as I did not find any other instructions in the task.

3) I don't add ordering in the model because it
imposes overhead on database queries, and it might
not be needed in some places. However, sorting
needs to be specified in the controller; otherwise,
pagination will jump by ID.

4) Filtering is very basic, as I did not find any other
instructions in the task.
"""

from typing import override

from rest_framework import viewsets, mixins

from wallets.models import Wallet, Transaction
from wallets.serializers import WalletSerializer, TransactionSerializer
from wallets.services import update_balance_with_transaction


class BaseAPI(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class WalletViewSet(BaseAPI):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filterset_fields = 'label',
    ordering_fields = 'id', 'label', 'balance'
    ordering = 'id',


class TransactionViewSet(BaseAPI):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_fields = 'wallet', 'txid'
    ordering_fields = 'id', 'txid', 'amount'
    ordering = 'id',

    @override
    def perform_create(self, serializer):
        update_balance_with_transaction(serializer)
