from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# Initialize the PasswordHasher instance
ph = PasswordHasher()

def hash_otp(otp_code: str) -> str:
    """
    Hashes the given OTP code using Argon2.

    Args:
        otp_code (str): The OTP code to hash.

    Returns:
        str: The hashed OTP code.
    """
    return ph.hash(otp_code)

def verify_otp(hashed_otp: str, otp_code: str) -> bool:
    """
    Verifies the provided OTP code against the hashed OTP.

    Args:
        hashed_otp (str): The previously hashed OTP code.
        otp_code (str): The OTP code to verify.

    Returns:
        bool: True if the OTP code matches the hashed OTP, False otherwise.
    """
    try:
        return ph.verify(hashed_otp, otp_code)
    except VerifyMismatchError:
        return False
