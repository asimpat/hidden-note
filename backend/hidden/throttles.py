from rest_framework.throttling import AnonRateThrottle


class MessageAnonRateThrottle(AnonRateThrottle):
    scope = 'message_anon'
