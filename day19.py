from openai import OpenAI
import os
from dotenv import load_dotenv

#load_dotenv()
#api_key = os.getenv('DS_API_KEY')
#model=os.getenv('DEFAULT_MODEL','deepseek-chat')
#print(f"使用模型：{model}")

"""class LLM:
    PLATFORMS={
        'ds':{'api_key':os.getenv('DS_API_KEY'),
    'base_url':'https://api.deepseek.com/v1',
    'model':'deepseek-chat'
    },
        'qwen': {'api_key': os.getenv('QWEN_API_KEY'),
               'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
               'model': 'qwen-plus'
               }
    }


    def __init__(self,platform:str,apikey:str):
        config=self.PLATFORMS[platform]
        self.client=OpenAI(api_key=config['api_key'],base_url=config['base_url'])
        self.model=config['model']

    def chat(self,prompt:str):
        response=self.client.chat.completions.create(
            model=self.model,
            messages=[{'role':'user','content':prompt}],
            max_tokens=128,
            temperature=1.5
        )
        usage=response.usage
        print(f"\n\n输入token:{usage.prompt_tokens}")
        print(f"输出token:{usage.completion_tokens}")
        print(f"总消耗token:{usage.total_tokens}")
        return response.choices[0].message.content

    def chat_stream(self,prompt:str,system_prompt: str = "你是一个乐于助人的助手。"):
        stream=self.client.chat.completions.create(
            model=self.model,
            messages=[{'role': 'system', 'content': system_prompt}, {'role':'user','content':prompt}],
            stream=True,
            max_tokens=128
    )
        full_content=''
        input_tokens = 0
        output_tokens = 0
        total_tokens = 0
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content=chunk.choices[0].delta.content
                full_content+=content
                print(content,end='',flush=True)
            if chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
                total_tokens = chunk.usage.total_tokens
        print(f"\n\n[Token 统计]")
        print(f"输入 Token: {input_tokens}")
        print(f"输出 Token: {output_tokens}")
        print(f"总消耗 Token: {total_tokens}\n")
        return full_content

    def system_prompt(self,prompt:str):
        print("请输入要修改的人设：")

if __name__=='__main__':
    for i in LLM.PLATFORMS:
        ai=LLM(f'{i}','api_key')
        print(ai.chat("你是什么模型"))



ai=LLM("qwen",'sk-4e9a1788216243f586edb6b991415546')
    print(ai.chat("你好"))"""


from cryptography.fernet import Fernet
import os
"""#1.生成密钥
key=Fernet.generate_key()
print(f'加密密钥：{key.decode()}')

#2.加密数据
f=Fernet(key)
token=f.encrypt(b'1111')
print(f"加密后：{token.decode()}")

#3.解密数据
original=f.decrypt(token)
print(f'解密后：{original.decode()}')

#4.密钥保存
with open('serect.key','wb') as f:
    f.write(key)"""

#进阶

def encrypt(input_file,output_file,key_file):
    #加密 .env文件
    with open(input_file,'rb') as f:
        data=f.read()

    #生成密钥
    key=Fernet.generate_key()
    with open(key_file,'wb') as f:
        f.write(key)
    print(f"密钥已保存到：{key_file}")

    #加密并保存
    fernet=Fernet(key)
    encrypted=fernet.encrypt(data)
    with open(output_file,'wb') as f:
        f.write(encrypted)
    print(f"加密文件已保存到：{output_file}")

def decrypt(env_file,key_file,output_file='.enc.tmp'):
    #1.读取密钥
    with open(key_file,'rb') as f:
        key=f.read()

    #2.读取加密后的数据
    with open(env_file,'rb') as f:
        encrypted=f.read()

    #3.解密
    fernet=Fernet(key)
    decrypted=fernet.decrypt(encrypted)

    #4.将解密后的明文写入文件
    with open(output_file,'wb') as f:
        f.write(decrypted)
    print(f"解密成功,文件已保存到：{output_file}")

if __name__=='__main__':
    original_env='test.env'
    encrypted_file='test.enc'
    key_file='serect.key'
    decrypted_file='decrypted_test.env'

    test_content=b'1111'
    with open(original_env,'wb') as f:
        f.write(test_content)
    print("测试用.env文件已创建")

    encrypt(original_env,encrypted_file,key_file)
    print("已加密")

    decrypt(encrypted_file,key_file,decrypted_file)
    print("已解密")

    with open(original_env,'rb') as f:
        original_data=f.read()
    with open(decrypted_file,'rb') as f:
        decrypted_data=f.read()
    print("原文件",original_data)
    print("解密后的原文件",decrypted_data)



# 完整版
"""
from openai import OpenAI
import os
from secret_manager import SecretManager

sm=SecretManager()
sm.create_key()
sm.encrypt_env()
sm.decrypt_env()
api_key=os.getenv('DS_API_KEY')

class LLM:
    PLATFORMS={
        'ds':{'base_url':'https://api.deepseek.com/v1',
            'model':'deepseek-chat'},
        'qwen': {'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
               'model': 'qwen-plus'}
            }


    def __init__(self,platform:str):
        config=self.PLATFORMS[platform]
        self.client=OpenAI(api_key=api_key,base_url=config['base_url'])
        self.model=config['model']

    def chat(self,prompt:str):
        response=self.client.chat.completions.create(
            model=self.model,
            messages=[{'role':'user','content':prompt}],
            max_tokens=128,
            temperature=1.5
        )
        usage=response.usage
        print(f"\n\n输入token:{usage.prompt_tokens}")
        print(f"输出token:{usage.completion_tokens}")
        print(f"总消耗token:{usage.total_tokens}")
        return response.choices[0].message.content

    def chat_stream(self,prompt:str,system_prompt: str = "你是一个乐于助人的助手。"):
        stream=self.client.chat.completions.create(
            model=self.model,
            messages=[{'role': 'system', 'content': system_prompt}, {'role':'user','content':prompt}],
            stream=True,
            max_tokens=128
    )
        full_content=''
        input_tokens = 0
        output_tokens = 0
        total_tokens = 0
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                content=chunk.choices[0].delta.content
                full_content+=content
                print(content,end='',flush=True)
            if chunk.usage:
                input_tokens = chunk.usage.prompt_tokens
                output_tokens = chunk.usage.completion_tokens
                total_tokens = chunk.usage.total_tokens
        print(f"\n\n[Token 统计]")
        print(f"输入 Token: {input_tokens}")
        print(f"输出 Token: {output_tokens}")
        print(f"总消耗 Token: {total_tokens}\n")
        return full_content


"""


#secret_manager
"""
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
"""