from holding.models import Holding


class MyHoldingService:
    def __init__(self, holding: Holding = Holding):
        self.holding = holding

    def get_my_holding(self, user):
        return self.holding.objects.filter(user=user).prefetch_related("market")