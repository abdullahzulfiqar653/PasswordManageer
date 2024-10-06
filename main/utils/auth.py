# utils.py
import string
import random
import secrets
import hashlib
from main.utils import WORDS


def generate_passphrase(num_words=16):
    return " ".join(random.choices(WORDS, k=num_words))


def hash_passphrase(passphrase):
    return hashlib.sha256(passphrase.encode()).hexdigest()


def verify_passphrase(input_passphrase, stored_hash):
    return hash_passphrase(input_passphrase) == stored_hash


def generate_random_password(length=15):
    return "".join(
        secrets.choice(string.ascii_letters + string.digits + string.punctuation)
        for _ in range(length)
    )
