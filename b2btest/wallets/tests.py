"""
Usually, I write more tests, but for the sake of this task,
I'm going to cover only the "balance >= 0" condition.
Initially, I considered writing a test for race conditions,
but that would require refactoring the application to be
asynchronous, not just the tests. Another option would be
to have `Gunicorn` up and running and use a third-party script
with `httpx` to generate a large number of requests.
Maybe another time! :)
I believe I've demonstrated enough for now.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse

from wallets.models import Wallet


@pytest.mark.django_db
def test_update_balance_with_transaction(client):
    response = client.post(
        reverse('wallet-list'),
        {'label': 'Test Wallet', 'balance': 0},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert Wallet.objects.count() == 1
    wallet_id = response.json()['id']

    def create_transaction(amount: int):
        return client.post(
            reverse('transaction-list'),
            {
                'wallet': wallet_id,
                'txid': str(amount),
                'amount': amount,
            },
        )

    n = 10
    for i in range(1, n + 1):
        response = create_transaction(i)
        assert response.status_code == HTTPStatus.CREATED

    wallet = Wallet.objects.only('balance').get(id=wallet_id)
    s = n * (n + 1) / 2
    assert wallet.balance == s

    amount = -1 * (s + 1)
    response = create_transaction(amount)
    assert response.status_code == HTTPStatus.BAD_REQUEST
