"""
You might expect me to handle the race condition here,
but I prefer to keep the serializer atomic in relation
to the Model. The only dependency it may have is the
user system. Moreover, we need to group validation,
transaction creation, and wallet update in
a single transaction. I can't see how to achieve this
while following the standard ModelSerializer architecture.
"""

from rest_framework import serializers

from wallets.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
