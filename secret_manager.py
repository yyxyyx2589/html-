from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
class SecretManager:
    def __init__(self, key_file='serect.key'):
        self.key_file = key_file
        self._fernet = None

    def _load_key(self):
        if self._fernet is not None:
            return self._fernet
        if not os.path.exists(self.key_file):
            raise FileNotFoundError(f'密钥文件不存在：{self.key_file}')
        with open(self.key_file, 'rb') as f:
            key = f.read()
        self._fernet = Fernet(key)
        return self._fernet

    def encrypt_env(self, source: str = '.env', target: str = '.env.enc', k_path: str = 'serect.key'):
        # 加密 .env文件
        with open(k_path, 'rb') as f:
            k = f.read()

        # 加密并保存
        fer = Fernet(k)
        with open(source, 'rb') as f:
            raw = f.read()
        cipher_data = fer.encrypt(raw)

        with open(target, 'wb') as f:
            f.write(cipher_data)
        print(f"加密文件已保存到：{target}")

    def decrypt_env(self, enc_file='.env.enc'):
        # 解密.env.enc 并加载到环境变量
        f = self._load_key()
        with open(enc_file, 'rb') as file:
            dec = f.decrypt(file.read())

        with open('.env.tmp', 'wb') as tmp:
            tmp.write(dec)

        with open(enc_file, 'rb') as file:
            dec = f.decrypt(file.read())

        # 导入临时明文文件 .env.tmp
        with open('.env.tmp', 'wb') as tmp:
            tmp.write(dec)

        # dotenv加载临时配置
        load_dotenv('.env.tmp')
        print("解密完成，环境变量已加载")

    def create_key(self, save_path: str = 'serect.key'):
        # 生成密钥
        key = Fernet.generate_key()
        with open(save_path, 'wb') as fp:
            fp.write(key)
        return key