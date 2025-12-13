from rest_framework.throttling import AnonRateThrottle


class TwoRequestPerOneMinuteAnonRateThrottle(AnonRateThrottle):
    rate = "2/min"
