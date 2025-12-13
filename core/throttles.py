from rest_framework.throttling import AnonRateThrottle


class OneMinuteAnonRateThrottle(AnonRateThrottle):
    rate = "1/min"
