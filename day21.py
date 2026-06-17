import os
from openai import OpenAI


def ai(user_prompt:str):
    global messages
    client = OpenAI(
        api_key=os.getenv('DS_API_KEY'),
        base_url='https://api.deepseek.com/v1'
                    )

    messages.append({'role': 'user', 'content': user_prompt})
    stream=client.chat.completions.create(
        model='deepseek-chat',
        messages=messages,
        stream=True,
        temperature=0.8
    )
    ans = ''
    print("AI：", end='')
    for i in stream:
        txt = i.choices[0].delta.content
        if txt:
            ans += txt
            print(txt, end='')
    print()
    write(user_prompt,ans)
    messages.append({'role': 'assistant', 'content': ans})

def write(user_prompt,ans):
    with open("AI_log.txt", "a", encoding="utf-8") as f:
        f.write(f" \n 用户：{user_prompt} \n AI：{ans}\n")


messages=[{'role':'system',
           'content':'你是一位深耕杭州20年的资深旅游顾问，拥有浙大旅游管理硕士学位。你的任务是为每位用户量身定制3天2晚的杭州三日游行程。1.你需要充分利用好用户的时间，通勤时间、人流高峰都要考虑到，留足缓冲不赶路。2.要包括经典地标比如西湖、灵隐寺，特色体验比如炒茶。3.要主动询问人数，用户的体力、兴趣，可根据用户的兴趣调整行程，给的计划格式严格按照：时间-地点-活动-交通-饮食，不可变更。语气要热情耐心，偶尔穿插与景点相关的趣闻。给出方案后要问：哪里需要调整，有没有特别想去的地方，以用户体验为上，但不要回答与旅游不相关的事情，你是专业的。'}]
while True:
    user_prompt=input("请输入：")
    ai(user_prompt)
