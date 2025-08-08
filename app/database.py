import os
import sqlite3
from uuid import uuid4
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables from .env (used for SECRET_KEY)
load_dotenv()

# Initialize Fernet encryption using the secret key from .env
fernet = Fernet(os.environ["SECRET_KEY"])

# SQLite database filename
DB_NAME = "secrets.db"


def init_db():
    """
    Initializes the SQLite database.
    Creates the 'secrets' table if it doesn't already exist.
    """
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS secrets (
                id TEXT PRIMARY KEY,          -- UUID key
                secret TEXT NOT NULL,         -- Encrypted secret text
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME           -- Expiration time (UTC)
            );
        """
        )
        conn.commit()


def save_secret(secret_text, expire_minutes):
    """
    Encrypts and stores a new secret in the database.

    Args:
        secret_text (str): The plaintext secret to be saved.
        expire_minutes (int): Minutes until the secret expires.

    Returns:
        str: The UUID key used to access the secret.
    """
    key = str(uuid4())
    expires_at = datetime.utcnow() + timedelta(minutes=expire_minutes)

    # Encrypt the secret before saving
    encrypted_secret = fernet.encrypt(secret_text.encode())

    # Store secret in DB
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO secrets (id, secret, expires_at) VALUES (?, ?, ?)",
            (key, encrypted_secret, expires_at.isoformat()),
        )
        conn.commit()

    return key


def get_and_delete_secret(key):
    """
    Retrieves and deletes a secret from the database by its key.

    - If the secret exists and is not expired, it is decrypted and returned.
    - If expired or not found, None is returned.
    - The secret is deleted whether expired or successfully retrieved.

    Args:
        key (str): The unique UUID of the secret.

    Returns:
        str | None: The decrypted secret string, or None if not found/expired.
    """
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT secret, expires_at FROM secrets WHERE id = ?", (key,))
        result = c.fetchone()

        if result:
            encrypted_secret, expires_at = result

            # Check expiration
            if datetime.utcnow() > datetime.fromisoformat(expires_at):
                c.execute("DELETE FROM secrets WHERE id = ?", (key,))
                conn.commit()
                return None

            # Delete immediately after viewing
            c.execute("DELETE FROM secrets WHERE id = ?", (key,))
            conn.commit()

            # Try to decrypt the secret
            try:
                decrypted_secret = fernet.decrypt(encrypted_secret).decode()
                return decrypted_secret
            except:
                return None

        return None
