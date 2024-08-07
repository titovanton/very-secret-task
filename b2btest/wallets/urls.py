from rest_framework import routers

from wallets.views import WalletViewSet, TransactionViewSet

router = routers.SimpleRouter()
router.register('wallets', WalletViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = router.urls
