from enum import Enum


class OtpSettings(Enum):
    MAX_ATTEMPTS = 5
    BLACKLIST_MULTIPLIER = 2
    OTP_EXPIRATION_TIME = 2
