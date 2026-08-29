from cryptography.fernet import Fernet


class EncryptionManager:

    """
    Generic Encryption Utility
    """

    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()

    def decrypt(self, encrypted_data: str) -> str:
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()

    def rotate_key(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_dict(self, data: dict):
        import json
        return self.encrypt(json.dumps(data))

    def decrypt_dict(self, encrypted_data: str):
        import json
        decrypted = self.decrypt(encrypted_data)
        return json.loads(decrypted)

    def secure_compare(self, a: str, b: str):
        return a == b

    def hash_data(self, data: str):
        import hashlib
        return hashlib.sha256(data.encode()).hexdigest()