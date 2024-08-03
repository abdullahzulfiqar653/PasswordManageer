# utils.py

import random
import hashlib
from api.utils import WORDS


def generate_passphrase(num_words=16):
    return " ".join(random.choices(WORDS, k=num_words))


def hash_passphrase(passphrase):
    return hashlib.sha256(passphrase.encode()).hexdigest()


def verify_passphrase(input_passphrase, stored_hash):
    return hash_passphrase(input_passphrase) == stored_hash
