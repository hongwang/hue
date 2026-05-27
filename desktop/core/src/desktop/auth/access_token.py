import logging
from cryptography.fernet import Fernet

LOG = logging.getLogger()

# 生成密钥方法: Fernet.generate_key()
SECRET_KEY = b'DfMOQeBEXmOG5XzmLFRErl2W5SP2s8GLSi2RoO9HDJc='

cipher = Fernet(SECRET_KEY)

def encode_token(password):
    if not password:
        return None

    try:
        # Fernet 返回的是 bytes，需要解码为 string
        return cipher.encrypt(password.encode('utf-8')).decode('utf-8')
    except Exception as e:
        LOG.error("Failed to encrypt password: %s" % str(e))
        return None

def decrypt_token(token):
    if not token:
        return None

    try:
        return cipher.decrypt(token.encode('utf-8')).decode('utf-8')
    except Exception as e:
        LOG.error("Failed to decrypt token: %s" % str(e))
        return None