from app.auth import hash_password, verify_password
from app.utils import generate_activation_key


def test_password_hashing():
    password = "12345678"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_generate_activation_key():
    key = generate_activation_key()

    assert isinstance(key, str)
    assert len(key) >= 32