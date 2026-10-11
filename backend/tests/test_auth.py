from app.services.auth_service import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    raw_pass = "SecurePass123!"
    hashed = hash_password(raw_pass)
    assert hashed != raw_pass
    assert verify_password(raw_pass, hashed) is True
    assert verify_password("WrongPass", hashed) is False

def test_jwt_token_generation():
    token = create_access_token({"sub": "1", "email": "test@example.com"})
    payload = decode_access_token(token)
    assert payload["sub"] == "1"
    assert payload["email"] == "test@example.com"
