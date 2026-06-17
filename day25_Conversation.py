from openai import OpenAI
import json
import os
import re
import requests

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

class ConversationManager:

    def __init__(self,
                 system_prompt:str,
                 model:str='deepseek-chat',
                 max_history:int=5,
                 max_tokens:int=4000):
        self.system_prompt = system_prompt
        self.model = model
        self.max_history = max_history #对话轮数
        self.max_tokens = max_tokens
        self.history:list[dict]=[]
        self.turn_count=0

    def estimate_tokens(self,text:str)->int:
        chinese_count=sum(1 for c in text if '\u4e00' <=c<='\u9fff')
        other_count=len(text)-chinese_count
        return int(chinese_count/1.5+other_count/4)

    def trim_history(self):
        """修剪历史记录：超过限制则删除最早的对话轮"""
        while len(self.history)>self.max_history * 2:
            self.history.pop(0)
            self.history.pop(0)

        total_tokens=sum(self.estimate_tokens(m['content']) for m in self.history)
        while total_tokens > self.max_tokens and len(self.history) >=2:
            removed_user=self.history.pop(0)
            removed_ai=self.history.pop(0)
            total_tokens-=(self.estimate_tokens(removed_user['content']) + self.estimate_tokens(removed_ai['content']))

    def chat(self,user_input:str,verbose:bool=False)->str:
        """发送消息，自动管理上下文"""
        self.turn_count+=1
        self.history.append({'role':'user','content':user_input})

        messages=[{'role':'system','content':self.system_prompt}] + self.history

        if verbose:
            total_mag_tokens=sum(self.estimate_tokens(m['content']) for m in messages)
            print(f"[轮次{self.turn_count}],历史轮数：{len(self.history)//2},预计token：{total_mag_tokens}")

        response = client.chat.completions.create(
            model=self.model,  # 确保模型名称正确
            messages=messages,
        )
        reply=response.choices[0].message.content
        self.history.append({'role':'assistant','content':reply})

        self.trim_history()
        return reply

text=ConversationManager(system_prompt='给我一句话答复',max_history=3)
print(text.chat('1的快递丢了',verbose=True))
print(text.chat('2的快递丢了',verbose=True))
print(text.chat('3的快递丢了',verbose=True))
print(text.chat('4的快递丢了',verbose=True))
print(text.chat('一共有谁的快递丢了',verbose=True))
