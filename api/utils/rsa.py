from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes


def generate_keypair(passphrase: bytes = None):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    public_key = private_key.public_key()
    try:
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=(
                serialization.BestAvailableEncryption(passphrase)
                if passphrase
                else serialization.NoEncryption()
            ),
        )
    except Exception as e:
        print(e)

    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem_private_key, pem_public_key


def encrypt_messages(message, public_keys_pem):
    encrypted_messages = []

    for pem_public_key in public_keys_pem:
        public_key = serialization.load_pem_public_key(pem_public_key.encode("utf-8"))
        encrypted_message = public_key.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        encrypted_messages.append(encrypted_message)
    encrypted_message = "-".join([msg.hex() for msg in encrypted_messages])
    return encrypted_message


def decrypt_message(encrypted_messages, private_key_pem, passphrase):
    encrypted_messages = [
        bytes.fromhex(hs) for hs in encrypted_messages.split("-") if hs
    ]
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=passphrase,
    )

    for msg in encrypted_messages:
        try:
            decrypted_message = private_key.decrypt(
                msg,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            return decrypted_message
        except:
            pass
