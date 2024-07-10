# utils.py

import random
import hashlib
from english_words import get_english_words_set

web2lowerset = get_english_words_set(['web2'], lower=True)

def generate_passphrase(num_words=6):
    return ' '.join(random.choices(list(web2lowerset), k=num_words))

def hash_passphrase(passphrase):
    return hashlib.sha256(passphrase.encode()).hexdigest()

def verify_passphrase(input_passphrase, stored_hash):
    return hash_passphrase(input_passphrase) == stored_hash
