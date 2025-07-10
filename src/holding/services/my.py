from account.models import Account
from holding.models import Holding


class MyHoldingService:
    def __init__(self, holding: Holding = Holding, account: Account = Account):
        self.holding = holding
        self.account = account

    def get_my_holding(self, user):
        return self.holding.objects.filter(user=user).select_related("market")
