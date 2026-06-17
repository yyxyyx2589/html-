from openai import OpenAI
import json
import os
import re
import requests

client=OpenAI(api_key=os.getenv("DS_API_KEY"),
              base_url='https://api.deepseek.com/v1'
              )

# class AIrole:
#     #可持久化的AI角色
#     def __init__(self,name:str,system_prompt:str,model:str='deepseek-chat'):
#         self.name=name
#         self.system_prompt=system_prompt
#         self.model=model
#         self.history:list[dict]=[]
#
#     def chat(self,user_input:str)->str:
#     #发送消息 保留上下文
#         self.history.append({"role":"user","content":user_input})
#         messages=[{"role":"system","content":self.system_prompt}]+self.history
#         response = client.chat.completions.create(
#             model="deepseek-chat",  # 确保模型名称正确
#             messages=messages,
#         )
#         reply=response.choices[0].message.content
#         self.history.append({"role":"assistant","content":reply})
#         return reply
#
#     def reset(self):
#         #重置历史对话 保留角色设定
#         self.history=[]
#         print(f"[{self.name}] 对话历史已清空")
#
#     def get_history_count(self)->int:
#         return len(self.history)//2
#
# python_tutor=AIrole(
#     name="python",
#     system_prompt="你是一个python编程助教，用简单语言教初学者，每次回答要包含代码示例",
# )
# print(python_tutor.chat("什么是函数"))


class AIrole:
    #可持久化的AI角色
    def __init__(self,name:str,system_prompt:str,model:str='deepseek-chat'):
        self.name=name
        self.system_prompt=system_prompt
        self.model=model
        self.history:list[dict]=[]

    def chat(self,user_input:str)->str:
    #发送消息 保留上下文
        self.history.append({"role":"user","content":user_input})
        messages=[{"role":"system","content":self.system_prompt}]+self.history
        response = client.chat.completions.create(
            model="deepseek-chat",  # 确保模型名称正确
            messages=messages,
        )
        reply=response.choices[0].message.content
        self.history.append({"role":"assistant","content":reply})
        return reply

    def reset(self):
        #重置历史对话 保留角色设定
        self.history=[]
        print(f"[{self.name}] 对话历史已清空")

    def get_history_count(self)->int:
        return len(self.history)//2

system_prompt_template="""
##角色
你是一个抖音平台客服专家。

##行为准则
1.用友好热情的态度回答客户的问题
2.对客户的问题耐心询问，对于不清楚的细节要温柔询问
3.回答要清楚、仔细

##输出格式
1.每次回答完后询问客户还有什么问题
2.最后要说”很开心为您服务“

##边界限制
1.只回答抖音平台相关问题
2.不涉及政治、宗教等无关话题
3.超出限制则礼貌回答”很抱歉无法为您回答这个问题，请问还有什么需要帮助的吗“
"""

python_tutor=AIrole(
    name="tutor",
    system_prompt="你是一个python编程助教，对bug态度严格，要求学员修改后才能通过",
)
python_friend=AIrole(
    name="friend",
    system_prompt="你是一个python编程助教，但提倡鼓励式教学，即使代码错了也先肯定亮点",
)
dy=AIrole(
    name="客服",
    system_prompt=system_prompt_template,
)
text="""
def ab(a,b):
    return a+b
print(f"9-6的结果：{ab(9,6)}")
"""
# print(python_tutor.chat(text))
# print(python_friend.chat(text))
print(dy.chat('我的快递什么时候发货'))

