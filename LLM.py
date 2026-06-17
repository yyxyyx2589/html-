from openai import OpenAI
import os
from secret_manager import SecretManager

SecretManager.create_key()
sm=SecretManager()
sm.encrypt_env()
sm.decrypt_env()

api_key=os.getenv('DS_API_KEY')
print(api_key)
class LLM:
    PLATFORMS={
        'ds':{'base_url':'https://api.deepseek.com/v1',
            'model':'deepseek-chat'},
        'qwen': {'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
               'model': 'qwen-plus'}
            }


    def __init__(self,platform:str,apikey:str):
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