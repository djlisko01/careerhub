from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from config import settings

ACCESS_TOKEN_EXPIRES_IN = timedelta(minutes=15)

password_hasher = PasswordHash.recommended()

class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass

class InactiveUserError(Exception):
    """Custom exception for inactive user errors."""
    pass

def hash_password(plain_password: str) -> str:
    """Hash the provided plain password.

    Args:
        plain_password: The plain text password to hash.

    Returns:
        The hashed password as a string.
    """
    return password_hasher.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the provided plain password matches the hashed password.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The hashed password to compare against.

    Returns:
        True if the passwords match, False otherwise.
    """
    return password_hasher.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_in: timedelta = ACCESS_TOKEN_EXPIRES_IN) -> str:
    """Create an access token with the provided data and expiration time.

    Args:
        data: The data to include in the token.
        expires_in: The duration for which the token is valid.

    Returns:
        The encoded JWT as a string.
    """
    expiration = datetime.now(timezone.utc) + expires_in
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGO)

def decode_access_token(token: str) -> dict:
    """Decode the provided access token.

    Args:
        token: The JWT to decode.

    Returns:
        The decoded token data as a dictionary.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGO])