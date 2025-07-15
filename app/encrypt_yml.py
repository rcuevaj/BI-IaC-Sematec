import yaml
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode


# AES-256 requiere una clave de 32 bytes (256 bits)
AES_KEY = "AES_SEMATIC_PROJECT_SECRET_KEY_A"

KEY = AES_KEY.encode("utf-8")
IV = b"\x00" * 16

def encrypt(text: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return b64encode(encrypted).decode()

def decrypt(encrypted_text: str) -> str:
    encrypted_data = b64decode(encrypted_text)

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    return decrypted.decode()

# Leer YAML
with open("credential.yml", "r") as f:
    config = yaml.safe_load(f)

# Encriptar Credenciales DBSupabase
if config['app']['DBSupabase']['encrypted'] == 0:
    config['app']['DBSupabase']['user'] = encrypt(config['app']['DBSupabase']['user'])
    config['app']['DBSupabase']['password'] = encrypt(config['app']['DBSupabase']['password'])
    config['app']['DBSupabase']['port'] = encrypt(config['app']['DBSupabase']['port'])
    config['app']['DBSupabase']['name'] = encrypt(config['app']['DBSupabase']['name'])
    config['app']['DBSupabase']['host'] = encrypt(config['app']['DBSupabase']['host'])
    config['app']['DBSupabase']['encrypted'] = 1

    # Guardar en YAML (encriptado)
    with open("credential.yml", "w") as f:
        yaml.dump(config, f)
else:
    print("DBSupabase ya encriptado")

# Encriptar Credenciales SematecPlataform
if config['app']['DBSematecPlataform']['encrypted'] == 0:
    config['app']['DBSematecPlataform']['host'] = encrypt(config['app']['DBSematecPlataform']['host'])
    config['app']['DBSematecPlataform']['port'] = encrypt(config['app']['DBSematecPlataform']['port'])
    config['app']['DBSematecPlataform']['user'] = encrypt(config['app']['DBSematecPlataform']['user'])
    config['app']['DBSematecPlataform']['password'] = encrypt(config['app']['DBSematecPlataform']['password'])
    config['app']['DBSematecPlataform']['database'] = encrypt(config['app']['DBSematecPlataform']['database'])
    config['app']['DBSematecPlataform']['encrypted'] = 1

    # Guardar en YAML (encriptado)
    with open("credential.yml", "w") as f:
        yaml.dump(config, f)
else:
    print("DBSematecPlataform ya encriptado")

# Leer y desencriptar
with open("credential.yml", "r") as f:
    encrypted_config = yaml.safe_load(f)

encrypted_user = decrypt(encrypted_config['app']['DBSupabase']['user'])
print(f"Usuario desencriptado: {encrypted_user}")
encrypted_user_2 = decrypt(encrypted_config['app']['DBSematecPlataform']['user'])
print(f"Usuario desencriptado: {encrypted_user_2}")
