import os
import tempfile
import sqlite3
import time

from app.database import init_db, save_secret, get_and_delete_secret
from cryptography.fernet import Fernet

# Use a temporary test DB to isolate tests
TEST_DB = "test_secrets.db"

def setup_module(module):
    # Override DB for tests
    from app import database
    database.DB_NAME = TEST_DB
    init_db()

def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_secret_creation():
    secret = "Hello pytest!"
    key = save_secret(secret, 10)  # 10-minute expiry
    assert isinstance(key, str)
    assert len(key) > 0

def test_encryption_and_decryption():
    secret = "Encrypt me"
    key = save_secret(secret, 10)
    result = get_and_delete_secret(key)
    assert result == secret

def test_expiration_logic():
    secret = "Short-lived secret"
    key = save_secret(secret, 0)  # 0-minute expiration
    time.sleep(1.5)  # wait to ensure it's expired
    result = get_and_delete_secret(key)
    assert result is None
