from rest_framework.throttling import AnonRateThrottle


class ThirtySecondAnonThrottle(AnonRateThrottle):
    rate = "1/min"