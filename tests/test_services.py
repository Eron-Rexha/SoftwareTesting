from datetime import timedelta
from unittest.mock import patch

from app.services import verify_password, hash_password, create_access_token

def test_password_hashing():
    """Unit Test: Ensure passwords are encrypted and verified correctly."""
    password = "secret_password123"
    # We use the name hash_password to match services.py
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

def test_create_access_token():
    """Unit Test: Ensure JWT tokens are generated with correct data."""
    data = {"sub": "eron_user"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 20  # JWTs should be long, encoded strings

def test_hash_password_uses_passlib_context():
    """Unit Test with patch: isolate passlib and verify our wrapper delegates correctly."""
    with patch("app.services.pwd_context.hash", return_value="mocked-hash") as mock_hash:
        hashed = hash_password("plain-secret")

    assert hashed == "mocked-hash"
    mock_hash.assert_called_once_with("plain-secret")

def test_create_access_token_calls_jwt_encode():
    """Unit Test with patch: isolate JWT encoding and verify payload forwarding."""
    with patch("app.services.jwt.encode", return_value="encoded-token") as mock_encode:
        token = create_access_token({"sub": "mock-user"}, expires_delta=timedelta(minutes=5))

    assert token == "encoded-token"
    payload = mock_encode.call_args.args[0]
    assert payload["sub"] == "mock-user"
    assert "exp" in payload
