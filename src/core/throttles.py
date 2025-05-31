from rest_framework.throttling import AnonRateThrottle


class OneMinuteAnonThrottle(AnonRateThrottle):
    rate = "1/min"